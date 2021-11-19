#merge request update1
from datetime import datetime
import MetaTrader5 as mt5
import pandas
import pytz

barsAmount = 99000
timezone = pytz.timezone("Etc/UTC")
EUR_USD = 'EURUSD'
HIGH = 'high'
LOW = 'low'
round_num = 5


def get_prices_for_whole_period():
    now = datetime.now(timezone)
    rates_whole_period = mt5.copy_rates_from(EUR_USD, mt5.TIMEFRAME_H1, now, barsAmount)
    rates_frame = pandas.DataFrame(rates_whole_period)

    high_price = rates_frame[[HIGH]]
    low_price = rates_frame[[LOW]]
    bar_size = high_price[HIGH] - low_price[LOW]
    print('Максимальная свеча за весь период: {round(bar_size.max(), round_num)}')
    print('Минимальная свеча за весь период: {round(bar_size.min(), round_num)}')


def get_prices_for_quarter(year, time_from, time_to, quarter):
    rates_in_range = mt5.copy_rates_range(EUR_USD, mt5.TIMEFRAME_H1, time_from, time_to)
    rates_frame = pandas.DataFrame(rates_in_range)

    high_price = rates_frame[[HIGH]]
    low_price = rates_frame[[LOW]]
    bar_size = high_price[HIGH] - low_price[LOW]
    print(f'Максимальная свеча за {quarter} квартал {year} года: {round(bar_size.max(), round_num)}')
    print(f'Минимальная свеча за {quarter} квартал {year} года: {round(bar_size.min(), round_num)}')


def get_prices_for_quarters():
    year = 1970
    while year < 2021:
        get_prices_for_quarter(year, datetime(year, 1, 1, tzinfo=timezone), datetime(year, 3, 31, tzinfo=timezone), 1)
        get_prices_for_quarter(year, datetime(year, 4, 1, tzinfo=timezone), datetime(year, 6, 30, tzinfo=timezone), 2)
        get_prices_for_quarter(year, datetime(year, 7, 1, tzinfo=timezone), datetime(year, 9, 30, tzinfo=timezone), 3)
        get_prices_for_quarter(year, datetime(year, 10, 1, tzinfo=timezone), datetime(year, 12, 31, tzinfo=timezone), 4)
        year += 1
    get_prices_for_quarter(year, datetime(year, 1, 1, tzinfo=timezone), datetime(year, 3, 31, tzinfo=timezone), 1)


if not mt5.initialize():
    print(f'Ошибка инициализации MetaTrader5: {mt5.last_error()}')
    quit()


print('Найти максимальную и минимальную свечи на весь период по EURUSD')
get_prices_for_whole_period()

print('\nНайти максимальную и минимальную свечи за каждый квартал по EURUSD')
get_prices_for_quarters()

mt5.shutdown()
