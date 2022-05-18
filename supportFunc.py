import re
import csv
import time
import os
import pandas as pd



def tableCreate(tags, tests, diffs):
    """
    Take in an array of tags, tests, and diffs, and output a dict in the format for a pd.Dataframe

    All preproccessing/value calculation is assumed to be completed at this point.
    Function will attempt to navigate all keys and subkeys to find each tag.
    If a tag is not found, an error will be thrown, and execution stopped.

    Final output will be a dict where each key is a tag, and each value an array. Each index in the array
    will corespond with a test_name and result provided by the "tests" dict parameter.
    """
    output = dict()

    output["test_name"] = []
    output["result"] = []
    output["version"] = []

    # Conditional values
    historic = dict()
    if "historic" in tags:
        historic = historicRecord(tests)

    file_names = []
    if "fchange" in tags:
        file_names = fileChange(diffs)
        for file in file_names:
            output[f"{file}_name"] = []
            output[f"{file}_extension"] = []
            output[f"{file}_change"] = []
            output[f"{file}_del"] = []
            output[f"{file}_add"] = []

    # Build columns
    for tag in tags:
        if tag not in output:
            if tag == "historic" or tag == "fchange":
                continue
            output[tag] = []

    # Build rows
    for version in tests:
        for test in tests[version]:

            # hard coded required info
            output["test_name"].append(tests[version][test]["test_name"])
            output["result"].append(tests[version][test]["result"])
            output["version"].append(version)

            # Load in passed tags, assumes no nested values
            for tag in tags:
                if tag in diffs[version]:
                    output[tag].append(diffs[version][tag])
                elif tag in tests[version][test]:
                    output[tag].append(tests[version][test][tag])
                if tag == "historic":
                    output["historic"] = historic[test]
                # Add changed files as features
                if tag == "fchange":
                    for file in file_names:
                        if file in diffs[version]["files"]:
                            output[f"{file}_change"].append(
                                diffs[version]["files"][file]["file_change"]
                            )
                            output[f"{file}_del"].append(
                                diffs[version]["files"][file]["file_del"]
                            )
                            output[f"{file}_add"].append(
                                diffs[version]["files"][file]["file_add"]
                            )
                            output[f"{file}_name"].append(1)
                            output[f"{file}_extension"].append(1)
                        else:
                            output[f"{file}_name"].append(0)
                            output[f"{file}_extension"].append("N/A")
                            output[f"{file}_change"].append(0)
                            output[f"{file}_del"].append(0)
                            output[f"{file}_add"].append(0)

    return output


def fileChange(diffs):
    """Take in array of diff dicts, return list of all changed files in given diffs"""
    output = []
    for version in diffs:
        for file in diffs[version]["files"]:
            if file not in output:
                output.append(file)

    return output


def historicRecord(tests):
    """Take in dict of tests of the format from the readTests() function, for each test calculate historic fail rate, return dict.

    Calculates historic pass/fail rate over all tests results.

    Output dict has keys of each testname, and value of the fail rate
    """
    output = dict()

    for version in tests:
        for test in tests[version]:
            if test in output:  # Add pass/fail to output under test heading.
                if test[version][test]["result"] == "pass":
                    output[test].append(1)
                else:
                    output[test].append(0)
            else:  # Creat new entry in output for the test
                if test[version][test]["result"] == "pass":
                    output[test] = [1]
                else:
                    output[test] = [0]

    # Build averages and output
    for k, v in output.items():
        tmp = 0
        for value in v:
            tmp += value

        # Calculate average
        tmp = tmp / len(v)

        # Overwrite output
        output[k] = tmp

    return output


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


def loadFiles(target_dir):
    """Takes in directory, returns list of paths to all files in that directory."""

    file_paths = []

    for file in os.scandir(target_dir):
        file_paths.append(file.path)

    return file_paths


def versionMatch(diff_dir_path, test_dir_path):
    """
    Take in path to a directory for diffs, and one for tests, return dictionary with diffs matched to test sets.
    {diff vers: [diff vers path, [test paths,test paths]]}

    """
    diffs = loadFiles(diff_dir_path)
    tests = loadFiles(test_dir_path)

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


def log_err(text, target_path):
    with open(target_path, "a") as target:
        target.write(str(time.localtime(time.time()) + "    " + text))


