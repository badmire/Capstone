import csv

from black import out
from supportFunc import *


class TestStruct:
    def __init__(self, name, result, machine):
        self.name = name
        self.current_score = result
        self.test_num = 1
        self.machines = [machine]
        self.historical = 0.5

    def __eq__(self, other):
        if self.name == other:
            return True
        else:
            return False


if __name__ == "__main__":
    matched_sets = versionMatch()
    output = dict()

    for k, v in matched_sets.items():
        output[k] = [v, dict()]
        for test_csv in v[1]:
            with open(test_csv, "r") as csv_file:
                current = csv.reader(csv_file)
                for row in current:
                    result = 0
                    if current["result"] == "skipped":
                        continue
                    else:
                        if current["result"] == "passed":
                            result = 1
                    if current["test_name"] not in output[k][1]:
                        output[k][1][current["test_name"]] = TestStruct(
                            current["test_name"], result, current["instrument_name"]
                        )
                    else:
                        pass  #
