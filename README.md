# Tektronix ML

Smart regression test selection through the power of machine learning.

## The Problem

Regression testing is part of any good software development cycle. It is critical to make sure that new additions do not break existing features, and equally important to let developers know as quickly as possible. What do you do when the regression testing suite becomes too large to run quickly for your developers, and your project too important to have errors? This is exactly the situation Tektronix found themselves in with a regression testing suite that takes 8+ hours to run overnight, and developers losing work to unknown mistakes and bugs.

## Our Solution: Smart Test Selection

Our solution to this particular problem is to leverage the power of machine learning to smartly select which of the tests are most likely to fail with a given change. Our model is built on the historical overnight test results as well as meta data from each code change. The model in the end produces a list of all of the tests, ranked by their likelihood of failure based on the incoming meta data of a code change. This allows the developers to run a small subset of the most risky tests, and be fairly confident that tests that are going to fail will be among them. The model is also designed to retrain itself automatically with each new nightly regression test, improving the overall accuracy and accounting for new tests and code changes.
(This is the description for the virtual presence)

## Getting Started

### Dependencies

- Python 3.6
- Pycaret 2.3.10
- Pandas

### Installing

Setup Environment:

pycaret requires python 3.6 to operate correctly

```
virtualenv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

### Docker Setup

Docker is required to use the Dockerfile

Perform the following in the same directory as the Dockerfile and the rest of the repository contents to build an image named 'model':
```
docker build -t model .
```

Perform the following to create a container named 'model_container' in interactive mode:
```
docker run -it --name model_container model
```

## Executing program

```
$ model.py -> [args]
```

First argument: 1, 2 or 0

- 1 = Make a new model
Second argument: path/to/diff/directory
Third argument: path/to/test/directory

optional flags:
-c name save model under specified name in the models directory

- 2 = Extract diffs
Second argument: /path/to/diff/directory
Third argument: /path/to/output/directory

- 0 = Use an old model
Second argument: path/to/target/diff.csv

optional flags:
-r  Changes behavior to target a raw diff txt
-c path/to/model Use to run a prediction against specified model .pkl file


### Example Usage:

Generate new model:

```
$ model.py 1 ./diffs ./tests
```

Generate new model with the name test:

```
$ model.py 1 ./diffs ./tests -c test
```

Generate predictions on a diff:

```
$ model.py 0 ./path/to/diff.csv 
```

Generate predictions on a diff with a specified model:

```
$ model.py 0 ./path/to/diff.csv -c /path/to/model
```

Process diffs for training and prediction

```
python model.py 2 ./in ./out
```
## Authors

- Brandon Admire (badmire4237@gmail.com)
- Alex Vogt (vogtalex@oregonstate.edu)
- Max Franz (maxfranz2@gmail.com)
- Evan Guenther (guenther.evan00@gmail.com)
- Akshat Lunia (luniaakshat@gmail.com)
