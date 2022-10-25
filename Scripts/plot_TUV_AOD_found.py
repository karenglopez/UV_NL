from Modules.params import get_params
import matplotlib.pyplot as plt
from Modules.functions import (
    get_unique_hours,
    get_daily_data,
    read_data,
)
from pandas import to_datetime
from os.path import join
from sys import argv


params = get_params()
params.update({
    "date": argv[1],
})
date = to_datetime(params["date"])
date = date.date()
filename = "Palacio_de_Justicia.csv"
filename = join(params["path data"],
                filename)
measurements = read_data(filename)
measurements = get_daily_data(measurements,
                              date)
filename = str(date)
filename = filename.replace("-",
                            "_")
filename = f"{filename}.csv"
filename = join(params["path results"],
                "TUV/AOD_found",
                filename)
model = read_data(filename)
hours = get_unique_hours(model)
hours.append(hours[-1]+1)
date_hour = [to_datetime(f"{date} {hour}:00")
             for hour in hours]
plt.subplots(figsize=(12, 4))
plt.plot(measurements,
         color="#38a3a5",
         label="San Bernabé")
plt.plot(model,
         color="#6a040f",
         label="Modelo TUV")
plt.xlabel("Hora local (h)")
plt.ylabel("Irradiancia UV (W/m$^2$)")
plt.title(date)
plt.xticks(date_hour,
           hours)
plt.xlim(date_hour[0],
         date_hour[-1])
plt.ylim(0, 70)
plt.grid(ls="--",
         color="#000000",
         alpha=0.6)
plt.legend(frameon=False,
           ncol=2)
plt.tight_layout()
filename = f"{date}_TUV.png"
filename = filename.replace("-",
                            "_")
filename = join(params["path graphics"],
                "TUV/AOD_found",
                filename)
plt.savefig(filename,
            dpi=400)
