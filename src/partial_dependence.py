from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.inspection import partial_dependence, plot_partial_dependence
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



if __name__ == '__main__':
    y_train = pd.read_csv('../data/y_train.csv')
    y_train = y_train['0']
    X_train = pd.read_csv('../data/X_train.csv')
    X_train = X_train.drop(columns=['TOTALCUSTOMERS','UTILITYNUMBER'])

    y_test = pd.read_csv('../data/y_test.csv')
    y_test = y_test['0']
    X_test = pd.read_csv('../data/X_test.csv')
    X_test = X_test.drop(columns=['TOTALCUSTOMERS','UTILITYNUMBER'])

    model = GradientBoostingRegressor(learning_rate=0.2,max_depth=9,min_samples_leaf=11
                                        ,max_features='auto',n_estimators=95,max_leaf_nodes=7)
    
    model.fit(X_train,y_train)

    print(X_train.columns)
    fig, ax = plt.subplots(figsize=(18,18))
    my_plots = plot_partial_dependence(model,       
                                   features=[20,21,22], # column numbers of plots we want to show
                                   X=X_train,            # raw predictors data.
                                   feature_names=list(X_train.columns), # labels on graphs
                                   grid_resolution=100,
                                   percentiles=(.01,.99),
                                   ax=ax) # number of values to plot on x axis

    plt.show()
    # plt.savefig('../images/partial_dependence_nuke.png',dpi=60)