def readTests(vM_dict):
    """
    Take in versionMatch() dict, load all data fields from from each test into output dict, organized by version.

    Skipping untested/skipped tests coupled with indexing tests by scenario number yields no duplicate
    tests in a given version at this time.

    Output will be a dictionary.
    Each key will be the version number, and each value will be a dictionary.
    Each key will be a test number, each value will be a dictionary
    Each key will be a coulumn name, each value will be the value from the csv.
    """
    output = dict()

    # Record keeping for injested tests.
    test_lib_file = open("./test_lib.txt","w+")
    test_lib = test_lib_file.readlines()

    lines_processed = 0
    for k, v in vM_dict.items():
        output[k] = dict()
        for test_csv in v[1]:
            with open(test_csv, "r", encoding="utf8") as csv_file:
                current = csv.DictReader(csv_file)
                for row in current:
                    lines_processed += 1
                    # Don't let skipped test effect weight
                    if row["result"] == "skipped" or row["result"] == "untested":
                        continue
                    if (  # Some tests run multiple times with different scenarios
                        str(row["test_name"] + "_" + row["scenario_number"])
                        not in output[k]
                    ):
                        output[k][row["test_name"]] = dict()

                        # Keep a running list of all tests in database for long term use
                        test_lib = list(set(test_lib + [row["test_name"]]))
                    else:
                        log_err(
                            f"Error, duplicate: {row['test_name']} already in use. Version {k}, {test_csv}",
                            "./readTestsLog.txt",
                        )
                    # Injest all columns for ease of later use.
                    for title, value in row.items():
                        output[k][row["test_name"]][title] = value
        print(f"Lines processed: {lines_processed}")

    # Write test library for later use
    for line in test_lib:
        line = line + '\n'
        test_lib_file.write(line)
    test_lib_file.close()

    return output


def loadDiffs(vM_dict):
    """
    Take in matched set from version match, output diffs info dict with version as k, dict as value.

    Each value has this format:
    total_change
    total_add
    total_del
    total_fchange
    files : array of dicts
        name
        extension
        file_change
        file_add
        file_del
    """
    output = dict()

    for k, v in vM_dict.items():
        current = dict()
        with open(v[0], "r", encoding="utf8") as target:
            diff = csv.DictReader(target)
            file_changes = []

            for row in diff:
                current["total_change"] = row["total changes for diff"]
                current["total_add"] = row["total addtions for diff"]
                current["total_del"] = row["total deletions for diff"]
                current["total_fchange"] = row["total number of files changed for diff"]
                current_file = dict()
                current_file["name"] = row["Filename"]
                current_file["extension"] = row["file extension"]
                current_file["file_change"] = row["total changes for file"]
                current_file["file_add"] = row["total additions for file"]
                current_file["file_del"] = row["total deletions for file"]
                file_changes.append(current_file)

            current["files"] = dict()
            for file in file_changes:
                current["files"][file["name"]] = file

            output[k] = current

    return output

def createPandasFrame(numerical_tags, categorical_tags, special_tags,diff_path,test_path):
    """Create the pandas data frame needed for the model
    
    Currently possible tags:
    From diffs:
    "total_change", "total_add", "total_del", "total_fchange",
    From tests:
    "child_link","parent_test_chain","child_result","parent_link","parent_start_date","sw_version","result","run_time","error_message","instrument_name","instrument_git_hash","run_date","collection_date","dut_console_log","is_system_test","connection_type","visa_name","test_git_hash","ptf_git_hash","test_log_file","test_name","test_requirements","test_description","scenario_number","expected_skipped_models","linked_issues_snapshot","seed"
    Misc:
    "historic"

    Special:
    "fchange"
    """
    # Load and match diffs to tests
    result = versionMatch(diff_path,test_path)

    # Load tests and condense them into TestStruct class
    tests = readTests(result)

    # Load diffs/features
    diffs = loadDiffs(result)





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
    
    return pd.DataFrame(final_set)


if __name__ == "__main__":
    # Informal test for historical

    files = versionMatch("./diffs","./tests")

    diffs = loadDiffs(files)
    tests = readTests(files)

    output = tableCreate(["fchange"], tests, diffs)
