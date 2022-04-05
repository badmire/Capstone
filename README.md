# Capstone

Setup Environment:

1. virtualenv myenv
2. myenv\Scripts\activate
3. pip install -r requirements.txt

How to Use:

1. Run logExtract.py on designated git_diff data
2. Run model.py
3. Select Processed Diff files
4. Select Corresponding test results

Thing to work on:

1. Associate diffs with correct tests
2. Ensure specific test is the same across all data
3. Change model from a binary predictor to something that analyzes confidence
4. Run on all tests
5. Change logExtract.py to effect multiple files at once
