# Steps:
# 1. Take data from csvs into one variable
# 2. Setup data into test and training set
# 3. Create Model based on data
# 4. Add additional CSV's and associate correctly
from html.entities import name2codepoint
from pycaret.classification import *
import csv
import pandas as pd
from tkinter.filedialog import askopenfilenames

test_number = 0
result_lst = []
data_lst = []

def loadFiles():
    file_names = askopenfilenames(title="Select file", filetypes=[(
        "Data", ("*.csv"))])
    print(file_names)
    return file_names

def loadResults(filename, testnum):
    with open(filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            curr_row = {}
            curr_row["child_result"] = row["child_result"]
            if line_count == testnum:
                result_lst.append(curr_row)
            line_count += 1
        print(f'Processed {line_count} lines.')

def loadData(filename):
    with open(filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        curr_row = {}
        filenames = []
        for row in csv_reader:
            filenames.append(row["Filename"])
            curr_row["num_changes"] = row["total number of files changed for diff"]
            line_count += 1
        curr_row["Filename"] = filenames
        data_lst.append(curr_row)
        print(f'Processed {line_count} lines.')


file_names = loadFiles()
for name in file_names:
    loadData(name)

file_names = loadFiles()
for name in file_names:
    loadResults(name, test_number)

for iterator in range(len(data_lst)):
    data_lst[iterator]['child_result'] = result_lst[iterator]['child_result']

dataset = pd.DataFrame(data_lst)

test = data_lst[0]


data = dataset.sample(frac=0.95, random_state=786)
data_unseen = dataset.drop(data.index)
data.reset_index(inplace=True, drop=True)
data_unseen.reset_index(inplace=True, drop=True)
print('Data for Modeling: ' + str(data.shape))
print('Unseen Data For Predictions: ' + str(data_unseen.shape))

s = setup(data, target = 'child_result', numeric_features= ['num_changes'])
numeric_features= ['num_changes']

rf = create_model('rf',fold=3)
print(rf)

tuned_rf = tune_model(rf, fold = 3)
print(tuned_rf)

predict_model(tuned_rf)

# plot_model(rf)

# best = compare_models()
# print(best)
# plot_model(best, plot = 'auc')
