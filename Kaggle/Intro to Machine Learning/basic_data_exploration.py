import pandas as pd

melbourne_file_path = 'data/melb_data.csv'

melbourne_data = pd.read_csv('data/melb_data.csv')

melbourne_data.describe()

print(melbourne_data.head())