'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")

#Reads in DF with all columns filtered by the top locations
tickets = pd.read_csv('cache/tickets_in_top_locations.csv')

#Sets the title and caption for streamlist
st.title('Top Locations for Parking Tickets within Syracuse')
st.caption('This dashboard shows the parking tickets that were issued in the top locations with $1,000 or more total aggregate voilation amounts')

#Creates a list of unique locations in the DF to use for the dropdown selection
unique_locations = tickets['location'].unique()

#Creates a drop downbox to select a location to analyze
location = st.selectbox('Select a location', unique_locations)

#If a location is selected the following code will run
if location:

    #Creates a new DF with only rows matching the location of the selected location
    filtered_tickets = tickets[tickets['location'] == location]

    #Creates two columns to put output of widgets side by side
    col1, col2 = st.columns(2)

    with col1:

        #Displays a metric of how many tickets have been issued in selected locations
        st.metric('Number of tickets issues: ', len(filtered_tickets))

        #Creates a plotting area for creating plot below
        fig1, ax1 = plt.subplots()

        #Sets the title of the plot
        ax1.set_title('Tickets Issued by Hour of Day')

        #Creates a bar plot based on filtered data, with hourofday on X axis, count on Y, and color as hour of day
        sns.barplot(data = filtered_tickets, x = 'hourofday', y = 'count', estimator = 'sum', hue = 'hourofday', ax = ax1)

        #Displays the plot created
        st.pyplot(fig1)

    #Same as code above, only changing the ouput of metric to sum of tickets, and changing the graph to display day of week 
    with col2:
        st.metric('Total amount', f"$ {filtered_tickets['amount'].sum()}")
        fig2, ax2 = plt.subplots()
        ax2.set_title('Tickets Issued by Day of Week')
        sns.barplot(data =  filtered_tickets, x = 'dayofweek', y = 'count', estimator = 'sum', hue = 'dayofweek')
        st.pyplot(fig2)
    
    #Creates a map of the point where the selected location is. Since there's only one location in the DF all the lat lon points are the same
    st.map(filtered_tickets[['lat', 'lon']])