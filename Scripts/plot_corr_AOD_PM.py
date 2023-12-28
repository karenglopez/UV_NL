from sklearn.linear_model import LinearRegression
from Modules.functions import fill_number
from Modules.params import get_params
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from os.path import join
from numpy import array
from sys import argv
from pandas import (
    to_datetime,
    DataFrame,
    read_csv,
)


def fit(x: DataFrame,
        y: DataFrame) -> LinearRegression:
    Regression = LinearRegression(fit_intercept=False)
    x = x.to_numpy()
    x = x.reshape(-1, 1)
    y = y.to_numpy()
    y = y.flatten()
    regression = Regression.fit(x, y)
    score = get_R2(x,
                   y,
                   regression)
    return regression, score


def get_R2(x: array,
           y: array,
           regression: LinearRegression) -> float:
    y_pred = regression.predict(x)
    score = r2_score(y, y_pred)
    return score


params = get_params()
pollutant = argv[1]
station_key = "NO"
filename = f"{pollutant}_2015_2022.csv"
filename = join(params["path data"],
                "SIMA",
                filename)
data = read_csv(filename,
                index_col=0,
                parse_dates=True)
station_data = DataFrame(data[station_key])
filename = "AOD_search.csv"
filename = join(params["path results"],
                filename)
aod = read_csv(filename,
               index_col=0,
               parse_dates=True)
aod[pollutant] = 0
for index in aod.index:
    date = index.date()
    hour = index.hour
    hour = fill_number(hour,
                       2)
    date = f"{date} {hour}:00"
    date = to_datetime(date)
    pm_hour = station_data.loc[date]
    pm_hour = pm_hour[station_key]
    aod.loc[index, pollutant] = pm_hour
regression, score = fit(aod["AOD"],
                        aod[pollutant])
coef = regression.coef_
coef = round(coef[0], 4)
y_pred = regression.predict([[0.2], [0.6]])
fig = plt.figure()
ax = fig.add_subplot(projection='polar')
ax.scatter(aod["AOD"],
           aod[pollutant])
# plt.plot([0, 0.6],
# y_pred,
# color="#6a994e",
# label=f"y={coef}x")
plt.ylim(0, 40)
plt.xlim(0.2, 0.6)
plt.ylabel("PM2.5")
plt.xlabel("AOD$_{550nm}$")
plt.legend(frameon=False)
plt.tight_layout()
plt.show()
