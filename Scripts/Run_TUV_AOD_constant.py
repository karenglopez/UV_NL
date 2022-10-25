from Modules.TUV import TUVResults
from Modules.functions import (
    create_input_file,
    get_daily_data,
    date2yymmdd,
    read_data,
)
from pandas import to_datetime,
from os.path import join
from os import system
from sys import argv

params = {
    "station": "PALA",
    "hour initial": 6,
    "hour final": 20,
    "date": argv[1],
    "AOD": 0.3,
}

filename = "Ozone.csv"
filename = join(params["path results"],
                filename)
OMI = read_data(filename)
date = to_datetime(params["date"])
date = date.date()
ozone = get_daily_data(OMI,
                       date)
ozone = float(ozone.iloc[0])
create_input_file(params,
                  date,
                  ozone,
                  params["AOD"])
system("./tuv.out")
TUV = TUVResults()
filename = date2yymmdd(date)
filename = f"{filename}.txt"
TUV.read(params,
         filename)
data = TUV.data
data.index = to_datetime(data["Date"])
data = data.drop(columns=["Date"])
data["UV"] = data.sum(axis=1)
data = data.drop(columns=["UVB",
                          "UVB*",
                          "UVA"])
date = str(date)
date = date.replace("-",
                    "_")
filename = f"{date}.csv"
filename = join(params["path results"],
                "TUV/AOD_constant",
                filename)
data.to_csv(filename)
