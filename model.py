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
condensed_tests = condenseTests(result)

print(f"number of diffs: {len(condensed_tests)}")

# Load diffs/features
diffs = loadDiffs(result)

# Build final dict for data frame
# df_dict = dict()
# for version, values in diffs.items():  # Iterate through each version
#     df_dict[version] = dict()
#     for k, v in values.items():  # Load in features
#         df_dict[version][k] = v

#     for testk, testv in condensed_tests[version][
#         1
#     ].items():  # Iterate through each test
#         # Calculate average pass/fail score
#         running_total = 0
#         for test_case in testv.tests:
#             if test_case[0] == "passed":
#                 running_total += 1

#         df_dict[version][testv.name] = dict()

#         df_dict[version][testv.name]["num_of_machines"] = len(testv.tests)
#         df_dict[version][testv.name]["average_score"] = running_total / len(testv.tests)
#         if round(df_dict[version][testv.name]["average_score"]):
#             df_dict[version][testv.name]["result"] = "passed"
#         else:
#             df_dict[version][testv.name]["result"] = "failed"

dataset = []

for version, test in condensed_tests.items():
    current = dict()
    current[test] = dict()
    for testk, testv in test.items():
        running_total = 0
        for test_case in testv.tests:
            if test_case[0] == "passed":
                running_total += 1

        current[testv.name]["num_of_machines"] = len(testv.tests)
        current[testv.name]["average_score"] = running_total / len(testv.tests)
        if round(current[testv.name]["average_score"]):
            current[testv.name]["result"] = "passed"
        else:
            current[testv.name]["result"] = "failed"

    dataset.append(current)

print(dataset)

print("*************************************")
print("***Processing done, starting model***")
print("*************************************")


dataset = pd.DataFrame(df_dict)

data = dataset.sample(frac=0.95, random_state=786)
data_unseen = dataset.drop(data.index)
data.reset_index(inplace=True, drop=True)
data_unseen.reset_index(inplace=True, drop=True)
print("Data for Modeling: " + str(data.shape))
print("Unseen Data For Predictions: " + str(data_unseen.shape))

s = setup(
    data,
    target="result",
    numeric_features=[
        "total_change",
        "total_add",
        "total_del",
        "total_fchange",
        "file_change",
        "file_add",
        "file_del",
        "average_score",
        "num_of_machines",
    ],
    categorical_features=["result", "name", "extension"],
)

rf = create_model("rf", fold=3)
print(rf)

tuned_rf = tune_model(rf, fold=3)
print(tuned_rf)

predict_model(tuned_rf)

plot_model(rf)

# best = compare_models()
# print(best)
# plot_model(best, plot = 'auc')
