'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

#Reading in DF
tickets = pd.read_csv('cache/top_locations_mappable.csv')

#Setting the title for the dashboard
st.title('Locations with parking ticket totals over $1,000')

#Converting the df to a geopandas dataframe
geo_df = gpd.GeoDataFrame(tickets, geometry= gpd.points_from_xy(tickets.lon, tickets.lat))

#Specificy the starting center coordinates for the map, and the zoom level
map = folium.Map(location = CUSE, zoom_start= ZOOM)


ticekts_map = geo_df.explore( 
    geo_df['amount'],           #Color the markers based on amount values
    m = map,                    #Adds to the map created above
    legend = True,              #Specifies to display the legend with color scale of markers
    legend_name = 'Amount',     #Names the legend amound
    marker_type= 'circle',      #Specifies to use circle markers
    marker_kwds= {'radius': 15, #Makes each marker have radius of 15 pixes
                  'fill': True} #Fills in the cirlce

)

#Embeds map into the streamlit widget for displaying
sf.folium_static(ticekts_map, width = 1000, height = 800)