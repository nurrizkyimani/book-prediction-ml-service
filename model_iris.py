import numpy as np
import pandas as pd


# import train test split from sklearn
from sklearn.model_selection import train_test_split

# import LinearRegression form sklearn
from sklearn.linear_model import LinearRegression

import pickle
import requests
import json

# read Salary_Data file from csv
dataset = pd.read_csv('./Salary_Data.csv')
X = dataset.iloc[:, :-1].values
Y = dataset.iloc[:, 1].values

# split data into train and test with test size 0.3
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=0)

# create model with linearRegression
regressor = LinearRegression()
regressor.fit(X_train, Y_train)
y_pred = regressor.predict(X_test)

# dump the pickle in file model with 'wb'
pickle.dump(regressor, open('model.pkl', 'wb'))
