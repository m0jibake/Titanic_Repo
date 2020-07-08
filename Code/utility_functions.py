# This is an auxiliary file to import custom functions into a jupyter notebook
# Calling this file by '%run ./utility_functions.py' in the jupyter notebook does the respective job

from dependencies import *

def split_training_set(data, rel_test_size):
    np.random.seed(42)
    abs_test_size = int(rel_test_size*data.shape[0])
    random_indices = np.random.permutation(data.shape[0])
    test_indices = random_indices[:abs_test_size]
    training_indices = random_indices[abs_test_size:]
    test_set = data.iloc[test_indices]
    training_set = data.iloc[training_indices]
    return pd.DataFrame(test_set, columns = data.columns), pd.DataFrame(training_set, columns = data.columns)


def report_results(results, n_top=1, metric='Accuracy'):
    """
    A function to evaluate classifiers returned by a grid or randomized search.

    INPUT PARAMETERS:
    results --- RandomizedSearchCV().cv_results_ or GridSearchCV().cv_results_
    n_top --- Number of top n models
    metric --- Determines according to what metric the models should be ranked. Possible parameters:
    Accuracy, Precision, Recall, F1 Score, AUC
    """
    try:
        for n in range(1,n_top+1):
            indices = (np.flatnonzero(results['rank_test_score']==n))
            for index in indices:
                print('Model with rank {0}'.format(n))
                print('Mean Accuracy score: {0:.4f} (sd: {1:.4f})'.format(float(results['mean_test_score'][index]),
                     float(results['std_test_score'][index])))
    except:
        print("Model rank criterion: {0}".format(metric))
        print("")
        for n in range(1,n_top+1):
            indices = (np.flatnonzero(results['rank_test_{0}'.format(metric)]==n))
            for index in indices:
                print('Model with rank {0}'.format(n))
                print('Mean Accuracy score: {0:.4f} (sd: {1:.4f})'.format(float(results['mean_test_Accuracy'][index]),
                     float(results['std_test_Accuracy'][index])))
                print('Mean Precision score: {0:.4f} (sd: {1:.4f})'.format(float(results['mean_test_Precision'][index]),
                     float(results['std_test_Precision'][index])))
                print('Mean Recall score: {0:.4f} (sd: {1:.4f})'.format(float(results['mean_test_Recall'][index]),
                     float(results['std_test_Recall'][index])))
                print('Mean F1 score: {0:.4f} (sd: {1:.4f})'.format(float(results['mean_test_F1 Score'][index]),
                     float(results['std_test_F1 Score'][index])))
                print('Mean AUC score: {0:.4f} (sd: {1:.4f})'.format(float(results['mean_test_AUC'][index]),
                     float(results['std_test_AUC'][index])))
                print('Parameters: {0}'.format(results['params'][index]))
                print('---------------------------------------------------------------------------------------------------------------------------')



def training_proc(df,features):
    '''
    This function performs a training routine for a Gradient Boosting Machine (xgBoost), a Random Forest and an Artificial Neural Network.

    INPUT PARAMETERS:
    df --- a pd.dataframe
    features --- the columns of the dataframe which should serve as the predictors. Provide as a list, i.e. ['feature1', 'feature2', ...]

    RETURN OBJECT
    a list containing three items, in particular the best performing estimator for each algorithm. 
    '''

    # check if df is a pd.DataFrame
    if not isinstance(df[features], pd.DataFrame):
        return print('Error: df is not of type pd.DataFrame.')

    # check if columns of df are of type string
    str_vars = list(df[features].dtypes[df[features].dtypes == np.object].index)
    if len(str_vars) > 0:
        return print('Error: The following columns contain Strings: {0}. \n Please remove Strings from the dataframe.'.format(str_vars))

    # check for missing values
    mv_tbl = df[features].isnull().sum()
    if mv_tbl.sum() > 0:
        return print('Error: There are missing values in your dataframe. The columns and number of missing values is: \n\n{0} \
        \n\nIf you want to display the rows with missing values, execute df[df.isnull().any(axis=1)] '.format(pd.DataFrame(mv_tbl[mv_tbl>0], columns=['Count'])))

    # checks are done
    print('Your dataframe is formally correct. Continue with the training routine.\n\n')

    y_train = df['Survived']
    X_train = df[features].drop(columns=['Survived'], axis=1)

    # training routine
    xgBoost_dist = {
        'learning_rate': [0.1, 0.01, 0.5],
        'max_depth':range(3,10,2),
        'min_child_weight':range(1,6,2),
        'gamma':[i/10.0 for i in range(0,5)],
        'subsample':[i/10.0 for i in range(6,10)],
        'reg_alpha':[1e-5, 1e-2, 0.1, 1, 100]
        }

    rf_dist = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [50, 100, 200, None],
        'min_samples_split': sp_randint(2, 20),
        'min_samples_leaf': sp_randint(1, 20),
        #'max_features': sp_randint(2, X_train.shape[1]),
        'max_leaf_nodes': [100, 500, 1000, 10000, None],
        'min_impurity_decrease': [0, 0.0001, 0.001, 0.01, 0.1],
        'class_weight': [None]
        }

    ann_dist = {
        'hidden_layer_sizes': [10,100,300,1000],
        'alpha': [0.0001, 0.001, 0.01, 0.1]
        }

    rand_cv_xgBoost = RandomizedSearchCV(estimator=XGBClassifier(), param_distributions=xgBoost_dist, n_iter=10, cv=3, refit=True, return_train_score=True, random_state=42)
    rand_cv_xgBoost_fitted = rand_cv_xgBoost.fit(X_train, y_train)
    print('XgBoost:')
    report_results(rand_cv_xgBoost_fitted.cv_results_)




    rand_cv_rf = RandomizedSearchCV(estimator=RandomForestClassifier(n_estimators=100, random_state=42), param_distributions=rf_dist, n_iter=10, cv=3, refit=True, return_train_score=True, random_state=42)
    rand_cv_rf_fitted = rand_cv_rf.fit(X_train, y_train)
    print('\nRandom Forest:')
    report_results(rand_cv_rf_fitted.cv_results_)

    rand_cv_ann = RandomizedSearchCV(estimator=MLPClassifier(early_stopping=True, random_state=42), param_distributions=ann_dist, n_iter=10, cv=3, refit=True, return_train_score=True, random_state=42)
    rand_cv_ann_fitted = rand_cv_ann.fit(X_train, y_train)
    print('\nANN:')
    report_results(rand_cv_ann_fitted.cv_results_)

    return list([rand_cv_xgBoost_fitted.best_estimator_, rand_cv_rf_fitted.best_estimator_, rand_cv_ann_fitted.best_estimator_])
