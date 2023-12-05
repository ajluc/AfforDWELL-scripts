
import requests
import pandas as pd
import json
from config import *
import time

def geocode_address(address, api_key):
    base_url = "https://us1.locationiq.com/v1/search.php"
    params = {
        "key": api_key,
        "q": address,
        "format": "json",  # Specify the response format as JSON
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        if data:
            # Extract latitude and longitude from the response
            latitude = data[0]["lat"]
            longitude = data[0]["lon"]
            return latitude, longitude
        else:
            print("No results found for the address:", address)
            return None, None
    else:
        print("Error:", data.get("error", "Unknown error"))
        return None, None


def get_address_lat_long(address): 
    # Call the geocode_address function
    latitude, longitude = geocode_address(address, api_key)
    if latitude and longitude:
        # print(f"Latitude: {latitude}, Longitude: {longitude}")
        return latitude, longitude
    else:
        return 0.00,0.00

# #========================
# def modify_row(row):
#     row['Age'] += 1
#     row['City'] = 'Unknown'
#     return row
#=========================

def translate_excel_file_to_geojson(excel_file_path, geojson_file_path = None,sheet_name="Staten Island"):
    """
    _summary_
    """
    # read all the pages of the excel file into separate pandas dataframes,
    # store in a dictionary with the sheet names
    df_dict = pd.read_excel(excel_file_path, sheet_name=None)
    print(df_dict.keys())
    for single_sheet_name in df_dict:
        if single_sheet_name != sheet_name:
            continue
        single_df = df_dict[single_sheet_name]
        single_df[ADDRESS_STRING] = ''
        single_df[LAT_STRING] = ''
        single_df[LON_STRING] = ''

        #iterate through the rows of the dataframe
        end_index = 2500
        for index, row in single_df.iterrows():
            if index == end_index:
                break
            #each row has the following columns "ZIP BLDGNO1	STREET1	STSUFX1	BLDGNO2	STREET2	STSUFX2	CITY	COUNTY	STATUS1	STATUS2	STATUS3	BLOCK	LOT"
            # we need to create a new column called ADDRESS_STRING that is a concatenation of the following columns: "BLDGNO1 STREET1	STSUFX1	CITY"
            address= str(row["bldgno1"]) + " " + str(row["street1"]) + " " + str(row["stsufx1"]) + ", " + str(row["city"] + ", ny") 
            lat,long = get_address_lat_long(address)
            single_df.loc[index,ADDRESS_STRING] = address
            single_df.loc[index,LAT_STRING] = lat
            single_df.loc[index,LON_STRING] = long
            time.sleep(1.1)
            if index % 10 == 0:
                print("At Index",index," out of ", end_index)
                filtered_df = single_df.iloc[0:index]
                filtered_df.to_json(sheet_name+'.json', orient='records', lines=True)

        # print(single_df)
        filtered_df = single_df.iloc[0:end_index]
        filtered_df.to_json(sheet_name+'.json', orient='records', lines=True)


        
            
if __name__ == "__main__":
    translate_excel_file_to_geojson("./Rent Stabilized Buildings Data (2).xlsx",sheet_name="Manhattan")
                                 