def confidence_threshold(prediction_list):
    """
    Takes in a list of dictionaries stored as prediction_list and orders it according to the following structure: 
        1. All failed tests
        2. Confidence: low to high

    Each dictionary in the list has a key for “prediction” which is either the string “SUCCESS” or “FAILURE”. Each dictionary has a key for “confidence” which is a number 0-1. 1 being 100% confident and 0 being 0% confident. 

    Sort the list to have all failed tests at the start of the list and then have the lowest confident tests next. The end of the list therefore has the highest confidence test prediction.

    return(sorted_prediction_list)

    """
    pass
    # your code here


def versionMatch(diffs, tests):
    """
    Takes in an array of diff csv and an array of test csv, matches by version type, and returns dictionary object with matched key pairs.

    Each entry in the output dictionary is a key value pair, with the key the version type, and the value a tuple. The first item in the tuple will be the appropriate diff csv that matches the version. The second item in the tuple will be an array of all test result csv that match the version.

    """
    pass
    # your code here
