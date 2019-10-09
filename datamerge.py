#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:18:46 2019

@author: flatironschool
"""
import pandas as pd

def create_offender_df(offender_df, population_df):
    
    '''This function creates an aggregated df from offender_df and 
    from population_df, returns a merged df containing offender number in
    normalized form for black and white races.'''
    
    df = offender_df.groupby(['state', 'year', 'race']).offenders.sum().reset_index()
    df2 = pd.merge(df, population_df, on=['state', 'year'])
    df_black = df2.loc[df2.race=='Black or African American']
    df_white = df2.loc[df2.race=='White']
    
    '''The function normalizes the offender ratio according to the population 
    proportion of that race, displaying on 1000 people.'''
    
    df_black['black_pop'] = df_black['black'] * df_black['population']
    df_black['black_norm'] = df_black.offenders / df_black.black_pop * 1000
    df_black = df_black.loc[:, ['state', 'year', 'black_norm']]
    
    df_white['white_pop'] = df_white['white'] * df_white['population']
    df_white['white_norm'] = df_white.offenders / df_white.white_pop * 1000
    df_white = df_white.loc[:, ['state', 'year', 'white_norm']]
    
    df3 = pd.merge(df_white, df_black, on=['state', 'year'])
    
    return df3
    
    
def create_population_df(employment_df, race_ratio_df):
    
    '''This function pulls out population information from employment_df
    by state and by year, and adds the race distribution ratio, returns the
    created df.'''
    
    ''' * * *
    ethnicity table source: 2017 1-year American Community Survey estimates, U.S. Census Bureau
    Retrieving from: https://www.governing.com/gov-data/census/state-minority-population-data-estimates.html
    * * *'''
    
    race_ratio_df.rename(columns = {'Unnamed: 0':'state_name'}, inplace=True)
    race_ratio_df.columns = race_ratio_df.columns.map(lambda x: x.lower())
    population_df = employment_df.loc[:, ['state_abbr', 'year', 'population', 'state_name']]
    population_df = population_df.rename(columns = {'state_abbr':'state'})
    population_df = pd.merge(population_df, race_ratio_df, how='left', on='state_name')
    
    return population_df