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

repo_directory = Path('D:\Kaggle\Titanic_Repo')
code_path = repo_directory / 'Code'
data_path = repo_directory / 'Data'

df = pd.read_csv(data_path / 'train.csv')

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

#Encode Sex and Embarked variables
df_train = encode_categorical_vars(df_train, ['Sex', 'Embarked'])
#Set mean for 'NaN' fields in Age
df_train['Age'].fillna(df_train['Age'].mean(), inplace = True)

#mutiplied Age gives different accuracy
df_train['Age_multiplied'] = df_train['Age']/1000

df_train.head(10)

df_train['Deck'] = df_train["Cabin"].str[0]

df_train.head(20)

df_train['Deck'].unique()

df_train['Deck'].fillna('Z', inplace=True)

# Apparently there is one person with Deck 'T', which seems to be an error on the Data. Replace by 'Z'.
df_train.loc[df_train['Deck']=='T', 'Deck'] = 'Z'

df_train = encode_categorical_vars(df_train, ['Deck'])

df_train.drop('Deck', axis=1, inplace=True)

df_train.head()

df_train['fam_size'] = df_train['SibSp'] + df_train['Parch']

df_train['travels_alone'] = 0
df_train['travels_alone'] = df_train['fam_size'].apply(lambda x: 1 if x==0 else 0)

df_train.head()

df_train['Title'] = df_train['Name'].str.split(",", n = 1, expand = True)[1].str.split(' ', n=2, expand=True)[1] 


def rare_title(x):
    if x not in ['Mr.', 'Miss.', 'Mrs.', 'Master.']:
        return 'Rare'
    return x


df_train['Title'] = df_train['Title'].apply(rare_title)

df_train

# + active=""
#

# + active=""
# All pre-processing done? Then proceed with the training procedure
#
# Sample usage (copy the following line in a new cell):
# training_example = training_proc(df_train,['Survived', 'Pclass', 'Fare'])
# -

#Standard train
training_example = training_proc(df_train,['Survived', 'Pclass', 'Age','Fare', 'Sex_female', 'Sex_male', 
                                           'Embarked_C', 'Embarked_Q', 'Embarked_S', 'Deck_A', 'Deck_B', 'Deck_C', 'Deck_D', 'Deck_E', 'Deck_F', 'Deck_G',
                                          'fam_size', 'travels_alone'])

training_example

#Experimental train with multiplied Age
training_example = training_proc(df_train,['Survived', 'Pclass','Fare', 
                                           'Sex_female', 'Sex_male', 'Embarked_C', 'Embarked_Q', 'Embarked_S'])

# + active=""
# Apply the fitted estimators to the test data
#
# Sample usage:
# test_proc(df_test, ['Survived', 'Pclass', 'Fare'], training_example)
