from audio_recorder_streamlit import audio_recorder
from datetime import datetime
from folium.plugins import HeatMap
from streamlit_folium import st_folium

import datefinder
import folium
import locationtagger
import openai
import os
import pandas as pd
import streamlit as st
import us

openai.api_key = 'Free the models'
openai.api_base = "https://leapfrogai.dd.bigbang.dev"

data_dir = os.path.join(os.path.dirname(__file__), "..", 'data')
print(data_dir)


def plot_aqi_heatmap(data, d):
    # Plots heatmap of AQI given date
    # Create a map centered around the United States
    m = folium.Map(location=[37.8, -96.9], zoom_start=4, no_touch=True)

    # Create a list of location and AQI data
    heat_data = [[row['Latitude'], row['Longitude'], row['AQI']]
                 for index, row in data.iterrows()]

    # Add the heatmap to the map
    HeatMap(heat_data).add_to(m)

    # Display the map
    st_folium(m, height=400, width=700)


st.title("Plot Air Quality Index Data with Your Voice!")
audio_bytes = audio_recorder(
    pause_threshold=5.0,
    text="Click the Robot and Start Talking",
    recording_color="#0000CD",
    neutral_color="#87CEFA	",
    icon_name="robot",
    icon_size="6x",
)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    wav_file = open("/tmp/audio.mp3", "wb")
    wav_file.write(audio_bytes)
    wav_file.close()

    wav_file = open("/tmp/audio.mp3", "rb")

    # post the bytes `audio_bytes` to the openai REST endpoint
    transcript = openai.Audio.translate(
        "whisper-1", wav_file, language="en", prompt="What would you like to do?")
    st.write("Transcript: ", transcript.text)

    place_entity = locationtagger.find_locations(text=transcript.text)

    # Find any states mentioned in the transcript
    stateRestrictor = ""
    if len(place_entity.regions) > 0:
        st.write("The states listed:", place_entity.regions)
        us_state = us.states.lookup(place_entity.regions[0])
        stateRestrictor = us_state.abbr

    dates_found_generator = datefinder.find_dates(transcript.text)
    dates_found = list(dates_found_generator)
    if len(dates_found) > 0:
        st.write("The dates found", list(dates_found))

    aqi_by_cbsa = pd.read_csv(os.path.join(
        data_dir, 'daily_aqi_by_cbsa_2022.csv'))

    # Needed to use the clean version, other was too big for GH
    cbsa_info = pd.read_csv(os.path.join(data_dir, 'aqs_monitors_clean.csv'))
    # cbsa_info = pd.read_csv(os.path.join(data_dir, 'aqs_monitors.csv'))

    # Clean up datasets, get what we care about
    cbsa_info_clean = cbsa_info[['CBSA Name', 'Latitude', 'Longitude']] \
        .drop_duplicates('CBSA Name')

    cbsa_info_clean = cbsa_info_clean[pd.notna(
        cbsa_info_clean['Latitude']) & pd.notna(cbsa_info_clean['Longitude'])]

    aqi_by_cbsa_clean = aqi_by_cbsa[['CBSA', 'AQI', 'Date']]
    aqi_by_cbsa_clean['Date'] = pd.to_datetime(aqi_by_cbsa_clean['Date'])

    # Merge data and basic clean up
    data = aqi_by_cbsa_clean.merge(
        cbsa_info_clean, left_on='CBSA', right_on='CBSA Name')

    # Filter to a specific state if provided
    if stateRestrictor != "":
        print("Restriciting to state: ", stateRestrictor)
        data = data.loc[data['CBSA Name'].str.split(
            ', ').str[1].str.contains(stateRestrictor)]

    # Filter to a specific date
    data_set = {
        'year': dates_found[0].year,  # 2022,
        'mo': dates_found[0].month,  # 1,
        'day': dates_found[0].day,  # 1
    }

    plot_aqi_heatmap(
        data[(data['Date'] == datetime(year=data_set['year'],
              month=data_set['mo'], day=data_set['day']))],
        '%d-%d-%d' % (data_set['year'], data_set['mo'], data_set['day'])
    )
