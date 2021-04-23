from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import sys


def random_search(model, X_train, y_train, feature_dict, n_trials,folds=5,scoring={'RMSE':'neg_root_mean_squared_error','R2': 'r2'}):
    '''
    Random searches for best model hyperparams

    Args:
        model (sklearn model): model to test
        X_train (numpy array): train dataset
        y_train (numpy array): train target values
        feature_dict (dictionary): dictionary of features to test as keys and ranges as values
        n_trials (int): number of iterations to search
        folds (int): number of cross validation folds to preform
        scoring (string): scoring metric for search

    Returns:
        df (pandas dataframe): dataframe of best features sorted by best recall score
    '''
    rs = RandomizedSearchCV(model,feature_dict,
                             n_jobs=-1, verbose=True,
                             cv=folds, scoring=scoring,
                             return_train_score=False,
                             n_iter=n_trials,
                             refit='RMSE')
    
    rs.fit(X_train, y_train)

    cols = list(feature_dict.keys())
    out_cols = ['param_' + x for x in cols]
    out_cols.extend(['mean_test_RMSE','mean_test_R2'])

    df = pd.DataFrame(rs.cv_results_)[out_cols]
    df = df.sort_values(['mean_test_RMSE'],ascending=False)

    return df

def grid_search(model, X_train, y_train, feature_dict, n_trials,folds=5,scoring={'RMSE':'neg_root_mean_squared_error','R2': 'r2'}):
    '''
    Grid searches for best model hyperparams

    Args:
        model (sklearn model): model to test
        X_train (numpy array): train dataset
        y_train (numpy array): train target values
        feature_dict (dictionary): dictionary of features to test as keys and ranges as values
        n_trials (int): number of iterations to search
        folds (int): number of cross validation folds to preform
        scoring (string): scoring metric for search

    Returns:
        df (pandas dataframe): dataframe of best features sorted by best recall score
    '''
    gs = GridSearchCV(model,feature_dict,
                             n_jobs=-1, verbose=True,
                             cv=folds, scoring=scoring,
                             return_train_score=False,
                             refit='RMSE')

    gs.fit(X_train, y_train)

    cols = list(feature_dict.keys())
    out_cols = ['param_' + x for x in cols]
    out_cols.extend(['mean_test_RMSE','mean_test_R2'])

    df = pd.DataFrame(gs.cv_results_)[out_cols]
    df = df.sort_values(['mean_test_RMSE'],ascending=False)

    return df
      

if __name__ == '__main__':
    ### BEGIN DATA LOADING
    
    y_train = pd.read_csv('../data/y_train.csv')
    y_train = y_train['0']
    X_train = pd.read_csv('../data/X_train.csv')

    y_test = pd.read_csv('../data/y_test.csv')
    y_test = y_test['0']
    X_test = pd.read_csv('../data/X_test.csv')



    ### END DATA LOADING ###



    ### BEGIN RANDSEARCH ###

    # gradient_boosting_grid = {'learning_rate': [0.1, 1],
    #                   'max_depth': [2,8],
    #                   'min_samples_leaf': [1,10],
    #                   'max_features': ['auto', 'sqrt', 'log2'],
    #                   'n_estimators': [20, 150, 200]}

    gradient_boosting_grid = {'learning_rate': [0.1, 0.2, 1],
                'n_estimators':list(np.arange(10,100,5)),
                'max_depth':list(np.arange(1,16,1)),
                'min_samples_split': list(np.arange(2,16,1)),
                'min_samples_leaf': list(np.arange(2,16,1)),
                'max_features':['auto','sqrt','log2'],
                'max_leaf_nodes': list(np.arange(2,8,1))}

    model = GradientBoostingRegressor()

    rf_grid = {'n_estimators':list(np.arange(10,100,5)),
                'max_depth':list(np.arange(1,16,1)),
                'min_samples_split': list(np.arange(2,16,1)),
                'min_samples_leaf': list(np.arange(2,16,1)),
                'max_features':['auto','sqrt','log2'],
                'max_leaf_nodes': list(np.arange(2,8,1))}

    model1 = RandomForestRegressor()

    print(random_search(model,X_train,y_train,gradient_boosting_grid,folds=5,n_trials=500).head(15))
    # print(random_search(model1,X_train,y_train,rf_grid,folds=5,n_trials=80).head(10))

    ### END GRIDSEARCH ###



    ### BEGIN RANDOM TESTING ###############################################

    # gradient_boosting_grid = {'learning_rate': [0.2, 0.1],
    #                 'max_depth': [9,11],
    #                 'min_samples_leaf': [8,12,15],
    #                 'max_features': ['auto'],
    #                 'n_estimators': [95,115,150],
    #                 'max_leaf_nodes': [6,8]}


    # model = GradientBoostingRegressor()

    # # model1 = RandomForestRegressor()

    # print(grid_search(model,X_train,y_train,gradient_boosting_grid,n_trials=200).head(10))

    ### END RANDOM TESTING ##################################################