from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from sys import argv
from pandas import (
    to_datetime,
    DataFrame,
    read_csv
)

params = get_params()
params.update({
    "PM2.5": {
        "line": 15,
    },
    "PM10": {
        "line": 45,
    },
    "stations": {
        "CE": {
            "name": "Obispado",
            "color": "#dc2f02",
        },
        "NO": {
            "name": "San Bernabé",
            "color": "#000000",
        },
    },
})

pollutant = argv[1]
date = to_datetime(argv[2])
station_key = "NO"
station = params["stations"][station_key]["name"]
date = date.date()
parameters = params[pollutant]
filename = f"{pollutant}_2015_2022.csv"
filename = join(params["path data"],
                "SIMA",
                filename)
data = read_csv(filename,
                index_col=0,
                parse_dates=True)
pm = data[data.index.date == date]
station_data = DataFrame(pm[station_key])

filename = "AOD_search.csv"
filename = join(params["path results"],
                filename)
aod = read_csv(filename,
               index_col=0,
               parse_dates=True)
aod = aod[aod.index.date == date]
aod = aod.resample("H").mean()

station_data = station_data.loc[aod.index]
color = params["stations"][station_key]["color"]

fig, ax1 = plt.subplots(figsize=(12, 4))
ax2 = ax1.twinx()
ax1.plot(station_data,
         color=color,
         label=pollutant)
ax2.plot(aod["AOD"],
         color="red",
         label="AOD$_{550nm}$")
fig.legend(frameon=False,
           loc="center")
ax1.axhline(parameters["line"],
            color="#6a040f")
plt.xticks(aod.index,
           aod.index.hour)
plt.title(f"Fecha: {date}")
ax1.set_ylabel(f"{pollutant} ($\\mu$gr/m$^3$)")
ax2.set_ylabel("AOD$_{550nm}$")
plt.xlabel("Hora local")
plt.tight_layout()
filename = argv[2].replace("-", "_")
filename = f"{filename}_{argv[1]}_AOD.png"
filename = join(params["path graphics"],
                filename)
plt.savefig(filename,
            dpi=400)
