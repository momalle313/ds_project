#!/usr/bin/python

import os
import sys 

import numpy as np
import pandas as pd
import scipy.stats as stats

data_path = './data/'
keep = ['Name', 'PA', 'WAR']

def to_ordinal(table_ordinal):
    mean = table_ordinal['WAR/PA'].mean()

    for index, row in table_ordinal.iterrows():
        value = row['WAR/PA']
        new = 0

        if value > mean:
            new = 1

        table_ordinal.at[index, 'WAR/PA'] = new
    
    return table_ordinal

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Incorrect usage! Exiting ...'
        sys.exit(1)

    minors_ordinal = pd.read_csv(data_path + sys.argv[1] + '_ordinal.csv')
    minors_numeric = pd.read_csv(data_path + sys.argv[1] + '_numeric.csv')

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
 
    table_ordinal  = pd.merge(minors_ordinal, majors, how='left', on=['Name']) 
    table_ordinal = to_ordinal(table_ordinal)
    table_ordinal.rename(columns={'WAR': 'WAR_MLB'}, inplace=True)
    
    table_numeric = pd.merge(minors_numeric, majors, how='left', on=['Name']) 
    table_numeric = to_ordinal(table_numeric)
    table_numeric.rename(columns={'WAR': 'WAR_MLB'}, inplace=True)   
    
    table_ordinal.to_csv('./data/' + sys.argv[1] +'_overlap_ordinal.csv', index=False, float_format='%.0f')
    table_numeric.to_csv('./data/' + sys.argv[1] +'_overlap_numeric.csv', index=False, float_format='%.3f')



    

