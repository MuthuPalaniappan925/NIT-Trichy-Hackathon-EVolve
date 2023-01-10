import streamlit as st
import matplotlib.pyplot as plt
st.title("EDA for Electric Vehicles in India")
import pandas as pd
st.write("Average range of Electric Vehicles in India")
st.image('range.png')
import pandas as pd
chargingstations=pd.read_csv(r'evchargestation.csv')
users=pd.read_csv(r'Indian Cities Database.csv')
import plotly.express as px
color_scale = [(0, 'orange'), (1,'red')]
@st.cache
def plotter(x,latitude,longitude):
  fig = px.scatter_mapbox(x, 
                          lat=latitude, 
                          lon=longitude, 
                          #hover_name="Address", 
                          #hover_data=["Address", "Listed"],
                          #color="Listed",
                          #color_continuous_scale=color_scale,
                          #color='green',

                          #size="Listed",
                          zoom=4, 
                          height=600,
                          width=600)

  fig.update_layout(mapbox_style="open-street-map")
  fig.update_layout(margin={"r":0,"l":0,"b":0})
  return fig

st.write("Distribution of Public EV Charging Stations in India")
fig1=plotter(chargingstations,"latitude","longitude")
st.write(fig1)

st.write('Our Users')
fig2=plotter(users, "Lat","Long")
st.write(fig2)

