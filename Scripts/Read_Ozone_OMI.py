from Modules.params import get_params
from Modules.functions import ls
from Modules.OMI import OzoneOMI
from os.path import join
from numpy import isnan
from pandas import (
    to_datetime,
    DataFrame,
    Timestamp,
)


def fill_data(data: DataFrame) -> DataFrame:
    mean = results["Ozone"].resample("MS").mean()
    mean = DataFrame(mean)
    data["Ozone"] = data.apply(lambda row:
                               get_mean(row[0], mean)
                               if isnan(row[1])
                               else row[1],
                               axis=1)
    data.drop(columns=["Date"],
              inplace=True)
    return data


def get_mean(date: Timestamp,
             mean) -> float:
    date = to_datetime(date)
    first_date = date.replace(day=1)
    value = mean.loc[first_date]
    value = float(value)
    return value


params = get_params()
params.update({
    "file results": "Ozone.csv",
    "longitude": -100.34,
    "latitude": 23.730,
})
files = ls(params["path Ozone OMI"])
results = DataFrame(columns=["Date",
                             "Ozone"])
OMI = OzoneOMI()
for i, file in enumerate(files):
    ozone = OMI.read(params,
                     file)
    results.loc[i] = ozone
results.index = to_datetime(results["Date"])
fill_data(results)
filename = join(params["path results"],
                params["file results"])
results.to_csv(filename)
