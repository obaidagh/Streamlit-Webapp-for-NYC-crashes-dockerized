from copyreg import pickle
import streamlit as st
import pandas as pd
import numpy as np
from datetime import time
import pydeck as pdk
import plotly.express as px


data_path = './Motor_Vehicle_Collisions_-_Crashes.csv'

# 1-Title&Description

st.title("Motor Vechicle collisions in NYC🗽")
st.markdown("### A streamlit dashboard to analyze motor vehicle collisions")


# 2-Data loading from CSV
@st.cache(persist=True)
def load_data(data_path, nrows):

    data = pd.read_csv(data_path, nrows=nrows, parse_dates=[
                       ['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date_time'}, inplace=True)
    return data


data = load_data(data_path, 100000)


# 3- First question
st.header("1- Where are the most people are injured ?")

injured_people = st.slider(
    "Numbers of persons injured in a single collision", 1, 19)
st.map(data.query("injured_persons >= @injured_people")
       [['latitude', 'longitude']].dropna(how='any'))


# 4- Second question
st.header("2- How many collisions occur in a given timeframe?")

# Creating timeframe
time_frame = st.slider(
    "Select time frame to inspect:",
    value=(time(8, 0), time(16, 30)))

time_list = [
    time_frame[0].replace(second=0, microsecond=0),
    time_frame[1].replace(second=0, microsecond=0)
]


data_tframe = data[(data['date_time'].dt.time >= time_list[0])]
data_tframe = data_tframe[(
    data_tframe['date_time'].dt.time <= time_list[1])]

st.write("Selected time", time_list[0], time_list[1])

# Pydeck map
midpoint = (np.average(data_tframe['latitude']),
            np.average(data_tframe['longitude']))

layer = pdk.Layer(
    "HexagonLayer",
    data=data_tframe[['date_time', 'latitude', 'longitude']],
    get_position=['longitude', 'latitude'],
    radius=100,
    extruded=True,
    pickable=True,
    elevation_scale=4,
    elevation_range=[0, 1000],
),

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 10,
        "pitch": 70,
        "bearing": -30
    },
    layers=[layer],

))

# Per minute Histogram
st.subheader("Breakdown By minute between {} and {}".format(
    str(time_list[0]), str(time_list[1])))

hist = np.histogram(
    data_tframe['date_time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({
    'minute': range(60),
    'No_collisions': hist
})

fig = px.bar(chart_data, x='minute', y='No_collisions',
             hover_data=['minute', 'No_collisions'], height=400)
st.write(fig)

if st.checkbox('Show raw data', False):
    # st.subheader('data_tframe')
    st.write(data_tframe)


# 5- Third question
st.header("3- which streets are the most dengerous?")
select = st.selectbox('Affected type of people', [
                      'pedestrians', 'Cyclists', 'Motorists'])
if select == 'pedestrians':
    st.dataframe(data.query("injured_pedestrians >=1")[["on_street_name", "injured_pedestrians"]].sort_values(
        "injured_pedestrians", ascending=False).dropna(how='any')[:5])

elif select == 'Cyclists':
    st.dataframe(data.query("injured_cyclists >=1")[["on_street_name", "injured_cyclists"]].sort_values(
        "injured_cyclists", ascending=False).dropna(how='any')[:5])

elif select == 'Motorists':
    st.dataframe(data.query("injured_motorists >=1")[["on_street_name", "injured_motorists"]].sort_values(
        "injured_motorists", ascending=False).dropna(how='any')[:5],)
