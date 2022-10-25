from Modules.params import get_params
from Modules.TUV import TUVResults
from Modules.functions import (
    create_input_file,
    get_daily_data,
    date2yymmdd,
    read_data,
)
from pandas import DataFrame
from os.path import join
from numpy import sum
from numpy import inf
from os import system


def get_AOD_initial(params: dict) -> float:
    """
    -
    """
    aod_i = params["AOD inferior"]
    aod_f = params["AOD superior"]
    aod = (aod_i+aod_f)/2
    return aod


def get_RD(measurement: float,
           model: float) -> float:
    """
    -
    """
    RD = (measurement-model)/measurement
    RD = RD*100
    RD = round(RD, 4)
    return RD


def get_new_AOD(params: dict,
                RD: float,
                AOD: float) -> float:
    """
    -
    """
    if RD > 0:
        params["AOD f"] = AOD
        AOD = params["AOD i"] + AOD
    else:
        aux = AOD
        params["AOD f"] = AOD
        AOD = params["AOD f"] + AOD
        AOD = AOD+aux
    AOD = AOD/2
    AOD = round(AOD, 5)
    return AOD


params = get_params()
params.update({
    "file results": "AOD_search.csv",
    "AOD inferior": 0.001,
    "AOD superior": 10,
    "station": "PALA",
    "RD limit": 10,
})
params["AOD initial"] = get_AOD_initial(params)
TUV = TUVResults()
filename = "Ozone.csv"
filename = join(params["path results"],
                filename)
OMI = read_data(filename)
filename = "Palacio_de_Justicia.csv"
filename = join(params["path data"],
                filename)
measurements = read_data(filename)
table = DataFrame(columns=["AOD",
                           "RD"])
for date_index in OMI.index:
    date_str = date2yymmdd(date_index)
    date_data = get_daily_data(measurements,
                               date_index.date())
    TUV_filename = f"{date_str}.txt"
    TUV_filename = join(params["path results"],
                        TUV_filename)
    ozone = OMI.loc[date_index]
    ozone = float(ozone)
    for date in date_data.index:
        measurement = measurements.loc[date]
        measurement = float(measurement)
        params["hour initial"] = date.hour
        params["hour final"] = date.hour+1
        minute = date.minute
        params["AOD i"] = params["AOD inferior"]
        params["AOD f"] = params["AOD superior"]
        RD = inf
        AOD = params["AOD initial"]
        print("-"*30)
        print(date)
        while RD > params["RD limit"] or RD < 0:
            create_input_file(params,
                              date,
                              ozone,
                              AOD)
            system("./tuv.out")
            TUV.read(params,
                     TUV_filename)
            results = TUV.data
            model = results.iloc[minute]
            # Get only UV
            model = model[["UVB",
                           "UVB*",
                          "UVA"]]
            model = sum(model)
            RD = get_RD(measurement,
                        model)
            AOD = get_new_AOD(params,
                              RD,
                              AOD)
        table.loc[date] = [AOD,
                           RD]
table.index.name = "Date"
filename = join(params["path results"],
                params["file results"])
table.to_csv(filename)
