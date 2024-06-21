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
from PIL import Image
from numerize.numerize import numerize

########################### Initial settings for the dashboard ##################################################
st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")

########################### Define side bar #####################
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Introduction","Weather Component and Bike Usage",
   "Most Popular Bike Stations",
    "Interactive Map with Aggregated Bike Trips", "Recommendations"])

####################### Import data #########################################

df = pd.read_csv('reduced_data_to_plot_split.csv')
df_agg = pd.read_csv('aggregated_data.csv')
top20 = pd.read_csv('top20.csv')

######################################### DEFINE THE PAGES ###################################


############ INTRO PAGE ############

if page == "Introduction":
    st.markdown("#### This dashboard is designed to offer valuable insights into the current expansion challenges faced by Citi Bike.")
    st.markdown("Presently, Citi Bike encounters issues where customers frequently report bike shortages at specific times. This analysis aims to explore the underlying causes of these availability problems.")
    st.markdown("The dashboard is separated into 4 sections:")
    st.markdown("- Most Popular Bike Stations")
    st.markdown("- Weather Component and Bike Usage")
    st.markdown("- Interactive Map with Aggregated Bike Trips")
    st.markdown("- Recommendations")
    st.markdown("The 'Aspect Selector' dropdown on the left allows navigation through the different categories examined in the analysis.")

    myImage = Image.open("citibike.jpg") #source: https://commons.wikimedia.org/wiki/File:Citi_Bike_logo.jpg
    st.image(myImage)
    st.markdown ("Source: https://commons.wikimedia.org/wiki/File:Citi_Bike_logo.jpg")

########### Create the dual axis line chart page ###############
    
elif page == 'Weather Component and Bike Usage':

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
    title=dict(
        text='Daily Bike Trips and Temperature in New York 2022',
        font=dict(
            size=22
        )
    ),
    xaxis_title='Date',
    yaxis_title='Daily Bike Rides',
    yaxis2_title='Daily Temperature',
    height=800,
    xaxis=dict(
        title=dict(
            text='Date',
            font=dict(
                size=20
            )
        )
    ),
    yaxis=dict(
        title=dict(
            text='Daily Bike Rides',
            font=dict(
                size=20
            )
        )
    ),
    yaxis2=dict(
        title=dict(
            text='Daily Temperature',
            font=dict(
                size=20 
            )
        )
    )
)

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("A seasonal trend is evident in both bike trips and temperature. Bike trips peak during the warmer months (May to October) and reach their lowest during the colder months (December to February). Similarly, temperatures are highest in summer and lowest in winter.")
    st.markdown("There is a clear correlation between temperature fluctuations and the frequency of bike trips. As temperatures drop, so does bike usage. This insight suggests that the shortage issue Citi Bike faces is primarily a concern during the warmer months.")

########## MOST POPULAR STATIONS PAGE #######################

#### Create the season variable ########

elif page == 'Most Popular Bike Stations':
    
####### Create the filter on the side bar ########
    with st.sidebar:
        st.write("Select or deselect a season to see how it influences bike trips.")
        with st.expander("Season", expanded=True):
            season_options = df['season'].unique()
            season_filter = []
            for season in season_options:
                if st.checkbox(season, value=True):
                    season_filter.append(season)

# Filter the dataframe based on the selected seasons
    
    df1 = df[df['season'].isin(season_filter)]

####### Define the total rides ###########
   
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value=numerize(total_rides))

######### Bar Chart ###########

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color' : top20['value'], 'colorscale' : 'Blues'}))
    fig.update_layout(
        title=dict(
            text = 'Top 20 Most Popular Bike Stations in New York',
            font=dict(
            size=22
        )
    ),
        xaxis = dict(
            title = dict(
                text = 'Start Stations',
                font=dict(
                size=20
             )
        )
    ),
    yaxis=dict(
        title=dict(
            text='Sum of Trips',
            font=dict(
                size=20
            )
        )
    ), 
        width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width = True)
    st.markdown("The bar chart clearly shows that certain start stations are more popular than others. The top four stations are West 21st Street/6th Avenue, West Street/Chambers Street, Broadway/West 58th Street, and 6th Avenue/West 33rd Street. These findings indicate that Citi Bike stations in Midtown Manhattan and near Central Park experience the highest usage. Further exploration of this trend can be conducted using the interactive map available through the sidebar select box.")

################# AGGREGATED BIKE TRIPS PAGE #################

elif page == 'Interactive Map with Aggregated Bike Trips': 
    
######### Create the map ##########

    st.write("Interactive Map Showing Aggregated Bike Trips over New York")

    path_to_html = "nyc_bike_map.html" 

############# Read file and keep in variable #####################

    with open(path_to_html,'r') as f: 
        html_data = f.read()

## Show in webpage #######
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=800)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("West 21st Street/6th Avenue, West Street/Chambers Street, Broadway/West 58th Street, and 6th Avenue/West 33rd Street. While having the aggregated bike trips filter enabled, we can see that even though Broadway/West 58th Street and 6th Avenue/West 33rd Street are popular start stations, they don't account for the most commonly taken trips.")
    st.markdown("The most common routes (>3,500) are:")
    st.markdown("West 21st St & 6th Avenue/9th Avenue & West 22nd St, West St & Chambers St/10th Avenue & West 14th St, 11th Avenue & West 41st St/11th Avenue & West 41st St, and 12th Avenue & West 40th St/10th Avenue & West 14th St.")
    st.markdown("These routes are near the the Hudson River Greenway, Chelsea, and the Meatpacking District.")
    st.markdown("Citi Bike routes are most popular in busy areas with many homes, businesses, transit stations, and parks. The Hudson River Greenway is a major bike path, and key routes running east-west and north-south help people commute and enjoy recreational biking across Manhattan.")

else:
    
    st.header("Conclusions and Recommendations")
    bikes = Image.open("recommendationpic.jpg")  #source: https://www.competitionsciences.org/2020/10/29/statistics-education-resources-for-teachers-and-students-from-the-asa/
    st.image(bikes)
    st.markdown ("Source: https://www.competitionsciences.org/2020/10/29/statistics-education-resources-for-teachers-and-students-from-the-asa/")
    st.markdown("### The analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations or increase the size of existing stations in high-demand areas to accomodate bike shortages, such as the Hudson River Greenway, Chelsea, and the Meatpacking District.")
    st.markdown("- Offer incentives, such as a $2 ride credit for users who return bikes to less busy stations or ride during off-peak hours.")
    st.markdown("- Ensure bikes are fully stocked in these areas during the warmer months to meet higher demand, while reducing the supply in winter and late autumn to lower logistics costs.")
