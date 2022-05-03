# Steps:
# 1. Take data from csvs into one variable
# 2. Setup data into test and training set
# 3. Create Model based on data
# 4. Add additional CSV's and associate correctly
from pycaret.classification import *
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

# Currently possible tags:
# From diffs:
# "total_change", "total_add", "total_del", "total_fchange",
# From tests:
# "child_link","parent_test_chain","child_result","parent_link","parent_start_date","sw_version","result","run_time","error_message","instrument_name","instrument_git_hash","run_date","collection_date","dut_console_log","is_system_test","connection_type","visa_name","test_git_hash","ptf_git_hash","test_log_file","test_name","test_requirements","test_description","scenario_number","expected_skipped_models","linked_issues_snapshot","seed"
# Misc:
# "historic"

# Special:
# "fchange"

numerical_tags = ["total_change", "total_add", "total_del", "total_fchange"]

categorical_tags = []

# For tags that produce more columns or have special logic
special_tags = ["fchange"]

final_set = tableCreate(
    numerical_tags + categorical_tags + special_tags, tests, diffs)

# Adjust which columns to include here
if "fchange" in special_tags:
    file_names = fileChange(diffs)
    for file in file_names:
        numerical_tags.append(f"{file}_change")
        numerical_tags.append(f"{file}_del")
        numerical_tags.append(f"{file}_add")
        categorical_tags.append(f"{file}_name")
        categorical_tags.append(f"{file}_extension")

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
    remove_perfect_collinearity=False
)

# Create Logitic regression model
dt = create_model("dt")

# Display AUC accuracy curves
plot_model(dt)

# ****************************
# Save the model "lr" here:
# ****************************


# ****************************
# Code that takes a while to load but eventually want to use for higher accuracy:
# ****************************

# best = compare_models()
# print(best)
# boosted_dt = ensemble_model(dt, method = 'Bagging')
# predictions = predict_model(boosted_dt)
# predictions.head()
# plot_model(boosted_dt)
# evaluate_model(boosted_dt)
# unseen_predictions = predict_model(boosted_dt, data=data_unseen)
# unseen_predictions.head()
# predictions.to_csv("newpredictions.csv")

# tuned_lr = tune_model(lr)
# predictions = predict_model(tuned_lr)
# plot_model(tuned_lr)
# evaluate_model(tuned_lr)
# final_lr = finalize_model(tuned_lr)
# print(final_lr)
# plot_model(final_lr)
