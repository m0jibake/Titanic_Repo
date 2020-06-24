# This is an auxiliary file to import custom functions into a jupyter notebook
# Calling this file by '%run ./utility_functions.py' in the jupyter notebook does the respective job

def split_training_set(data, rel_test_size):
    np.random.seed(42)
    abs_test_size = int(rel_test_size*data.shape[0])
    random_indices = np.random.permutation(data.shape[0])
    test_indices = random_indices[:abs_test_size]
    training_indices = random_indices[abs_test_size:]
    test_set = data.iloc[test_indices]
    training_set = data.iloc[training_indices]
    return pd.DataFrame(test_set, columns = data.columns), pd.DataFrame(training_set, columns = data.columns)
