#!/usr/bin/python

import os

import numpy as np
import pandas as pd
import scipy.stats as stats

data_path = './raw_data/'
remove_header_list = ['Team', 'Age', 'G', 'AB', 'PA', 'CS', '3B', 'HBP', 'SH', 'SF', 'GDP', 'playerid']

def combine(tables):    


    ctr = 1
    length = len(tables)
    
    while ctr < length:
        tables[0] = tables[0].append(tables[ctr], ignore_index = True)
        ctr += 1
    
    df = tables[0].drop(remove_header_list, axis=1)
    df = df.groupby(['Name']).mean()

    return df

 
        
if __name__ == '__main__':
    AAA_tables = []

    for filename in os.listdir(data_path):
        if filename[:3] == 'AAA':    
            AAA_tables.append(pd.read_csv(data_path + filename))
            
    AAA_df = combine(AAA_tables)

    AAA_df.to_csv('./data/AAA.csv', float_format='%.3f')

