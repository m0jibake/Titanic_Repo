# This is an auxiliary file to import python modules and packages into a jupyter notebook
# Calling this file by '%run ./dependencies' in the jupyter notebook does the respective job

import os
import pandas as pd
import numpy as np
import random
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from pandas.plotting import scatter_matrix

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier#
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_val_score

from jupyterthemes import jtplot
jtplot.style(theme='chesterish', context='notebook', ticks=True, grid=False)

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from scipy.stats import randint as sp_randint
