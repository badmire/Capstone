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
- Pycaret
- Pandas

### Installing

Setup Environment:

```
virtualenv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

## Executing program

```
$ model.py -> [args]
```

First argument: 0 or 1

- 0 = Make a new model
- 1 = Use an old model

Second argument: path/to/diff/directory

Third argument: path/to/test/directory

### Flags:

Specify path to save model to or load model from

```
-c path/to/a/model
```

Tell app to use a processed diff rather than a raw diff

```
-p
```

### Example Usage:

Generate new model:

```
$ model.py 0 ./diffs ./tests
```

Generate tests on new data:

```
$ model.py 1 ./diffs ./tests -c path/to/a/model
```

Generate tests on new data with pre-processed diff:

```
$ model.py 1 ./diffs ./tests -c path/to/a/model -p
```

## Authors

- Brandon Admire (badmire4237@gmail.com)
- Alex Vogt (vogtalex@oregonstate.edu)
- Max Franz (maxfranz2@gmail.com)
- Evan Guenther (guenther.evan00@gmail.com)
- Akshat Lunia (luniaakshat@gmail.com)
