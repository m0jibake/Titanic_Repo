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
pd.set_option('display.max_rows', 500)

# +
#Testing Area

data_test = {'Sex': ['male', 'female', 'male', 'male'], 'Name': ['a', 'b', 'c', 'a']}
df_test = pd.DataFrame.from_dict(data_test)
#df_test['Sex'].isnull().sum()
df_test.head()

if df_test['Sex'].isnull().values.any() == True:
    print('\nWarning: tetsttest')

df_test = encode_categorical_vars(df_test, ['Sex', 'Name'])

df_test['Sex'].nunique()



df_test.head()
# -

repo_directory = Path('D:\Kaggle\Titanic_Repo')
code_path = repo_directory / 'Code'
data_path = repo_directory / 'Data'

df_train = pd.read_csv(data_path / 'train.csv')

df.info()

df.head(80)

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

#Encode Embarked variables
df_train = encode_categorical_vars(df_train, ['Sex', 'Embarked'])
#Set mean for 'NaN' fields in Age
df_train['Age'].fillna(df_train['Age'].mean(), inplace = True)

# Title
df_train['Title'] = df_train['Name'].str.split(",", n = 1, expand = True)[1].str.split(' ', n=2, expand=True)[1]
df_train['Title'] = df_train['Title'].apply(rare_title)


# Total family size
df_train['fam_size'] = df_train['SibSp'] + df_train['Parch']

# Travels alone (binary)
df_train['travels_alone'] = 0
df_train['travels_alone'] = df_train['fam_size'].apply(lambda x: 1 if x==0 else 0)

df_train.head(10)

# Deck
df_train['Deck'] = df_train["Cabin"].str[0]
df_train['Deck'].unique()

df_train['Deck'].fillna('Z', inplace=True)

# Apparently there is one person with Deck 'T', which seems to be an error on the Data. Replace by 'Z'.
df_train.loc[df_train['Deck']=='T', 'Deck'] = 'Z'

#Encode Sex and Embarked variables
df_train = encode_categorical_vars(df_train, ['Sex', 'Embarked', 'Title', 'Deck'])
#Set mean for 'NaN' fields in Age
df_train['Age'].fillna(df_train['Age'].mean(), inplace = True)

df_train.head()

# create a list which contains the relevant features. For this purpose, create first a list of all non-relevant features
drop_those_features = ['PassengerId', 'Name', 'Sex', 'SibSp', 'Parch', 'Ticket', 'Cabin', 'Embarked', 'Title', 'Deck']
features = df_train.columns.tolist()
features = [e for e in features if e not in drop_those_features]

# + active=""
# All pre-processing done? Then proceed with the training procedure
#
# Sample usage (copy the following line in a new cell):
# training_example = training_proc(df_train,['Survived', 'Pclass', 'Fare'])
# -

#Standard train
training_example = training_proc(df_train, features)

training_example

#Experimental train with multiplied Age
training_example = training_proc(df_train,['Survived', 'Pclass','Fare',
                                           'Sex_female', 'Sex_male', 'Embarked_C', 'Embarked_Q', 'Embarked_S'])

# + active=""
# Apply the fitted estimators to the test data
#
# Sample usage:
# test_proc(df_test, ['Survived', 'Pclass', 'Fare'], training_example)
# -

df_test = pd.read_csv(data_path / 'test.csv')

# Title
df_test['Title'] = df_test['Name'].str.split(",", n = 1, expand = True)[1].str.split(' ', n=2, expand=True)[1]
df_test['Title'] = df_test['Title'].apply(rare_title)

# Total family size
df_test['fam_size'] = df_test['SibSp'] + df_test['Parch']

# Travels alone (binary)
df_test['travels_alone'] = 0
df_test['travels_alone'] = df_test['fam_size'].apply(lambda x: 1 if x==0 else 0)

# Deck
df_test['Deck'] = df_test["Cabin"].str[0]
df_test['Deck'].unique()

df_test['Deck'].fillna('Z', inplace=True)

#Encode Sex and Embarked variables
df_test = encode_categorical_vars(df_test, ['Sex', 'Embarked', 'Title', 'Deck'])
#Set mean for 'NaN' fields in Age
df_test['Age'].fillna(df_train['Age'].mean(), inplace = True)
df_test['Fare'].fillna(df_train['Fare'].mean(), inplace = True)

# create a list which contains the relevant features. For this purpose, create first a list of all non-relevant features
drop_those_features = ['PassengerId', 'Name', 'Sex', 'SibSp', 'Parch', 'Ticket', 'Cabin', 'Embarked', 'Title', 'Deck']
features = df_test.columns.tolist()
features = [e for e in features if e not in drop_those_features]

df_test['Fare'] = df_test['Fare'].fillna(df_train['Fare'].mean())

df_test[features][df_test[features].isna().any(axis=1)]

pred = training_example[0].predict(df_test[features])

test_submission = pd.DataFrame({'PassengerId': df_test['PassengerId'], 'Survived': pred})

test_submission.to_csv(data_path / 'test_submission.csv', index=False)

test_submission
