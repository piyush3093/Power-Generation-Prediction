# Exploratory Data Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

power_actual = pd.read_csv("power_actual.csv")
weather_actual = pd.read_csv("weather_actuals.csv")
weather_forecast = pd.read_csv("weather_forecast.csv")

power_actual = power_actual.drop('Unnamed: 0', axis = 1)
weather_actual = weather_actual.drop('Unnamed: 0', axis = 1)
weather_forecast = weather_forecast.drop('Unnamed: 0', axis = 1)

weather_forecast.columns
weather_actual.columns
print(weather_actual.columns == weather_forecast.columns)

weather_actual.head()
power_actual.head()
weather_actual.datetime_local.tail()
power_actual.tail()

datetime = pd.to_datetime(power_actual.datetime)
datetime2 = pd.to_datetime(weather_actual.datetime_local)

for i in range(1, len(datetime)):
    if((datetime[i] - datetime[i-1]).seconds/60 != 15):
        print(i)

missing_hours = []

for i in range(1, len(datetime2)):
    if((datetime2[i] - datetime2[i-1]).days >= 1):
        missing_hours.append(i)

(datetime2[3744] - datetime2[3743]).seconds/3600
(datetime2[3600] - datetime2[3599]).seconds/3600
(datetime2[3600] - datetime2[3599]).days*24

datetime3 = pd.to_datetime(weather_forecast.datetime_local)
for i in range(1, len(datetime3)):
    if((datetime3[i] - datetime3[i-1]).seconds > 3600):
        missing_hours.append(i)


# Weather actual has some data missing

weather_actual.max()
weather_forecast.max()
weather_forecast.isnull().sum()

weather_actual.cloud_cover.min()
weather_actual.cloud_cover.value_counts().head()
cloud_cover_datetime = weather_actual[['datetime_local', 'cloud_cover']]
cloud_cover_datetime = cloud_cover_datetime[cloud_cover_datetime.cloud_cover != -9999]
cloud_cover_datetime.datetime_local = pd.to_datetime(cloud_cover_datetime.datetime_local)

plt.scatter(x = cloud_cover_datetime.index.to_list(), y = cloud_cover_datetime.cloud_cover.to_list())

for i in range(5, len(weather_actual)):
    if(weather_actual.cloud_cover[i] == -9999):
        mean = (weather_actual.cloud_cover[i-1] + weather_actual.cloud_cover[i-2] + weather_actual.cloud_cover[i-3] + weather_actual.cloud_cover[i - 4] + weather_actual.cloud_cover[i - 5])/5
        weather_actual.cloud_cover[i] = mean

weather_actual.precip_type.unique()
weather_forecast.precip_type.unique()

weather_actual.summary.unique()
weather_forecast.summary.unique()

weather_actual.icon.unique()
weather_forecast.icon.unique()

weather_actual = weather_actual.drop(['plant_id', 'datetime_utc', 'wind_chill', 'heat_index', 'qpf', 'snow', 'pop', 'fctcode', 'precip_accumulation', 'precip_type', 'sunrise', 'sunset', 'updated_at'], axis = 1)
weather_forecast = weather_forecast.drop(['plant_id', 'datetime_utc', 'wind_chill', 'heat_index', 'qpf', 'snow', 'pop', 'fctcode', 'precip_accumulation', 'precip_type', 'sunrise', 'sunset', 'updated_at'], axis = 1)
weather_actual.wind_gust.max()
weather_forecast.visibility.nunique()
weather_actual.visibility.max()
weather_actual.visibility.min()
weather_actual.precip_probability.max()

weather_actual.wind_bearing.max()
weather_forecast.wind_bearing.max()
weather_forecast.wind_bearing.min()
weather_actual.wind_bearing.value_counts().head()

weather_actual.wind_gust.value_counts().head()

weather_actual.to_csv("weather_actual_cleaned.csv")
weather_forecast.to_csv("weather_forecast_cleaned.csv")

weather_forecast_2 = pd.read_csv('weather_forecast_cleaned.csv')
weather_actual_2 = pd.read_csv('weather_actual_cleaned.csv')

weather_actual_2.datetime_local = pd.to_datetime(weather_actual_2.datetime_local)

weather_actual_3 = weather_actual_2.copy(deep = True)

n = len(weather_actual_3)
for i in range(n):
    if(weather_actual_3['datetime_local'][i].month != 9):
        weather_actual_3 = weather_actual_3.drop(i, axis = 0)

weather_actual_3 = weather_actual_3.reset_index()
