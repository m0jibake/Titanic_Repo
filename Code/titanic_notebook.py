# %matplotlib inline
# %run ./dependencies.py
# %run ./utility_functions.py

pd.set_option('display.max_columns', 500)
# -

repo_directory = Path('D:\Kaggle\Titanic\Titanic_Repo')
code_path = repo_directory / 'Code'
data_path = repo_directory / 'Data'

df = pd.read_csv(data_path / 'train.csv')

df.head()

df.describe()
