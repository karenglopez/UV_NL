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
                index_col=0,
                parse_dates=True)
dates = sorted(list(set(data.index.date)))
for date in dates:
    daily_data = data[data.index.date == date]
    daily_data.index = daily_data.index.map(lambda date:
                                            date.replace(year=2022,
                                                         month=1,
                                                         day=1)
                                            )
    plt.plot(daily_data["Palacio de Justicia"],
             label=date)
hours = range(8, 18)
date_hour = [to_datetime(f"2022-01-01 {hour}:00:00")
             for hour in hours]
plt.xticks(date_hour,
           hours)
plt.ylim(0, 60)
plt.xlabel("Hora local")
plt.ylabel("Irradiancia UV (W/m$^2$)")
plt.legend(frameon=False,
           loc="lower center")
plt.tight_layout()
filename = "palacio_de_justicia.png"
filename = join(params["path graphics"],
                filename)
plt.savefig(filename,
            dpi=400)
plt.show()
