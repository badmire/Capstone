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

final_set = dict()
final_set["test_name"] = []
final_set["result"] = []
final_set["machine_num"] = []
# final_set["average_score"] = []
final_set["version"] = []
final_set["total_change"] = []
final_set["total_add"] = []
final_set["total_del"] = []
final_set["total_fchange"] = []

for version, test in condensed_tests.items():
    for test_name, test_val in test.items():
        final_set["test_name"].append(test_name)

        # calculate average
        running_total = 0
        for test_case in test_val.tests:
            if test_case[0] == "passed":
                running_total += 1

        final_set["machine_num"].append(len(test_val.tests))
        # final_set["average_score"].append(running_total / len(test_val.tests))

        if round(running_total / len(test_val.tests)):
            final_set["result"].append(1)
        else:
            final_set["result"].append(0)

        # final_set["result"].append(test_val.tests[0][0])

        final_set["version"].append(version)
        final_set["total_change"].append(diffs[version]["total_change"])
        final_set["total_add"].append(diffs[version]["total_add"])
        final_set["total_del"].append(diffs[version]["total_del"])
        final_set["total_fchange"].append(diffs[version]["total_fchange"])


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
    numeric_features=[
        "total_change",
        "total_add",
        "total_del",
        # "average_score",
        "machine_num",
        "total_fchange",
    ],
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
