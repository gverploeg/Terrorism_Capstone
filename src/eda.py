import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from clean_data import *

def fatalities_greater_than(df, num):
    '''
    Create dataframe where fatalities are above a certain amount
    '''
    terror_gtr = df[df['Fatalities'] >= num]
    return terror_gtr

def groupby_func(df, group, agg_column, modifier = 'sum'):
    '''
    Create different groupby dataframes with different aggregate functions
    '''
    if modifier == 'sum':
        return df.groupby(group)[agg_column].sum().reset_index()
    elif modifier == 'max':
        return df.groupby(group)[agg_column].max().reset_index()
    elif modifier == 'min':
        return df.groupby(group)[agg_column].min().reset_index()
    elif modifier == 'count':
        return df.groupby(group)[agg_column].count().reset_index()

def plots_over_time(df, column1, column2, xlab, ylab, title, save_loc):
    ''' Plot different variables over time: Overall Dttacks, Deaths '''
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, figsize=(15,6))
    x = df.iloc[:, column1]
    y = df.iloc[:,column2]
    sns.barplot(x,y,palette='rocket',edgecolor=sns.color_palette('dark',10))
    plt.xticks(rotation=90, fontsize=13)
    ax.set_xlabel(xlab, fontsize=15)
    ax.set_ylabel(ylab, fontsize=15)
    ax.set_title(title, fontsize=18)
    plt.savefig(save_loc, bbox_inches = 'tight')




if __name__ == '__main__':
    df = pd.read_csv('../data/globalterrorism.csv', encoding='ISO-8859-1')
    df2 = pd.read_csv('../data/gtd1993.csv', encoding='ISO-8859-1')

    dict1 = {'ï»¿eventid': 'eventid'}
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

    ''' Create dataframe of fatalities greater than 1'''
    terror_gtr = fatalities_greater_than(terror, 1)
    # print(terror_gtr.head(10))

    ''' Plot 1: Amount of Terrorist Attacks Over Time'''
    attack_time = groupby_func(terror, 'Year', 'Event_ID', 'count')
    #  Creates dataframe that shows the count of attacks for each year
    plots_over_time(attack_time, 0,1, "Year", "Number of Attacks", "Number of Attacks Over Time", '../images/Attacks_Over_Time.png' )
    
    ''' Plot 2: Amount of Fatalities Over Time'''
    # death_time = groupby_func(terror, 'Year', 'Fatalities', 'sum')
    #  Creates dataframe that shows the sum of deaths for each year
    # plots_over_time(death_time, 0,1, "Year", "Number of Deaths", "Amount of Deaths Over Time" )

    ''' Plot 3: Amount of Fatalities Over Time'''

    plt.show()
    


