#!/usr/bin/python

import os
import sys 

import numpy as np
import pandas as pd
import scipy.stats as stats

data_path = './data/'
keep = ['Name', 'PA', 'WAR']

def to_ordinal(table):
    mean = table['WAR/PA'].mean()

    for index, row in table.iterrows():
        value = row['WAR/PA']
        new = 0

        if value > mean:
            new = 1

        table.at[index, 'WAR/PA'] = new
    
    return table

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Incorrect usage! Exiting ...'
        sys.exit(1)

    minors = pd.read_csv(data_path + sys.argv[1] + '_ordinal.csv')
    majors = pd.read_csv('./raw_data/' + 'MLB.csv')
    
    
    majors_copy = majors
    for column in majors_copy:
        if column not in keep:
            majors = majors.drop(column, axis=1)
    
    majors['WAR/PA'] = 0.0
    
    for index, row in majors.iterrows():
        majors.at[index, 'WAR/PA'] = row['WAR'] / float(row['PA'])
    
    majors.drop('WAR', axis=1, inplace = True)
    majors.drop('PA', axis=1, inplace = True) 
 
    table  = pd.merge(minors, majors, how='inner', on=['Name'])
    table = to_ordinal(table)
    table.rename(columns={'WAR': 'WAR_MLB'}, inplace=True)
    table.to_csv('./data/' + sys.argv[1] +'_overlap.csv')



    

