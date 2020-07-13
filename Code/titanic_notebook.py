# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %matplotlib inline
# %run ./dependencies.py
# %run ./utility_functions.py

pd.set_option('display.max_columns', 500)

repo_directory = Path('D:\Kaggle\Titanic\Titanic_Repo')
code_path = repo_directory / 'Code'
data_path = repo_directory / 'Data'

df = pd.read_csv(data_path / 'train.csv')

df.info()

df.head()

df.describe()

# + active=""
# Split the whole available data into a training set and a test set. Do not involve the test set in the training procedure, but apply pre-processing (i.e. get rid of missing values, encode categorical variables, etc.)
# -

df_train, df_test = split_training_set(df, 0.1)
print('The training data contains {0} columns and {1} rows'.format(df_train.shape[1], df_train.shape[0]))
print('The test data contains {0} columns and {1} rows'.format(df_test.shape[1], df_test.shape[0]))

# + active=""
# Pre-Processing
#
# The following utility functions may be applied: 
# encode_categorical_vars() --- to transform categorical variables to numerical ones via the dummy variable approach

# + active=""
# All pre-processing done? Then proceed with the training procedure
#
# Sample usage (copy the following line in a new cell):
# training_example = training_proc(df_train,['Survived', 'Pclass', 'Fare'])

# + active=""
# Apply the fitted estimators to the test data
#
# Sample usage:
# test_proc(df_test, ['Survived', 'Pclass', 'Fare'], training_example)
