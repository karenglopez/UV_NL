from Modules.params import get_params
from Modules.TUV import TUVResults
from Modules.functions import (
    create_input_file,
    get_daily_data,
    date2yymmdd,
    read_data,
)
from os.path import join
from os import system
from sys import argv
from pandas import (
    to_datetime,
    DataFrame,
    concat,
)
params = get_params()
params.update({
    "station": "PALA",
    "date": argv[1],
})

filename = "Ozone.csv"
filename = join(params["path results"],
                filename)
OMI = read_data(filename)
date = to_datetime(params["date"])
date = date.date()
ozone = get_daily_data(OMI,
                       date)
ozone = float(ozone.iloc[0])
filename = "AOD_search.csv"
filename = join(params["path results"],
                filename)
aod = read_data(filename)
aod = get_daily_data(aod,
                     date)
TUV = TUVResults()
filename = date2yymmdd(date)
filename = f"{filename}.txt"
results = DataFrame()
for index in aod.index:
    params["hour initial"] = index.hour
    params["hour final"] = index.hour+1
    aod_hour = aod.loc[index]
    aod_hour = float(aod_hour[0])
    create_input_file(params,
                      date,
                      ozone,
                      aod_hour)
    system("./tuv.out")
    TUV.read(params,
             filename)
    data = TUV.data
    data.index = to_datetime(data["Date"])
    data = data.drop(columns=["Date"])
    data["UV"] = data.sum(axis=1)
    data = data.drop(columns=["UVB",
                              "UVB*",
                              "UVA"])
    data = data[data.index.hour == index.hour]
    data = data[data.index.minute == index.minute]
    results = concat([results,
                      data])
filename = f"{date}.csv"
filename = join(params["path results"],
                "TUV/AOD_found",
                filename)
filename = filename.replace("-",
                            "_")
results.to_csv(filename)
