# Steps:
# 1. Take data from csvs into one variable
# 2. Setup data into test and training set
# 3. Create Model based on data
# 4. Add additional CSV's and associate correctly
from pycaret.classification import *
import pandas as pd
import sys

from supportFunc import *
from datetime import datetime


if (len(sys.argv) != 2):
    print("Please add the following command line option: ")
    print("0: Train (Create a new model)")
    print("1: Predict (Use old model to predict test outcomes)")
    sys.exit


newModel = False
model = []
target_data = []


if (sys.argv[1] == '1'):
    newModel = False
elif (sys.argv[1] == '0'):
    newModel = True

# Create the models folder if it doesn't exist
if not os.path.exists(os.getcwd()+"/models"):
    os.mkdir(os.getcwd()+"/models")

# Create the predictions folder if it doesn't exit
if not os.path.exists(os.getcwd()+"/predictions"):
    os.mkdir(os.getcwd()+"/predictions")

if newModel == False:
    model_names = loadFiles("Models")
    print("\n")
    print("\n")
    print("\n")
    print("Found ", len(model_names), " models: ")
    for model in model_names:
        print(model)
    os.chdir(os.getcwd() + "/models")
    print("Please enter the name of the model to be loaded: ")
    load_model_name = input()
    if ".pkl" in load_model_name:
        load_model_name = load_model_name.replace('.pkl', '')
    model = load_model(load_model_name)
    os.chdir("..")

if newModel == True:
    # Load and match diffs to tests
    result = versionMatch()

# Load and match diffs to tests
    result = versionMatch()

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

    target_data = dataset.sample(frac=0.95, random_state=786)
    data_unseen = dataset.drop(target_data.index)
    target_data.reset_index(inplace=True, drop=True)
    data_unseen.reset_index(inplace=True, drop=True)
    print("Data for Modeling: " + str(target_data.shape))
    print("Unseen Data For Predictions: " + str(data_unseen.shape))

    s = setup(
        target_data,
        target="result",
        numeric_features=numerical_tags,
        categorical_features=categorical_tags,
        silent=True,
        remove_perfect_collinearity=False
    )

    # Create Logitic regression model

    # best = compare_models()
    model = create_model("lr")


    # Else we have already loaded a model into the lr variable

    # ****************************
    # Tune and then save the model "lr" here:
    # ****************************

    print("Tuning the new model...")
    # lr = ensemble_model(best, method='Boosting', choose_better=True)
    model = tune_model(model)
    print("Sucessfully tuned model.")
    plot_model(model, save=True)
    os.chdir(os.getcwd() + "/models")
    print("Please enter the name of the model to be saved: ")
    model_name = input()
    save_model(model, model_name)
    os.chdir("..")

target_data = data_unseen

if (newModel == False):
    # Make target_data only use the new diff we are trying to analyse
    pass

# Predict
predictions = predict_model(lr, data=target_data)
os.chdir(os.getcwd()+"/predictions")
now = datetime.now()
dateString = str(now)
dateString = dateString[:16]
dateString = dateString.replace(':', '-')
predictionName = dateString+".csv"
print(predictionName)
predictions.to_csv(dateString+".csv")
os.chdir("..")
