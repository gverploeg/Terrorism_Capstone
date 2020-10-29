import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import folium
from folium.plugins import FastMarkerCluster, Fullscreen, MiniMap, HeatMap, HeatMapWithTime
import geopandas as gpd
from branca.colormap import LinearColormap
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import requests


df = pd.read_csv('../data/globalterrorism.csv', encoding='ISO-8859-1')

df2 = pd.read_csv('../data/gtd1993.csv', encoding='latin-1')
df2.rename(columns={'ï»¿eventid': 'eventid'}, inplace=True)

df_ = pd.concat([df, df2], axis=0)

df_.rename(columns={'eventid': 'Event_ID', 'iyear': 'Year', 'imonth': 'Month', 'iday': 'Day', 'country_txt':'Country','region_txt':'Region',
                    'latitude': 'Latitude', 'longitude': 'Longitude', 'attacktype1_txt':'AttackType','target1':'Target','nkill':'Fatalities',
                    'nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_Type','weaptype1_txt':'Weapon_Type',
                    'motive':'Motive'}, inplace=True)

terror = df_[['Event_ID', 'Year', 'Month', 'Day', 'Country', 'Region', 'Latitude', 'Longitude', 'AttackType', 'Target', 'Fatalities', 'Wounded', 
              'Summary', 'Group', 'Target_Type', 'Weapon_Type', 'Motive']]


toposite2 = 'https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson'
worldgeo = json.loads(requests.get(toposite2).text)

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
world_geo = f'{url}/world-countries.json'
json_data = gpd.read_file(f'{url}/world-countries.json')
worldgeo_ = json.loads(requests.get(world_geo).text)

countries = terror[terror['Fatalities'] >= 1].groupby('Country')['Fatalities'].sum().to_frame().reset_index().sort_values('Fatalities', ascending=False)[:20]
countries['Country'].replace({'United States': 'United States of America'},inplace=True)



m = folium.Map(
    location=[0, 0], 
    zoom_start=1.50,
    tiles='openstreetmap'
)

folium.Choropleth(
    geo_data=worldgeo_,
    name='Ataques Terroristas',
    data=countries,
    columns=['Country', 'Fatalities'],
    key_on='feature.properties.name',
    fill_color='OrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    nan_fill_color='white',
    nan_fill_opacity=0.9,
    legend_name='Terrorism Recorded 1970 - 2017',
    popup_function='Teste'
).add_to(m)

Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True
).add_to(m)

# m.save('../images/terrorism_incidents_worldwide.html')

