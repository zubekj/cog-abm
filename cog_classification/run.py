import argparse
import json

import sys
sys.path.append('../../')
sys.path.append('../')
sys.path.append('')

import pandas as pd
import numpy as np

from sklearn import tree
from sklearn import neighbors

from cog_classification.steels_classifier.steels_classifier import SteelsClassifierExtended


def add_arguments(pars):

    pars.add_argument('-c', '--classifier_file', dest='classifier_file', action='store', required=True,
                      help='Name of file with all parameters of classifier.')

    pars.add_argument('-t', '--task_file', dest='task_file', action='store', required=True,
                      help='Name of file with all parameters of classifier\'s task.')

    pars.add_argument('-o', '--output_file', dest='output_file', action='store', required=True,
                      help='Name of file where results of simulation will be stored.')

    pars.add_argument('-a', '--alpha', dest='alpha', action='store', default=0.99, type=float,
                      help='How fast agents forget. Values from 0 (total sclerosis) to 1 (perfect memory).')

    pars.add_argument('-t', '--threshold', dest='threshold', action='store', default=0.95, type=float,
                      help="The threshold which affects generation of new categories. "
                           "Value from 0 (as rarely as possible) to 1 (always).")

def load_dataset(filename):
    """
    Loads a data set from UCI file. All non-numerical columns are factorized.
    Optional auxilary file contains list of columns not used in machine
    learning. First index on the list should point class column. If auxilary
    file is not present, the last column is treated as class.

    :returns: * X -- matrix containing values of all attributes.
        * Y -- vector containing class values.

    Method from https://bitbucket.org/zubekj/selection_ensembles.
    """
    try:
        with open('{0}.class'.format(filename)) as f:
            columns_to_skip = [int(c) for c in f.readline().split(" ")]
    except (IOError, ValueError) as e:
        columns_to_skip = [-1]

    df = pd.read_csv(filename, header=None)
    X = [pd.factorize(df[col])[0] if df[col].dtype.kind == 'O' else df[col] for col in df]

    Y = np.array(X[columns_to_skip[0]])
    X = [f for i, f in enumerate(X) if not (i in columns_to_skip or (i-len(X)) in columns_to_skip)]

    return np.array(X, dtype=float).T, Y

def make_classifiers(classifiers_names):

    def make_classifier(classifier_name):
        return {"Tree": tree.DecisionTreeClassifier(),
                "Knn": neighbors.KNeighborsClassifier(n_neighbors=1)
                }.get(classifier_name)

    classifiers = []

    for name in classifiers_names:
        classifiers.append(make_classifier(name))

    return classifiers

def parse(classifier_source, task_source=None):
    classifiers = make_classifiers(classifier_source["classifiers"])
    return SteelsClassifierExtended(classifiers, alpha=task_source['alpha'])


def run_task(classifier_source, task_source):

    classifier = parse(classifier_source, task_source)

    samples, classes = load_dataset(task_source["data"])

    return classifier.get_results(samples, classes)

def run(classifier_file, task_file, alpha, threshold):
    with open(classifier_file, 'r') as f:
        classifier_source = json.loads(f.read())

    with open(task_file, 'r') as f:
        task_source = json.loads(f.read())

    if 'alpha' not in task_source:
        task_source['alpha'] = alpha

    if 'threshold' not in task_source:
        task_source['threshold'] = threshold

    return run_task(classifier_source, task_source)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This program is implementation of Steels classifier.")
    add_arguments(parser)
    args = parser.parse_args()

    with open(args.output_file, 'w') as f:
        json.dump(run(args.classifier_file, args.task_file, args.alpha, args.threshold), f)
