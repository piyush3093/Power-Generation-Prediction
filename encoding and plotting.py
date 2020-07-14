import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

weather_actual = pd.read_csv('weather_actual_cleaned.csv')
weather_forecast = pd.read_csv('weather_forecast_cleaned.csv')
power_actual = pd.read_csv('power_actual.csv')

weather_actual = weather_actual.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1)
weather_forecast = weather_forecast.drop('Unnamed: 0', axis = 1)

weather_actual.datetime_local = pd.to_datetime(weather_actual.datetime_local)
weather_forecast.datetime_local = pd.to_datetime(weather_forecast.datetime_local)

# Dropping Visibility as it doesn't contain Relevent Information
weather_actual = weather_actual.drop('visibility', axis = 1)
weather_forecast = weather_forecast.drop('visibility', axis = 1)

weather_forecast['month'] = [weather_forecast.datetime_local[i].month for i in range(0, len(weather_forecast))]
weather_forecast['time'] = [weather_forecast.datetime_local[i].hour for i in range(0, len(weather_forecast))]

weather_actual = weather_actual.drop('datetime_local')
weather_forecast = weather_forecast.drop('datetime_local')

power_actual.datetime = pd.to_datetime(power_actual.datetime)
power_actual['time'] = [x.hour for x in power_actual.datetime]
power_actual['month'] = [x.month for x in power_actual.datetime]
power_actual['date'] = [x.day for x in power_actual.datetime]
power_generated = power_actual.power.groupby([power_actual['time'], power_actual['month'], power_actual['date']]).first()

weather_actual_org = pd.read_csv('weather_actuals.csv')
weather_forecast_org = pd.read_csv('weather_forecast.csv')

weather_forecast['sunrise'] = pd.to_datetime(weather_forecast_org['sunrise'])
weather_forecast['sunset'] = pd.to_datetime(weather_forecast_org['sunset'])
weather_actual['sunrise'] = pd.to_datetime(weather_actual_org['sunrise'])
weather_actual['sunset'] = pd.to_datetime(weather_actual_org['sunset'])

n = len(weather_actual)
for i in range(0, n):
    if(weather_actual.time[i] <= 6):
        weather_actual = weather_actual.drop(i)
    elif(weather_actual.time[i] >= 18):
        weather_actual = weather_actual.drop(i)

weather_forecast['power_generated'] = np.nan
n = len(weather_forecast)
for i in range(0, n):
    if(weather_forecast.time[i] <= 6):
        weather_forecast.power_generated[i] = 0
    elif(weather_forecast.time[i] >= 18):
        weather_forecast.power_generated[i] = 0

weather_actual['power_generated'] = np.nan
weather_actual['date'] = [x.day for x in weather_actual.datetime_local]
weather_actual = weather_actual.reset_index()

for i in range(0, len(weather_actual)):
    weather_actual['power_generated'][i] = power_generated[weather_actual.time[i]][weather_actual.month[i]][weather_actual.date[i]]

weather_actual = weather_actual.drop(['sunrise', 'sunset'], axis = 1)
weather_actual = weather_actual.drop(['month', 'date'], axis = 1)
weather_forecast = weather_forecast.drop('sunrise', axis = 1)
weather_actual = weather_actual.drop('datetime_local', axis = 1)
weather_forecast = weather_forecast.drop('datetime_local', axis = 1)
weather_forecast = weather_forecast.reset_index(drop = True)
weather_forecast = weather_forecast.drop('month', axis = 1)
weather_actual = weather_actual.drop('index', axis = 1)

data_corr = weather_actual.corr()
weather_pred = weather_forecast.power_generated
weather_forecast = weather_forecast.drop('power_generated', axis = 1)
weather_forecast['power_generated'] = weather_pred

#encoding the categorical variable

def encoding(dataset, feature_to_encode):
    dummies = pd.get_dummies(dataset[feature_to_encode], drop_first = True)
    dataset = dataset.drop([feature_to_encode], axis = 1)
    dataset = pd.concat([dataset, dummies], axis = 1)
    return dataset, dummies

total_data = pd.concat((weather_actual, weather_forecast), axis = 0)

total_data, dummy = encoding(total_data, 'icon')
total_data, dummy = encoding(total_data, 'time')
total_data, dummy = encoding(total_data, 'summary')

# Plotting all the variables
sns.distplot(a = total_data.cloud_cover)
sns.distplot(a = total_data.apparent_temperature)
sns.distplot(a = total_data.dew_point)
sns.distplot(a = total_data.wind_bearing)
sns.distplot(a = total_data.ozone)
sns.distplot(a = total_data.precip_intensity)
sns.distplot(a = total_data.precip_probability)

total_data.to_csv('total_data_cleaned.csv')



