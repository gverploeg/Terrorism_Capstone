import pandas as pd
import numpy as np


def rename_columns(df, diction):
    '''
    Replaces prior column names with new ones

    ARGS:
        df - dataframe
        diction - dictionary containing old column names and new column names
    
    RETURN:
        New dataframe with null values replaced
    '''
    df.rename(columns=diction, inplace=True)


def merge_dataframes(df, df2):
    '''
    The year 1993 was missing so I need to add it to the whole dataframe

    ARGS:
        df - dataframe
        df2 - second dataframe to be added
    RETURN:
        New dataframe with prior two combined 
    '''
    joined_df = pd.concat([df, df2], axis=0)
    return joined_df


def new_df_with_specific_columns(df, col_list):
    '''
    Select the columns that are necessary for my analysis
    ARGS:
        df - dataframe
        col_list - list of columns 
    RETURN:
        New dataframe with specific columns
    '''
    terror = df[col_list]
    return terror

def display_row_nulls(df):
    '''
    Shows the rows with null values 
    
    ARGS: 
        df - dataframe
    RETURNS
        dataframe that has rows with null vals
    '''
    is_NaN = df.isnull()
    row_has_Nan = is_NaN.any(axis = 1)
    return df[row_has_Nan].head(15)

def display_col_nulls_with_amount(df):
    '''
    Shows the columns with null values and amount
    
    ARGS: 
        df - dataframe
    RETURNS
        dataframe that has columns with null vals and amount
    '''
    return df.isnull().sum().sort_values(ascending = False).head(20)

def replace_null_values(df, column, replacement):
    '''
    Replaces null vals inside a column with your designated replacement

    ARGS:
        df - dataframe
        column - dataframe column name as str
        replacement - string
    RETURN:
        New dataframe with null values replaced
    '''
    df = df[column].fillna(replacement, inplace = True)


if __name__ == '__main__':
    df = pd.read_csv('../data/globalterrorism.csv', encoding='ISO-8859-1')
    df2 = pd.read_csv('../data/gtd1993.csv', encoding='ISO-8859-1')

    dict1 = {'ï»¿eventid': 'eventid'}
    '''When combining the 1993 data, ï»¿eventid needed to be renamed in order to merge properly'''
    
    dict2 = {'eventid': 'Event_ID', 'iyear': 'Year', 'imonth': 'Month', 'iday': 'Day', 'country_txt':'Country','region_txt':'Region',
                    'latitude': 'Latitude', 'longitude': 'Longitude', 'attacktype1_txt':'AttackType','target1':'Target','nkill':'Fatalities',
                    'nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_Type','weaptype1_txt':'Weapon_Type',
                    'motive':'Motive'}
    columns_list = ['Event_ID', 'Year', 'Month', 'Day', 'Country', 'Region', 'Latitude', 'Longitude', 'AttackType', 'Target', 'Fatalities', 'Wounded', 
              'Summary', 'Group', 'Target_Type', 'Weapon_Type', 'Motive']

    rename_columns(df2, dict1)
    joined_df = merge_dataframes(df, df2)
    rename_columns(joined_df, dict2)
    replace_null_values(joined_df, 'Fatalities', 0)
    replace_null_values(joined_df, 'Wounded', 0)
    terror = new_df_with_specific_columns(joined_df, columns_list)
    print(terror.head())

    
    
