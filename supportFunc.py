import random
import re
import csv
from tkinter.filedialog import askopenfilenames


def confidenceThreshold(prediction_list):
    """
    Take in a list of dictionaries stored as prediction_list and order it according to the following structure:
        1. All failed tests
        2. Confidence: low to high

    Each dictionary in the list has a key for “prediction” which is either the string “SUCCESS” or “FAILURE”. Each dictionary has a key for “confidence” which is a number 0-1. 1 being 100% confident and 0 being 0% confident.

    Sort the list to have all failed tests at the start of the list and then have the lowest confident tests next. The end of the list therefore has the highest confidence test prediction.

    return(sorted_prediction_list)

    """
    return sorted(prediction_list, key=lambda x: (x["prediction"], x["confidence"]))


def loadFiles(File_Type):
    # THIS FUNCTION NEEDS TO CHANGE TO ACCEPT A PATH W/O HUMAN INTERACTION
    # A command line argument perhaps?
    file_names = askopenfilenames(title="File_Type", filetypes=[("Data", ("*.csv"))])
    # print(file_names)
    return file_names


def versionMatch():
    """
    Take in path to a directory for diffs, and one for tests, return dictionary with diffs matched to test sets.

    """
    diffs = loadFiles("Diff csvs")
    tests = loadFiles("Test csvs")

    output = dict()
    for diff in diffs:
        # Each dictionary value is an array, [*path to diff*, [*array of paths to tests*]]
        output[re.findall("\d+_\d+_\d+_\d+", diff)[0]] = [diff, []]

    for test in tests:
        try:
            output[re.findall("\d+_\d+_\d+_\d+", test)[0]][1].append(test)
        except:  # If no match is found
            print(
                f"Path :{test}\n This path does not appear to be a file with correctly formatted version number in it's path."
            )
            continue

    return output


class TestStruct:
    def __init__(self, name):
        self.name = name
        self.current_score = -1
        # Array of tuples, one with result, one with machine, if any.
        self.tests = []
        # Historical pass fail rate, dummy value for now
        self.historical = 0.5

    def __eq__(self, other):
        if self.name == other:
            return True
        else:
            return False

    def __repr__(self):
        return f"TestStruct:{self.name}"


def condenseTests(vM_dict):
    """
    Take in matched set from versionMatch(), load into TestStruct for averaging

    vM_dict == versionMatch() return value

    return:
    {
        diff_version: [
            ["path/to/diff",[array/of/paths/to/tests]],
            {test_name: TestStruct}
        ]
    }
    """
    output = dict()

    for k, v in vM_dict.items():
        output[k] = [v, dict()]
        for test_csv in v[1]:
            with open(test_csv, "r") as csv_file:
                current = csv.DictReader(csv_file)
                for row in current:
                    if (
                        row["result"] == "skipped"
                    ):  # Don't let skipped test effect weight
                        continue

                    if row["test_name"] not in output:
                        # create new
                        output[k][1][row["test_name"]] = TestStruct(row["test_name"])
                    # update existing/give current values
                    if row["instrument_name"] is not None:
                        output[k][1][row["test_name"]].tests.append(
                            (row["result"], row["instrument_name"])
                        )
                    else:
                        output[k][1][row["test_name"]].tests.append(
                            (row["result"], None)
                        )
    return output


if __name__ == "__main__":
    from tkinter.filedialog import askopenfilenames

    # Informal test for versionMatch
    diffs_paths = askopenfilenames(title="Select file", filetypes=[("Data", ("*.csv"))])
    test_paths = askopenfilenames(title="Select file", filetypes=[("Data", ("*.csv"))])

    result = versionMatch(diffs_paths, test_paths)

    for k, v in result.items():
        print(k)
        print(f"diff: {v[0]}")
        for path in v[1]:
            print(f"    {path}")

    # # Informal test for confidenceThreshold
    # test_list = []
    # for i in range(50):
    #     test_list.append(
    #         {
    #             "prediction": "SUCCESS" if random.randint(0, 1) else "FAILURE",
    #             "confidence": random.random(),
    #         }
    #     )
    # result = confidenceThreshold(test_list)
    # for thing in result:
    #     print(thing)
