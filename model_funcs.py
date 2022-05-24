
from pycaret.classification import *
from supportFunc import *
import shutil
import re
import datetime
import csv

numerical_tags = ["total_change", "total_add", "total_del", "total_fchange"]

categorical_tags = []

special_tags = ["fchange"]


def createNewModel(diff_path,test_path,model_save):
    """Creates new model to be saved.
    -diff_path and test_path should just point at a directory full of 
    diffs and tests respecivly. diffs should be processed in advance 
    via the extractLogs().
    
    -model_save is the name the model should be saved as without extension.
    Defaults to "current_model"
    """
    # Create table for modeling
    dataset = createPandasFrame(numerical_tags,categorical_tags,special_tags,diff_path,test_path)

    target_data = dataset.sample(frac=0.95, random_state=245)
    data_unseen = dataset.drop(target_data.index)
    target_data.reset_index(inplace=True, drop=True)
    data_unseen.reset_index(inplace=True, drop=True)
    print("Data for Modeling: " + str(target_data.shape))
    print("Unseen Data For Predictions: " + str(data_unseen.shape))

    # Setup preprocessing
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
    best_models = compare_models(include = ['dt', 'ada', 'ridge', 'lr', 'nb', 'svm', 'rf', 'lightgbm', 'dummy', 'knn'], n_select = 3)

    # ****************************
    # Tune and then save the model:
    # ****************************

    print("Tuning the new model...")
    model = blend_models(estimator_list = best_models)
    print("Sucessfully tuned model.")

    save_model(model, model_save)
    # plot_model(model, save=True)
    shutil.move(f"./{model_save}.pkl",f"./models/{model_save}.pkl")

def forcastPredictions(target_diff_path,model_path):
    """Uses existing model to make predictions.
    Two sets of predictions are produced. The full output of the model is saved
    in the ./predictions directory as a csv, and a condensed, sorted version in
    the ./output directory, also as a csv. In both cases, they are saved using
    the current time stamp.

    Uses the default "current_model" that is saved in the ./models directory,

    can specify a different model to use with the model_path parameter.

    -target_diff_path is the path to a csv diff file that has been processed 
    with extractLogs()

    """
    # Load the model
    os.chdir("./models")
    model = load_model(model_path)
    os.chdir("..")
    # Construct list of expected column heads by the model
    headers =  model.named_steps['dtypes'].final_training_columns

    # Simulate functionality of the versionMatch function for a single, targeted, diff.
    target = dict()

    target[re.findall("\d+_\d+_\d+_\d+", target_diff_path)[0]] = [target_diff_path, []]

    version = list(target.keys())[0]

    # Load the diff into a familar format
    diff = loadDiffs(target)

    # Strip off a layer of dict
    diff = next(iter(diff.values()))

    # Build a list of tests from historical test results
    test_lib = [line.rstrip() for line in open('./test_lib.txt')]

    final_set = dict()

    for header in headers:
        final_set[header] = []

    for test in test_lib:
        final_set['test_name'].append(test)
        final_set['version'].append(version)

        # Iterate through all required headers and fill in value
        for key in final_set.keys():
            if key == "test_name": # Skip test_name
                continue
            if key == "version":
                continue
            # When value is known
            if key in diff:
                final_set[key].append(diff[key])
                continue
            else:
                #Check for nested file type info
                if key[key.rfind("_"):] in ["_extension","_change","_del","_add"]: # Skip extras after file name
                    continue
                if key[key.rfind("_"):] == "_name":
                    if key[:key.rfind("_")] in diff["files"]:
                        final_set[key].append(1)
                        final_set[key[:key.rfind("_")]+"_extension"].append(diff["files"][key[:key.rfind("_")]]["extension"])
                        final_set[key[:key.rfind("_")]+"_change"].append(diff["files"][key[:key.rfind("_")]]["file_change"])
                        final_set[key[:key.rfind("_")]+"_del"].append(diff["files"][key[:key.rfind("_")]]["file_del"])
                        final_set[key[:key.rfind("_")]+"_add"].append(diff["files"][key[:key.rfind("_")]]["file_add"])
                    else:
                        final_set[key].append(0)
                        final_set[key[:key.rfind("_")]+"_extension"].append(0)
                        final_set[key[:key.rfind("_")]+"_change"].append(0)
                        final_set[key[:key.rfind("_")]+"_del"].append(0)
                        final_set[key[:key.rfind("_")]+"_add"].append(0)
                else: # File not present in diff, set to null
                    final_set[key].append(0)

    print("Building dataframe...")
    target_data = pd.DataFrame(final_set)

    target_data.to_csv("./target_data.csv")
    print("done")


    # Finally, make prediction/forcast
    predictions = predict_model(model, data=target_data)

    test_names = predictions['test_name'].tolist()
    results = predictions['Label'].tolist()
    scores = predictions['Score'].tolist()

    zipper = zip(test_names,results,scores)
    output = sorted(zipper,key=lambda x: (x[1],x[2]*-1))

    os.chdir(os.getcwd()+"/predictions")
    now = datetime.datetime.now()
    dateString = str(now)
    dateString = dateString[:16]
    dateString = dateString.replace(':', '-')
    predictionName = dateString+".csv"
    print(predictionName)
    predictions.to_csv(dateString+".csv")
    os.chdir("..")

    # Save output to csv
    with open(f"./output/output-{str(now).replace(':','-')}.csv","w",newline='') as target_file:
        writer = csv.writer(target_file)
        writer.writerow(["test_name","Label","Score"])
        writer.writerows(output)

    return output
    



