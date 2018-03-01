#!/usr/bin/python


import os
import pydot
import sys

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score


def usage(program):
    print 'Usage: {} league'.format(program)


if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        sys.exit(1)

    training = pd.read_csv('./data/' + sys.argv[1] + '_training.csv')
            
    
    features = list(training.columns[3:-1])
    target = list(training.columns[-1:])[0]

    dt = DecisionTreeClassifier(criterion='entropy', max_depth=3)
    dt = dt.fit(training[features], training[target])

    # output a PNG of the decision tree
    dotfile = 'AAA.dot'
    png = 'AAA.png'

    export_graphviz(dt, out_file=dotfile, feature_names=features)
    (tree, ) = pydot.graph_from_dot_file(dotfile)
    tree.write_png(png)

    # test
    testing = pd.read_csv('./data/' + sys.argv[1] + '_testing.csv')
    predict_Y = dt.predict(testing[features])
    
    print accuracy_score(testing[target], predict_Y)

