from cache_utils import cache_results

import datetime
import calendar
import random
from dateutil.relativedelta import relativedelta


@cache_results
def add_years_months_days_to_date(date: datetime.date = None,
                                  years: int = 0,
                                  months: int = 0,
                                  weeks: int = 0,
                                  days: int = 0) -> datetime.date:
    """
    Прибавляет к дате нужно количество месяцев (с учетом високосных годов)
    """

    # Переводим поданные на вход годы и недели в месяцы и дни соответственно
    months = months + (years * 12)
    days += weeks * 7

    # Обрабатываем переход к следующему месяцу, если нужно
    while days > 0:
        days_in_month = calendar.monthrange(date.year, date.month)[1]
        remaining_days_in_month = days_in_month - date.day + 1

        if remaining_days_in_month > days:
            date += datetime.timedelta(days=days)
            break
        else:
            date += datetime.timedelta(days=remaining_days_in_month)
            days -= remaining_days_in_month
            date = date.replace(day=1) + datetime.timedelta(days=1)

    # Добавляем месяцы
    while months > 0:
        new_year = date.year + (date.month + months - 1) // 12
        new_month = (date.month + months) % 12
        if new_month == 0:
            new_month = 12
        last_day = calendar.monthrange(new_year, new_month)[1]
        new_day = min(date.day, last_day)
        date = date.replace(year=new_year, month=new_month, day=new_day)
        months -= 1

    return date


@cache_results
def subtract_years_months_days_to_date(date: datetime.date = None,
                                       years: int = 0,
                                       months: int = 0,
                                       weeks: int = 0,
                                       days: int = 0) -> datetime.date:
    """
    Вычитает к дате нужно количество месяцев (с учетом високосных годов)
    """

    # Переводим поданные на вход годы и недели в месяцы и дни соответственно
    months = months + (years * 12)
    days += weeks * 7

    # Вычитаем месяцы и дни с использованием relativedelta
    delta = relativedelta(months=months, days=days)
    new_date = date - delta

    return new_date


def random_date_from_range(start_date: datetime.date = None, end_date: datetime.date = None) -> datetime.date:
    """
    Возвращает случайную дату из заданного диапазона
    """

    # Рассчитываем количество дней между начальной и конечной датами
    total_days = (end_date - start_date).days + 1

    # Генерируем случайное количество дней от начальной даты
    random_days = random.randint(0, total_days - 1)

    # Добавляем случайное количество дней к начальной дате
    random_date = start_date + datetime.timedelta(days=random_days)

    return random_date
