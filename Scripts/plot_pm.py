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
date = date.date()
parameters = params[pollutant]

filename = f"{pollutant}_2015_2022.csv"
filename = join("data",
                filename)
data = read_csv(filename,
                index_col=0,
                parse_dates=True)
daily_data = data[data.index.date == date]
plt.subplots(figsize=(10, 5))
for station in params["stations"]:
    station_data = DataFrame(daily_data[station])
    color = params["stations"][station]["color"]
    name = params["stations"][station]["name"]
    plt.plot(station_data,
             color=color,
             label=name)
plt.legend(frameon=False)
plt.axhline(parameters["line"],
            color="#6a040f")
plt.xticks(daily_data.index,
           daily_data.index.hour)
plt.title(f"Fecha: {date}")
plt.ylabel(f"{pollutant} ($\\mu$gr/m$^3$)")
plt.xlabel("Hora local")
plt.tight_layout()
filename = argv[2].replace("-", "_")
filename = f"{filename}_{argv[1]}.png"
filename = join(params["path graphics"],
                filename)
plt.savefig(filename,
            dpi=400)
