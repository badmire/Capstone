import csv
import sys

commit_hash = ""
bump_version = ""
output = []

if len(sys.argv) < 2:
    print("Must have arguments, pass -h for help")
    exit()
elif sys.argv[1] == "-h":
    print("1st argument == source, 2nd argument == destination")
    exit()

with open(sys.argv[1], "r") as target:
    for line in target.readlines():

        # Check for meta data and assign to globals for future use
        if line.split()[0] == "Bump":
            bump_version = line.split()[-1]
            continue
        elif line.split()[0] == "Commit":
            commit_hash = line.split()[1]
            continue
        elif line.split()[0] == "Changes" or line.split()[0] == "Summary":
            continue

        # Handle all regular rows assuming the format: blah ... blah *filepath* (diff)
        if line.split()[-1] != "(diff)":
            print("Unexpected format, exiting")
            print(f"problem with: {line}")
            exit(-1)
        else:
            current = line.split()[-2]
            ftype = ""

            if "." not in current.split("/")[-1]:
                ftype = "generic"
            else:
                ftype = current.split("/")[-1].split(".")[-1]

            # Append to list for later writing to csv
            output.append([current, ftype, commit_hash, bump_version])

with open(sys.argv[2], "w+", newline="") as out_target:
    csvwriter = csv.writer(out_target, delimiter=",", quotechar="|")
    csvwriter.writerow(["Filename", "file extension", "commit hash", "bump version"])

    for row in output:
        csvwriter.writerow(row)
