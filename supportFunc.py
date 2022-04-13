import random
import re


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


def versionMatch(diffs, tests):
    """
    Takes in an array of diff csv and an array of test csv, matches by version type, and returns dictionary object with matched key pairs.

    Each entry in the output dictionary is a key value pair, with the key the version type, and the value a tuple. The first item in the tuple will be the appropriate diff csv that matches the version. The second item in the tuple will be an array of all test result csv that match the version.

    """
    output = {}
    for diff in diffs:
        # Each dictionary value is an array, [*path to diff*, [*array of paths to tests*]]
        output[re.findall("\d+_\d+_\d+_\d+", diff)[0]] = [diff, []]

    for test in tests:
        try:
            output[re.findall("\d+_\d+_\d+_\d+", test)[0]][1].append(test)
        except:  # If no match is found
            print(
                f"{test} does not appear to be a file with correctly formatted version number in it's path."
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