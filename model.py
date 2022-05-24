# Steps:
# 1. Take data from csvs into one variable
# 2. Setup data into test and training set
# 3. Create Model based on data
# 4. Add additional CSV's and associate correctly

from pycaret.classification import *
import sys
import argparse

from model_funcs import *
from supportFunc import *
from datetime import datetime


parser = argparse.ArgumentParser(description='Apply PyCaret ML to a set of tests and diffs.')
parser.add_argument('--p', '--processed', action='store_true', help='Tell the program to load processed diffs rather than raw diffs.')
parser.add_argument('--c', '--custom_model_name', help='Tell the program to load or save a PyCaret model with a unique name. Models are saved in the models directory.')
parser.add_argument('new_model_option', choices=[0, 1], type=int, help='0: Create a new PyCaret model. 1: Load an existing model.')
args = parser.parse_args()

newModel = False
doProcessed = False
modelName = "current_model"



# argparse handles invalid options
if (args.new_model_option == 0):
    newModel = True
elif (args.new_model_option == 1):
    newModel = False

if (args.p is not None):
    doProcessed = True

if (args.c is not None):
    modelName = args.c




model = []
target_data = []



# Create the models folder if it doesn't exist
if not os.path.exists(os.getcwd()+"/models"):
    os.mkdir(os.getcwd()+"/models")

# Create the predictions folder if it doesn't exit
if not os.path.exists(os.getcwd()+"/predictions"):
    os.mkdir(os.getcwd()+"/predictions")

# Create the output folder if it doesn't exit
if not os.path.exists(os.getcwd()+"/output"):
    os.mkdir(os.getcwd()+"/output")

if newModel == True:
    createNewModel("./diffs","./tests",modelName)


if (newModel == False):
    output = forcastPredictions("./data_unseen/v1_41_8_930.csv",modelName,doProcessed)


    # for final in output:
    #     print(final)



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
