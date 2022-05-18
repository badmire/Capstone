# Steps:
# 1. Take data from csvs into one variable
# 2. Setup data into test and training set
# 3. Create Model based on data
# 4. Add additional CSV's and associate correctly

from pycaret.classification import *
import sys

from model_funcs import *
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
    createNewModel("./diffs","./tests")


if (newModel == False):
    # function currently a placeholder
    forcastPredictions("path/to/diff",model)



# Predict
# predictions = predict_model(model, data=target_data)
# os.chdir(os.getcwd()+"/predictions")
# now = datetime.now()
# dateString = str(now)
# dateString = dateString[:16]
# dateString = dateString.replace(':', '-')
# predictionName = dateString+".csv"
# print(predictionName)
# predictions.to_csv(dateString+".csv")
# os.chdir("..")
