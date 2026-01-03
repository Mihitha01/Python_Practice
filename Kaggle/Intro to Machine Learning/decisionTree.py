# ===============================
# Exercise 5: Decision Tree - Full Script
# ===============================

import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Step 1: Load data
iowa_file_path = '../input/home-data-for-ml-course/train.csv'
home_data = pd.read_csv(iowa_file_path)

# Step 2: Define target and features
y = home_data.SalePrice
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF',
            'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
X = home_data[features]

# Step 3: Split into training and validation sets
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Step 4: Define helper function to compute MAE for a given max_leaf_nodes
def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=1)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return mae

# Step 5: Find the best max_leaf_nodes
candidate_max_leaf_nodes = [5, 25, 50, 100, 250, 500]
mae_values = {}
for leaf_size in candidate_max_leaf_nodes:
    mae_values[leaf_size] = get_mae(leaf_size, train_X, val_X, train_y, val_y)

best_tree_size = min(mae_values, key=mae_values.get)
print("Best max_leaf_nodes:", best_tree_size)
print("MAE at best size:", mae_values[best_tree_size])

# Step 6: Train final model on all data
final_model = DecisionTreeRegressor(max_leaf_nodes=best_tree_size, random_state=1)
final_model.fit(X, y)

# Step 7: Make validation predictions (optional)
val_predictions = final_model.predict(val_X)
val_mae = mean_absolute_error(val_y, val_predictions)
print("Validation MAE on split data:", val_mae)

# ===============================
# End of script — ready for GitHub
# ===============================
