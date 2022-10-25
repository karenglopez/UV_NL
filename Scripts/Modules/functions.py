from os import listdir
from pandas import (
    DataFrame,
    Timestamp,
    read_csv
)


def ls(path: str) -> list:
    """
    -
    """
    return sorted(listdir(path))


def fill_number(number: int,
                fill: int) -> str:
    """
    -
    """
    number_str = str(number)
    number_str = number_str.zfill(fill)
    return number_str


def date2yymmdd(date: Timestamp) -> str:
    """
    -
    """
    month = date.month
    month = fill_number(month,
                        2)
    year = date.year
    year = str(year)[2:]
    day = date.day
    day = fill_number(day,
                      2)
    date_str = "".join([year,
                        month,
                        day])
    return date_str


def create_input_file(params: dict,
                      date: Timestamp,
                      ozone: float,
                      AOD: float) -> None:
    """
    -
    """
    file = open("../data.txt", "w")
    date_str = date2yymmdd(date)
    month = date.month
    year = date.year
    day = date.day
    hour_i = params["hour initial"]
    hour_f = params["hour final"]
    station = params["station"]
    text = " ".join([station,
                    date_str,
                    str(AOD),
                    str(ozone),
                    str(year),
                    str(month),
                    str(day),
                    str(hour_i),
                    str(hour_f)])
    file.write(text)
    file.close()


def get_daily_data(data: DataFrame,
                   date: Timestamp) -> DataFrame:
    """
    -
    """
    daily_data = data[data.index.date == date]
    return daily_data


def read_data(filename: str) -> DataFrame:
    """
    -
    """
    data = read_csv(filename,
                    index_col=0,
                    parse_dates=True)
    return data


def get_unique_hours(data: DataFrame) -> list:
    """
    -
    """
    hours = sorted(list(set(data.index.hour)))
    return hours
