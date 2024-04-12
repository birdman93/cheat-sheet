import time


def retry_request(max_retries=5, delay=30):
    """
    Если сервис, с которым общаемся по апи, не отличается стабильностью в поведении, тогда можно использовать этот
    декоратор, в котором задаются число попыток и время ожидания между ними
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_count = 0

            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"Попытка ретрая: {retry_count + 1} из {max_retries}. Ждем: {delay} секунд.")
                    time.sleep(delay)
                    retry_count += 1

            raise Exception(f"Не удалось успешно выполнить запрос. Было попыток: {max_retries}.")

        return wrapper
    return decorator
