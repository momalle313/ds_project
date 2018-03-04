#!/usr/bin/python


import os
import pydot
import sys

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

def usage(program):
    print 'Usage: {} league'.format(program)


if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        sys.exit(1)

    table_ordinal = pd.read_csv('./data/' + sys.argv[1] + '_overlap_ordinal.csv')
    table_numeric = pd.read_csv('./data/' + sys.argv[1] + '_overlap_numeric.csv')
    
    features = list(table_ordinal.columns[2:-1])
    target = list(table_ordinal.columns[-1:])[0]

    X_train, X_test, y_train, y_test = train_test_split(table_ordinal[features], table_ordinal[target], random_state=1)

    dt_entropy = DecisionTreeClassifier(criterion='entropy', max_depth=3)    
    dt_entropy = dt_entropy.fit(X_train, y_train)

    # output a PNG of the decision tree
    dotfile = sys.argv[1] + '_entropy.dot'
    png     = sys.argv[1] + '_entropy.png'

    export_graphviz(dt_entropy, out_file=dotfile, feature_names=features)
    (tree, ) = pydot.graph_from_dot_file(dotfile)
    tree.write_png(png)

    # test
    y_predict = dt_entropy.predict(X_test)
    print "Entropy: {}".format(accuracy_score(y_test, y_predict))

    X_train, X_test, y_train, y_test = train_test_split(table_numeric[features], table_numeric[target], random_state=1)
    dt_gini = DecisionTreeClassifier(criterion='gini', max_depth=3)    
    dt_gini = dt_gini.fit(X_train, y_train)

    # output a PNG of the decision tree
    dotfile = sys.argv[1] + '_gini.dot'
    png     = sys.argv[1] + '_gini.png'

    export_graphviz(dt_gini, out_file=dotfile, feature_names=features)
    (tree, ) = pydot.graph_from_dot_file(dotfile)
    tree.write_png(png)

    y_predict = dt_gini.predict(X_test)
    print "Gini: {}".format(accuracy_score(y_test, y_predict))
     
    gauss = GaussianNB()
    y_predict = gauss.fit(X_train, y_train).predict(X_test)
    print "Bayes: {}".format(accuracy_score(y_test, y_predict))

    random_forest = RandomForestClassifier(criterion='entropy', max_depth=3)
    X_train, X_test, y_train, y_test = train_test_split(table_ordinal[features], table_ordinal[target], random_state=1)
    random_forest.fit(X_train, y_train)
    y_predict = random_forest.predict(X_test)
    print "Random Forest: {}".format(accuracy_score(y_test, y_predict))   
    
    ada = AdaBoostClassifier(random_state=1)
    X_train, X_test, y_train, y_test = train_test_split(table_ordinal[features], table_ordinal[target], random_state=1)
    ada.fit(X_train, y_train)
    y_predict = ada.predict(X_test)
    print "AdaBoost: {}".format(accuracy_score(y_test, y_predict))   
    


