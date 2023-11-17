from weather import get_weather

import os
import telebot
from loguru import logger


def telegram_bot():

    token = str(os.environ["WEATHER_BOT_TOKEN"])

    bot = telebot.TeleBot(token)

    start_text = "Напишите название города для получения прогноза погоды"

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.from_user.id,
                         start_text,
                         parse_mode='Markdown')

    @bot.message_handler(content_types=['text'])
    def weather(message):

        city = message.text
        logger.info(f"Бот получил запрос с текстом: {city}")

        forecast = get_weather(city=city)

        bot.send_message(message.from_user.id, forecast)
        logger.info(f"Бот отправил ответ по запросу: {city}")

    return bot


if __name__ == '__main__':

    # Настройка логирования в файл "app.log" с уровнем INFO
    logger.add("app.log", level="INFO")

    bot = telegram_bot()

    while True:

        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as ex:
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')