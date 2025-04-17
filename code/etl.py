import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    
    #Creates a pivot table with location as the index, and the sum of the values for each location
    location_amounts_df = violations_df.pivot_table(index = 'location', values = 'amount', aggfunc= 'sum')

    #Sorts the amount values in descending order
    location_amounts_df = location_amounts_df.sort_values('amount', ascending= False)

    #Currently, the locations are a index not a column so makes the locations into a column
    location_amounts_df['location'] = location_amounts_df.index

    #Resets the index to regular numerical values instead of locations
    location_amounts_df = location_amounts_df.reset_index(drop = True)
    #Filters for amounts that are greather than or equal to the threshold of 1,000
    location_amounts_df = location_amounts_df[location_amounts_df['amount'] >= threshold]

    #Returns the new DF
    return location_amounts_df
    

def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:

    #Calls the function created in the previous step
    top_locations_df = top_locations(violations_df)

    #Filters original violations DF to just three columns: location, lat, lon. Keeps only one row per location
    violations_df_filtered = violations_df[['location', 'lat', 'lon']].drop_duplicates(subset = 'location')

    #Joins the DF from last step with filtered violations DF, adding lat and lon to previous DF
    merged_df = pd.merge(top_locations_df, violations_df_filtered, on= 'location', how= 'inner')

    #Returns new DF
    return merged_df


def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:

    #Creates top locations df using the function created earlier
    top_locations_df = top_locations(violations_df)

    #Inner joins original violations df with just the locations of the top locations df to get all ticket info for top locations
    merged_df = pd.merge(violations_df, top_locations_df[['location']], on = 'location', how = 'inner')

    #Returns new DF
    return merged_df


if __name__ == '__main__':
    '''
    Main ETL job. 
    '''

    #Reads in original ticket DF
    parking_df = pd.read_csv('cache/final_cuse_parking_violations.csv')

    #Calls all three functions created above to make new DF's
    top_locations_df = top_locations(parking_df)
    top_locations_mappable_df = top_locations_mappable(parking_df)
    tickets_in_top_locations_df = tickets_in_top_locations(parking_df)

    #Verifies each one of the DF's has the desired information
    print(top_locations_df.head())
    print(top_locations_mappable_df.head())
    print(tickets_in_top_locations_df.head())

    #Saves all three DF's as csv's in the cache folder for later analysis. Commented out so new csv's don't get created each run
    #top_locations_df.to_csv('cache/top_locations.csv')
    #top_locations_mappable_df.to_csv('cache/top_locations_mappable.csv')
    #tickets_in_top_locations_df.to_csv('cache/tickets_in_top_locations.csv')
    