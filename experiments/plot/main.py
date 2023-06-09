import os
import pandas as pd
import numpy as np
from datetime import datetime
import folium
from folium.plugins import HeatMap
import plotly.graph_objects as go
import plotly.offline as pyo

def plot_aqi_heatmap(data, d):
    ## Plots heatmap of AQI given date
    # Create a map centered around the United States
    m = folium.Map(location=[37.8, -96.9], zoom_start=5)

    # Create a list of location and AQI data
    heat_data = [[row['Latitude'], row['Longitude'], row['AQI']] for index, row in data.iterrows()]

    # Add the heatmap to the map
    HeatMap(heat_data).add_to(m)

    # Display the map
    m.save('aqi_heatmap_%s.html' % d)


def plot_aqi_over_time(data, loc):
    ## Plots AQI over time given location
    p = go.Figure(data=go.Scatter(x=data['Date'], y=data['AQI'], mode='markers'))
    pyo.plot(p, filename='scatterplot_%s.html' % loc, auto_open=False)


def main():
    # Where is the logic to parse text and determine plot type?? Here or elsewhere...
    # If 'location' is in text...

    # If 'date' is in string...
    plot_type_requested = 'heatmap'
    # plot_type_requested = 'scatter'

    # Import CSV datasets of AQI, create necessary format for plot function
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    aqi_by_cbsa = pd.read_csv(os.path.join(data_dir, 'daily_aqi_by_cbsa_2022.csv'))
    cbsa_info = pd.read_csv(os.path.join(data_dir, 'aqs_monitors_clean.csv')) # Needed to use the clean version, other was too big for GH
    # cbsa_info = pd.read_csv(os.path.join(data_dir, 'aqs_monitors.csv'))

    # Clean up datasets, get what we care about
    cbsa_info_clean = cbsa_info[['CBSA Name', 'Latitude', 'Longitude']] \
        .drop_duplicates('CBSA Name')
    cbsa_info_clean = cbsa_info_clean[pd.notna(cbsa_info_clean['Latitude']) & pd.notna(cbsa_info_clean['Longitude'])]
    
    aqi_by_cbsa_clean = aqi_by_cbsa[['CBSA', 'AQI', 'Date']] 
    aqi_by_cbsa_clean['Date'] = pd.to_datetime(aqi_by_cbsa_clean['Date'])
    
    # Merge data and basic clean up
    data = aqi_by_cbsa_clean.merge(cbsa_info_clean, left_on='CBSA', right_on='CBSA Name')

    # Plot
    if plot_type_requested == 'heatmap':
        data_set = {
            'year': 2022,
            'mo': 1,
            'day': 1
        }
        plot_aqi_heatmap(
            data[(data['Date'] == datetime(year=data_set['year'], month=data_set['mo'], day=data_set['day']))],
            '%d-%d-%d' % (data_set['year'], data_set['mo'], data_set['day'])
        )

    if plot_type_requested == 'scatter':
        loc_name = 'Columbus, OH'
        plot_aqi_over_time(data[data['CBSA Name'] == loc_name], loc_name)


if __name__ == '__main__':
    main()