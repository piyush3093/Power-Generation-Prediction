# Model Development
# Model Development and Feature Selection

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

total_data = pd.read_csv('total_data_cleaned.csv')
total_data = total_data.drop('Unnamed: 0', axis = 1)

columns = [i for i in range(0, 48) if i != 13]
X_train = total_data.iloc[:6242, columns]
X_test = total_data.iloc[6242:, columns]
y_train = total_data.iloc[:6242, 13]
y_train = y_train.values

# Selecting Best Features
# Dividing the variables as categorical and continous

X_train_cat = pd.concat((X_train.iloc[:, 3], X_train.iloc[:, 13:]), axis = 1)
X_test_cat = pd.concat((X_test.iloc[:, 3], X_test.iloc[:, 13:]), axis = 1)
X_train_cont = pd.concat((X_train.iloc[:, :3], X_train.iloc[:, 4:13]), axis = 1)
X_test_cont = pd.concat((X_test.iloc[:, :3], X_test.iloc[:, 4:13]), axis = 1)

from sklearn.feature_selection import f_regression, SelectKBest
s = SelectKBest(score_func = f_regression, k = 11)
s.fit(X_train_cont, y_train)
scores = s.scores_
X_train_cont = s.transform(X_train_cont)
X_test_cont = s.transform(X_test_cont)

from sklearn.feature_selection import f_classif
s = SelectKBest(score_func = f_classif, k = 20)
s.fit(X_train_cat, y_train)
scores = s.scores_
X_train_cat = s.transform(X_train_cat)
X_test_cat = s.transform(X_test_cat)

X_test = np.concatenate((X_test_cont, X_test_cat), axis = 1)
X_train = np.concatenate((X_train_cont, X_train_cat), axis = 1)

# normalizing the data
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
sc_y = StandardScaler()

X_train_sc = sc_X.fit_transform(X_train)
y_train_sc = sc_y.fit_transform(y_train.values.reshape((-1, 1)))
X_test_sc = sc_X.transform(X_test)

# Model development
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train_sc, y_train_sc)

from sklearn.svm import SVR
regressor = SVR(kernel = 'rbf')
regressor.fit(X_train_sc, y_train_sc)

from xgboost import XGBRegressor
regressor = XGBRegressor()
regressor.fit(X_train_sc, y_train_sc)

from lightgbm import LGBMRegressor
regressor = LGBMRegressor()
regressor.fit(X_train_sc, y_train_sc)

# Model Testing

from sklearn.model_selection import cross_val_score
scores = cross_val_score(estimator = regressor, X = X_train_sc, y = y_train_sc, cv = 5, scoring = 'neg_root_mean_squared_error')
scores.mean()

#linear_model = 0.760
#SVM = 0.775
# XGBoost = 0.755
#LightGBM = 0.774

y_pred = regressor.predict(X_test_sc)
y_pred = sc_y.inverse_transform(y_pred)

weather_forecast_2 = pd.read_csv('weather_forecast.csv')
weather_forecast_2.datetime_local = pd.to_datetime(weather_forecast_2.datetime_local)

Solution = pd.DataFrame(weather_forecast_2.datetime_local)
Solution['power_generated'] = np.nan

j = 0
i = 0
while(j < 297 and i < 648):
    if(Solution.datetime_local[i].hour <= 6 or Solution.datetime_local[i].hour >= 18):
        Solution.power_generated[i] = 0
    else:
        Solution.power_generated[i] = y_pred[j]
        j+=1
    i+=1

Solution.to_csv('Power_Generated.csv')


