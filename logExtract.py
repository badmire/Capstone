from cgi import test
import csv
import sys

total_changes_diff = 0
total_insertions_diff = 0
total_deletions_diff = 0
total_touched_diff = 0
git_div_ver_diff = str()
output = []

if len(sys.argv) < 2:
    print("Must have arguments, pass -h for help")
    exit()
elif sys.argv[1] == "-h":
    print("1st argument == source")
    exit()

out_file = sys.argv[1].split("_diff")[0] + ".csv"
allLines = []

with open(sys.argv[1], "r") as target:
    allLines = []
    for line in target.readlines():
        allLines.append(line)

git_div_ver = allLines[0].split()[2]  # Git diff ver
total_changes_dif = allLines[-1].split()[0]  # Total changes for entire diff
# Total insertions for entire diff
total_insertions_dif = allLines[-1].split()[3]
# total deletions for entire diff
total_deletions_dif = allLines[-1].split()[5]

del allLines[0]
del allLines[-1]

total_touched_dif = len(allLines)  # Total number of files changed on diff

for line in allLines:
    current = []
    current_target = line.split()
    current.append(current_target[0])  # File name
    try:
        current.append(current_target[0].split(".")[1])  # File extension
    except:
        current.append("none")

    current.append(line.split("|")[1].count("+"))  # Total additions for file
    current.append(line.split("|")[1].count("-"))  # Total deletions for file
    current.append(current[-2] + current[-1])  # Total changes for file

    current.append(git_div_ver)
    current.append(total_changes_dif)
    current.append(total_insertions_dif)
    current.append(total_deletions_dif)
    current.append(total_touched_dif)

    output.append(current)

with open(out_file, "w", newline="") as out_target:
    csvwriter = csv.writer(out_target, delimiter=",", quotechar="|")
    csvwriter.writerow(
        [
            "Filename",
            "file extension",
            "total changes for file",
            "total additions for file",
            "total deletions for file",
            "diff ver",
            "total changes for diff",
            "total addtions for diff",
            "total deletions for diff",
            "total number of files changed for diff",
        ]
    )

    for row in output:
        csvwriter.writerow(row)
