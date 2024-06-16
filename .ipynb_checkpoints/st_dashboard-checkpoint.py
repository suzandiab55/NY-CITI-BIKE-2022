############################ Importing necessary libraries ##############################################################
import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt

########################### Initial settings for the dashboard ##################################################
st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Citi Bike currently faces.")
st.markdown("Right now, Citi Bike runs into situations where customers complain about bikes not being available at certain times. This analysis aims to look at the potential reasons behind this.")

####################### Import data #########################################

df = pd.read_csv('reduced_data_to_plot.csv')
df_agg = pd.read_csv('aggregated_data.csv')
top20 = pd.read_csv('top20.csv')

####################### Bar Chart ########################################

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color' : top20['value'], 'colorscale' : 'Blues'}))
fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York',
    xaxis_title = 'Start Stations', 
    yaxis_title = 'Sum of Trips', 
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width = True)

############################ Line chart ###################################

fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(x=df_agg['date'], y=df_agg['bike_rides_daily'], name='Daily Bike Rides', marker={'color': 'red'}),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(x=df_agg['date'], y=df_agg['avgTemp'], name='Daily Temperature', marker={'color': 'blue'}),
    secondary_y=True
)

fig_2.update_layout(
    title='Daily Bike Trips and Temperature in 2022',
    xaxis_title='Date',
    yaxis_title='Daily Bike Rides',
    height=800
)

fig_2.update_layout(
    title='Daily Bike Trips and Temperature in New York 2022',
    xaxis_title='Date',
    yaxis_title='Daily Bike Rides',
    yaxis2_title='Daily Temperature'
)

st.plotly_chart(fig_2, use_container_width=True)

############ Add the Map ##########

path_to_html = "nyc_bike_map.html" 

############# Read file and keep in variable#####################
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)


