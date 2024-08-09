import json
import logging
import time
from kafka import KafkaProducer, KafkaConsumer

from common.bindings.kafka.decoders import decode_thrift


class Kafka:

    def __init__(self, bootstrap_servers='localhost:9092', user=None, keytab=None):
        self.bootstrap_servers = bootstrap_servers
        self.user = user
        self.keytab = keytab
        self.security_protocol = "SASL_PLAINTEXT"
        self.sasl_mechanism = "GSSAPI"
        self.producer = None
        self.consumer = None

        self.logger = logging.getLogger('Kafka')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.producer:
            self.producer.close()

        if self.consumer:
            self.consumer.close()

    def create_producer(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                security_protocol=self.security_protocol,
                sasl_mechanism=self.sasl_mechanism,
                sasl_kerberos_service_name="kafka",
            )
            self.logger.info("Producer успешно создан")
        except Exception as e:
            self.logger.error(f"Не удалось создать producer: {e}")
            raise

    def send_message(self, topic, message):

        if not self.producer:
            self.create_producer()

        try:
            self.producer.send(topic, value=message)
            self.producer.flush()
            self.logger.info(f"Сообщение отправлено в топик: {topic}")
        except Exception as e:
            self.logger.error(f"Не удалось отправить сообщение в топик: {e}")
            raise

    def create_consumer(self, topic, sasl_kerberos_service_name="kafka", auto_offset_reset='latest',
                        enable_auto_commit=True, consumer_timeout_ms=30000, api_version_auto_timeout_ms=1000000,
                        connections_max_idle_ms=1500000, request_timeout_ms=1000000, **kwargs):
        try:
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                security_protocol=self.security_protocol,
                sasl_mechanism=self.sasl_mechanism,
                sasl_kerberos_service_name=sasl_kerberos_service_name,
                auto_offset_reset=auto_offset_reset,
                enable_auto_commit=enable_auto_commit,
                consumer_timeout_ms=consumer_timeout_ms,
                api_version_auto_timeout_ms=api_version_auto_timeout_ms,
                connections_max_idle_ms=connections_max_idle_ms,
                request_timeout_ms=request_timeout_ms,
                **kwargs
            )
            self.logger.info(f"Consumer создан для топика: {topic}")
        except Exception as e:
            self.logger.error(f"Не удалось успешно создать consumer: {e}")
            raise

    def read_messages(self, depth=5):
        if not self.consumer:
            raise Exception("Consumer не был инициализирован. Сначала нужно вызвать create_consumer()")

        messages = []

        try:
            self.consumer.poll(0)

            while len(messages) < depth:
                message_pack = self.consumer.poll(timeout_ms=1000)

                # Проверяем, что пакет сообщений не пуст
                if not message_pack:
                    continue

                for tp, msgs in message_pack.items():
                    for message in msgs:
                        if len(messages) < depth:
                            messages.append(message)
                        else:
                            return messages

        except Exception as e:
            raise

    def send_and_search_by_json(self, *search_criteria, send_function=None, max_messages_search=1, search_depth=100000,
                                offset=0, max_wait_time=60, decoding_model=None, **kwargs):

        if not self.consumer:
            raise Exception("Consumer не был инициализирован. Сначала нужно вызвать create_consumer()")

        try:
            self.consumer.poll(0)

            if offset > 0:
                partitions = self.consumer.assignment()
                for partition in partitions:
                    end_offset = self.consumer.end_offsets([partition])[partition]
                    new_offset = end_offset - offset if end_offset - offset > 0 else 0
                    self.consumer.seek(partition, new_offset)

            messages = []
            checked_messages = 0
            start_time = time.time()

            flag = False

            while len(messages) < max_messages_search and checked_messages < search_depth:

                message_pack = self.consumer.poll(timeout_ms=1000)

                if not flag:
                    send_function(**kwargs)
                    flag = True

                for tp, msgs in message_pack.items():
                    for message in msgs:
                        checked_messages += 1
                        try:

                            if decoding_model is not None:
                                msg_value = decode_thrift(message=message.value, model=decoding_model)
                            else:
                                msg_value = json.loads(message.value.decode('utf-8'))

                            if all(msg_value.get(key) == value for key, value in search_criteria):
                                messages.append(msg_value)
                                if len(messages) >= max_messages_search:
                                    break
                        except json.JSONDecodeError as e:
                            self.logger.error(f"Не удалось декодировать json: {e}")
                            continue
                    if len(messages) >= max_messages_search or checked_messages >= search_depth:
                        break

                if not message_pack and (time.time() - start_time) > max_wait_time:
                    self.logger.info("Превышено максимальное время ожидания сообщений")
                    break

            if messages:
                self.logger.info(f"Найдено сообщений: {len(messages)}")
            else:
                self.logger.info(f"Сообщений не найдено. Проверено сообщений: {len(messages)}")
            return messages
        except Exception as e:
            self.logger.error(f"Ошибка при чтении сообщений: {e}")
            raise

    def find_message_by_key(self, search_key, search_depth=100000):
        """
        Функция для поиска сообщения в топике Kafka по ключу
        """
        if not self.consumer:
            raise Exception("Consumer не был инициализирован. Сначала нужно вызвать create_consumer()")

        try:
            counter = 0

            for message in self.consumer:
                if message.key == search_key:
                    self.consumer.close()
                    return message.value

                counter += 1
                if counter >= search_depth:
                    break

            self.consumer.close()
            return None

        except Exception as e:
            self.logger.error(f"Ошибка при чтении сообщений: {e}")
            raise
