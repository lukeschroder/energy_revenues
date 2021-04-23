import pandas as pd
import numpy as np

def train_test_split(df):
    
    test = df[df['DATAYEAR'] >= 2019]
    train = df[df['DATAYEAR'] < 2019]
    
    return train, test

def X_y_split(df):
    y = pd.Series(df['TOTALREVENUE']/df['TOTALSALES'])
    X = df.drop(columns=['TOTALREVENUE','TOTALSALES']).copy()
    return X, y

if __name__ == '__main__':

    data = pd.read_csv('../data/combined.csv')

    data['TOTALREVENUE'] = np.log(data['TOTALREVENUE'])
    data['TOTALSALES'] = np.log(data['TOTALSALES'])
    data['NAMEPLATECAPACITY(MW)'] = np.log(data['NAMEPLATECAPACITY(MW)'])

    train, test = train_test_split(data)

    X_train, y_train = X_y_split(train)
    X_test, y_test = X_y_split(test)

    X_train.to_csv('../data/X_train.csv',index=False)
    y_train.to_csv('../data/y_train.csv',index=False)
    X_test.to_csv('../data/X_test.csv',index=False)
    y_test.to_csv('../data/y_test.csv',index=False)