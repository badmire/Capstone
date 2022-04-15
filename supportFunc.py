import random
import re
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


def versionMatch(diff_dir, test_dir):
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
