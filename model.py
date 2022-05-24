from pycaret.classification import *
import argparse
import sys
from model_funcs import *
from supportFunc import *



parser = argparse.ArgumentParser(description='Apply PyCaret ML to a set of tests and diffs.')
parser.add_argument('--r', '--raw', action='store_true', help='Tell the program to load raw diff rather than processed diff.')
parser.add_argument('--c', '--custom_model_name', help='Tell the program to load or save a PyCaret model with a unique name. Models are saved in the models directory.')
parser.add_argument('new_model_option', choices=[0, 1], type=int, help='1: Create a new PyCaret model. 0: Load an existing model.')
parser.add_argument('diffs_path_arg', help='Specify the path to the diffs.')

if (int(sys.argv[1])):
    parser.add_argument('tests_path_arg', help='Specify the path to the tests.')
args = parser.parse_args()

newModel = args.new_model_option
do_raw_diff = False
modelName = "current_model"

if (args.r is not None):
    do_raw_diff = True

if (args.c is not None):
    modelName = args.c

diffPath = args.diffs_path_arg




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

if newModel:
    testPath = args.tests_path_arg
    createNewModel(diffPath,testPath,modelName)
else:
    if (do_raw_diff):
        os.mkdir(os.getcwd()+"/tmp")
        shutil.copy(diffPath,os.getcwd()+"/tmp")
        extractLogs(os.getcwd()+"/tmp",os.getcwd()+"/tmp")
        diffPath = [x for x in os.scandir(os.getcwd()+"/tmp") if ".csv" in x.name][0].path

    output = forcastPredictions(diffPath,modelName)

    if (do_raw_diff):
        shutil.rmtree(os.getcwd()+"/tmp")




