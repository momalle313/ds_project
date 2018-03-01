#!/usr/bin/python

import os
import sys


import numpy as np
import pandas as pd
import scipy.stats as stats

data_path = './raw_data/'
keep =          ['Name', 'PA', 'BB%', 'K%', 'BB/K', 'AVG', 'OBP', 'SLG', 'OPS']
higher_better = [False,  True, True, False, True, True, True, True, True] 

remove = []

def usage(program):
    print 'Usage: {} league'.format(program)

def clean(table):
    for column in table:
        if column not in keep:
            remove.append(column)
    
    table = table.drop(remove, axis=1)
    
    for column in table:
        if column == 'BB%' or column == 'K%':
            table[column] = table[column].str.replace(' %', '')
            table[column] = table[column].astype(float)

    return table

def weighted_average(g):
    return g._get_numeric_data().multiply(g['PA'], axis=0).sum()/g['PA'].sum()

def combine(tables):    

    ctr = 1
    length = len(tables)
    
    while ctr < length:
        tables[0] = tables[0].append(tables[ctr], ignore_index = True)
        ctr += 1
    
    return tables[0].groupby(['Name']).apply(weighted_average)

def to_ordinal(table):
    for column in table:
        try:
            stddev = table[column].std()
            mean = table[column].mean()
        except ValueError as ex:
            continue

        minimum = mean - stddev
        maximum = mean + stddev
        
        for index, row in table.iterrows():
            value = row[column]

            new = 1
            h_better = higher_better[keep.index(column)]
            if value < minimum:
                if h_better:
                   new = 0
                else: 
                    new = 2
            elif value > maximum:
                if h_better:
                    new = 2
                else:
                    new = 0
    
            table.at[index, column] = new 

    return table

if __name__ == '__main__':
    tables = []
    
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        sys.exit(1)

    for filename in os.listdir(data_path):
        if filename[:3] == sys.argv[1]:    
            tables.append(clean(pd.read_csv(data_path + filename)))
            

    numerical_data = combine(tables)
    numerical_data.to_csv('./data/' + sys.argv[1] + '_numerical.csv', float_format='%.3f')
    
    ordinal_data = to_ordinal(numerical_data)
    ordinal_data.to_csv('./data/' + sys.argv[1] + '_ordinal.csv', float_format='%.0f')
