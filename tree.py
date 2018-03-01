#!/usr/bin/python


import os
import pydot
import sys

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def usage(program):
    print 'Usage: {} league'.format(program)


if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        sys.exit(1)

    #training = pd.read_csv('./data/' + sys.argv[1] + '_training.csv')
    table = pd.read_csv('./data/' + sys.argv[1] + '_overlap.csv')

    
    features = list(table.columns[2:-1])
    target = list(table.columns[-1:])[0]

    X_train, X_test, y_train, y_test = train_test_split(table[features], table[target], random_state=1)

    dt = DecisionTreeClassifier(criterion='entropy', max_depth=3)
    dt = dt.fit(X_train, y_train)

    # output a PNG of the decision tree
    dotfile = 'AAA.dot'
    png = 'AAA.png'

    export_graphviz(dt, out_file=dotfile, feature_names=features)
    (tree, ) = pydot.graph_from_dot_file(dotfile)
    tree.write_png(png)

    # test
    y_predict = dt.predict(X_test)
    
    print accuracy_score(y_test, y_predict)

