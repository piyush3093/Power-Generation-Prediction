# Dealing with missing Values

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

weather_actual = pd.read_csv('weather_actual_cleaned.csv')
weather_forecast = pd.read_csv('weather_forecast_cleaned.csv')
power_actual = pd.read_csv('power_actual.csv')

weather_actual.datetime_local = pd.to_datetime(weather_actual.datetime_local)
weather_forecast.datetime_local = pd.to_datetime(weather_forecast.datetime_local)

weather_actual.wind_bearing = weather_actual.wind_bearing.replace(-9999, np.nan)
mean = weather_actual.wind_bearing.dropna().mean()
weather_actual.wind_bearing = weather_actual.wind_bearing.replace(np.nan, mean)

weather_actual.wind_speed = weather_actual.wind_speed.replace(-9999, np.nan)
mean = weather_actual.wind_speed.dropna().mean()
weather_actual.wind_speed = weather_actual.wind_speed.replace(np.nan, mean)

weather_actual = weather_actual.replace(-9999, np.nan)

# Wind Gust
for i in range(0, len(weather_actual)):
    if pd.isnull(weather_actual.pressure[i]):
        if(i%3 == 1):
            weather_actual.pressure[i] = (weather_actual.pressure[i-1] + weather_actual.pressure[i+2])/2
        elif(i%3 == 2):
            weather_actual.pressure[i] = (weather_actual.pressure[i-2] + weather_actual.pressure[i+1])/2
            
for i in range(0, len(weather_actual)):
    if (weather_actual.datetime_local[i].month == 3 and weather_actual.datetime_local[i].year == 2019):
        print(i)
        break
   
mean = weather_actual.ozone[4859:5603].mean()
weather_actual.wind_gust.mean()

for i in range(0, len(weather_actual)):
    if(pd.isnull(weather_actual.wind_gust[i])):
        if(weather_actual.datetime_local[i].month == 10):
            weather_actual.wind_gust[i] = 4.2453
        elif(weather_actual.datetime_local[i].month == 11):
            weather_actual.wind_gust[i] = 3.1971
        elif(weather_actual.datetime_local[i].month == 12):
            weather_actual.wind_gust[i] = 2.6705
        elif(weather_actual.datetime_local[i].month == 1):
            weather_actual.wind_gust[i] = 3.4837
        elif(weather_actual.datetime_local[i].month == 2):
            weather_actual.wind_gust[i] = 4.2372

plt.scatter(x = weather_actual.index[3264:], y = weather_actual.uv_index[3264:])
mean = weather_actual.ozone.dropna().mean()
weather_actual.ozone = weather_actual.ozone.replace(np.nan, mean)

#uv index

weather_actual['time'] = [weather_actual.datetime_local[i].hour for i in range(0, len(weather_actual))]
uv_index = weather_actual.uv_index.groupby(weather_actual.time).mean()

for i in range(0, len(weather_actual)):
    if(pd.isnull(weather_actual.uv_index[i])):
        weather_actual.uv_index[i] = uv_index[weather_actual.time[i]]
        
# Precip probability

mean = weather_actual.precip_probability.dropna().mean()
weather_actual.precip_probability = weather_actual.precip_probability.replace(np.nan, mean)


plt.scatter(x = weather_actual.index[3264:], y = weather_actual.precip_intensity[3264:])
mean = weather_actual.precip_intensity.dropna().mean()
weather_actual.precip_intensity = weather_actual.precip_intensity.replace(np.nan, mean)

weather_actual['month'] = [weather_actual.datetime_local[i].month for i in range(0, len(weather_actual))]
precip_intensity = weather_actual.precip_intensity.groupby(weather_actual.month).mean()

for i in range(0, len(weather_actual)):
    if(pd.isnull(weather_actual.precip_intensity[i])):
        weather_actual.precip_intensity[i] = precip_intensity[weather_actual.month[i]]

weather_actual.to_csv('weather_actual_cleaned.csv')
weather_forecast.to_csv('weather_forecast.cleaned.csv')


