from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import sys

def evaluate(X_train,y_train,X_test):
    model = GradientBoostingRegressor(learning_rate=0.2,max_depth=9,min_samples_leaf=11
                                        ,max_features='auto',n_estimators=95,max_leaf_nodes=7)
    
    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)

    y_pred = np.e**y_pred
    print(y_pred)

    RMSE = mean_squared_error(y_test,y_pred,squared=False)

    return RMSE

if __name__ == '__main__':
    y_train = pd.read_csv('../data/y_train.csv')
    y_train = y_train['0']
    X_train = pd.read_csv('../data/X_train.csv')
    X_train = X_train.drop(columns=['TOTALCUSTOMERS','UTILITYNUMBER','DATAYEAR','MONTH'])

    y_test = pd.read_csv('../data/y_test.csv')
    y_test = y_test['0']
    X_test = pd.read_csv('../data/X_test.csv')
    X_test = X_test.drop(columns=['TOTALCUSTOMERS','UTILITYNUMBER','DATAYEAR','MONTH'])

    RMSE = evaluate(X_train,y_train,X_test)

    print(RMSE)