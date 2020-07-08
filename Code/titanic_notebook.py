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
# -

repo_directory = Path('D:\Kaggle\Titanic\Titanic_Repo')
code_path = repo_directory / 'Code'
data_path = repo_directory / 'Data'

df = pd.read_csv(data_path / 'train.csv')

df.info()

df.head()

df.describe()

training_example = training_proc(df,['Survived', 'Pclass', 'Fare'])
