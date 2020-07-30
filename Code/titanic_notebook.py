# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %matplotlib inline
# %run ./dependencies.py
# %run ./utility_functions.py

pd.set_option('display.max_columns', 500)

repo_directory = Path('D:\Kaggle\Titanic_Repo')
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
# -

#Encode Sex and Embarked variables
df_train = encode_categorical_vars(df_train, ['Sex', 'Embarked'])
#Set mean for 'NaN' fields in Age
df_train['Age'].fillna(df_train['Age'].mean(), inplace = True)

#mutiplied Age gives different accuracy
df_train['Age_multiplied'] = df_train['Age']/1000

df_train.head(10)

# + active=""
# All pre-processing done? Then proceed with the training procedure
#
# Sample usage (copy the following line in a new cell):
# training_example = training_proc(df_train,['Survived', 'Pclass', 'Fare'])
# -

#Standard train
training_example = training_proc(df_train,['Survived', 'Pclass', 'Age','Fare', 'Sex_female', 'Sex_male', 
                                           'Embarked_C', 'Embarked_Q', 'Embarked_S'])

#Experimental train with multiplied Age
training_example = training_proc(df_train,['Survived', 'Pclass', 'Age_multiplied','Fare', 
                                           'Sex_female', 'Sex_male', 'Embarked_C', 'Embarked_Q', 'Embarked_S'])

# + active=""
# Apply the fitted estimators to the test data
#
# Sample usage:
# test_proc(df_test, ['Survived', 'Pclass', 'Fare'], training_example)
