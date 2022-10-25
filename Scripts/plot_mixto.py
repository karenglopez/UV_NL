from Modules.params import get_params
import matplotlib.pyplot as plt
from os.path import join
from pandas import (
    to_datetime,
    read_csv,
)

params = get_params()
filename = "mediciones.csv"
filename = join(params["path data"],
                filename)
data = read_csv(filename,
                index_col=3,
                parse_dates=True)
stations = ["Las palmas",
            "Obispado",
            "Chipinque",
            "El toro",
            ]
dates = sorted(list(set(data.index.date)))
for station, date in zip(stations,
                         dates):
    daily_data = data[data.index.date == date]
    daily_data.index = daily_data.index.map(lambda date:
                                            date.replace(year=2022,
                                                         month=1,
                                                         day=1)
                                            )
    plt.scatter(daily_data.index,
                daily_data["Mixto"],
                label=station)
hours = range(9, 19)
date_hour = [to_datetime(f"2022-01-01 {hour}:00:00")
             for hour in hours]
plt.xticks(date_hour,
           hours)
# plt.ylim(0, 60)
plt.xlabel("Hora local")
plt.ylabel("Irradiancia UV (W/m$^2$)")
plt.legend(frameon=False,
           loc="lower center")
plt.tight_layout()
filename = "mixto.png"
filename = join(params["path graphics"],
                filename)
plt.savefig(filename,
            dpi=400)
plt.show()
