from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from sys import argv
from pandas import (
    to_datetime,
    DataFrame,
    read_csv,
    concat
)

params = get_params()

pollutant = argv[1]
date = to_datetime(argv[2])
station_key = "NO"
date = date.date()
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

data = concat([station_data,
               aod],
              axis=1)
data.columns = ["PM2.5",
                "AOD",
                "RD"]
plt.scatter(data["PM2.5"],
            data["AOD"])
plt.title(f"Fecha: {date}")
plt.xlabel("PM2.5")
plt.ylabel("AOD$_{550nm}$")
plt.show()
# ax1.plot(station_data,
# color=color,
# label=pollutant)
# ax2.plot(aod["AOD"],
# color="red",
# label="AOD$_{550nm}$")
# fig.legend(frameon=False,
# loc="center")
# ax1.axhline(parameters["line"],
# color="#6a040f")
# plt.xticks(aod.index,
# aod.index.hour)
# ax1.set_ylabel(f"{pollutant} ($\\mu$gr/m$^3$)")
# ax2.set_ylabel("AOD$_{550nm}$")
# plt.xlabel("Hora local")
# plt.tight_layout()
# filename = argv[2].replace("-", "_")
# filename = f"{filename}_{argv[1]}_AOD.png"
# filename = join(params["path graphics"],
# filename)
# plt.savefig(filename,
# dpi=400)
