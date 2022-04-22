# Steps:
# 1. Take data from csvs into one variable
# 2. Setup data into test and training set
# 3. Create Model based on data
# 4. Add additional CSV's and associate correctly
from html.entities import name2codepoint
from pycaret.classification import *
import csv
import pandas as pd
from supportFunc import *

# ****************************
# **Brandon Fuck-around zone**
# ****************************

# Load and match diffs to tests
result = versionMatch()

# Load tests and condense them into TestStruct class
tests = readTests(result)

# Load diffs/features
diffs = loadDiffs(result)

numerical_tags = ["total_change", "total_add", "total_del", "total_fchange"]

categorical_tags = []

final_set = tableCreate(numerical_tags + categorical_tags, tests, diffs)

print("*************************************")
print("***Processing done, starting model***")
print("*************************************")


dataset = pd.DataFrame(final_set)

data = dataset.sample(frac=0.95, random_state=786)
data_unseen = dataset.drop(data.index)
data.reset_index(inplace=True, drop=True)
data_unseen.reset_index(inplace=True, drop=True)
print("Data for Modeling: " + str(data.shape))
print("Unseen Data For Predictions: " + str(data_unseen.shape))

s = setup(
    data,
    target="result",
    numeric_features=numerical_tags,
    categorical_features=categorical_tags,
    silent=True,
)

rf = create_model("rf", fold=3)
print(rf)

tuned_rf = tune_model(rf, fold=3)
print(tuned_rf)

predict_model(tuned_rf)

plot_model(rf)

best = compare_models()
print(best)
plot_model(best, plot="auc")
