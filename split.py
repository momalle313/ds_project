#!/usr/bin/python

import os
import sys 

import numpy as np
import pandas as pd
import scipy.stats as stats


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Incorrect usage! Exiting ...'
        sys.exit(1)

    original = pd.read_csv('./data/' + sys.argv[1] + '_overlap.csv')
    training  = pd.DataFrame({})
    testing = pd.DataFrame({})

    for index, row in original.iterrows():
        if index % 2 == 0:
            training = training.append(row, ignore_index=False)
        else:
            testing = testing.append(row, ignore_index=False)
    
    training = training[original.columns]
    testing = testing[original.columns]

    training.to_csv('./data/AAA_training.csv')
    testing.to_csv('./data/AAA_testing.csv')

