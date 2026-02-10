# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 10:40:01 2022

@author: tilahun
"""
#%%
import pandas as pd
from BinaryFileHandler import ReadBin

name = ["eu", "af","as","au","na","sa","wg2","wa","clm","clm025"]
ng = [180721, 371410, 841703, 109084, 461694, 226852, 66896, 67420,70412,281648]
continent_index = 0    # Europe
outflowpath = r"U:\Codes\Python_codes\G_OUTFLC.UNF4" # mentions the immediate downstream cell for each cell
MostDownstreamCell = [82130,82129,82128] # Provided by the user

def DelineateBasin(MostDownstreamCell, outflowpath, ng, continent_index):
    OutflowData = ReadBin(outflowpath, ng[continent_index])
    DataTable = {'GCRC': list(range(1,ng[continent_index]+1)), 'DownstreamCell': OutflowData}
    df2 = pd.DataFrame(DataTable)
    df2.set_index('GCRC')
    
    Basincells = MostDownstreamCell
    NewDownstreamcells = MostDownstreamCell
    temp = []
    while temp!= NewDownstreamcells:
        upstreamcells = [df2[df2['DownstreamCell'] == i]['GCRC'].values.tolist() for i in NewDownstreamcells]
        flat_list_upstreamcells = [item for sublist in upstreamcells for item in sublist]
        Basincells.extend(flat_list_upstreamcells)
        temp = NewDownstreamcells
        NewDownstreamcells = flat_list_upstreamcells
    return Basincells

List_of_cells_in_the_basin = DelineateBasin(MostDownstreamCell, outflowpath, ng, continent_index)
df6 = pd.DataFrame({'CellsInBasin':List_of_cells_in_the_basin})
df6.to_excel(r"U:\Codes\Python_codes\BasinCells.xlsx", header = False) 
#%%
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import the basin shape file and the continental grid file

mother_grid = gpd.read_file(r"U:\Codes\WG_mothers\mother_eu.shp")

# Moehne

basin_shp_file = gpd.read_file(r"U:\GIS Files\Moehne_Catchment\Moehne_Catchment_Dissolved.shp")
reservoir_shp_file = gpd.read_file(r"U:\GIS Files\Moehne_reservoir_shp_not_precise")

# Bigge
# basin_shp_file = gpd.read_file(r"U:\GIS Files\Bigge_catchment_shp_file\Bigge_from_hydrosheds_level09.shp")
# reservoir_shp_file = gpd.read_file(r"U:\GIS Files\Bigge_catchment_shp_file\Bigge_Reservoir\BiggeReservoir.shp")

basin_shp_file.plot()
reservoir_shp_file.plot()

# Intersection

intersection = gpd.overlay(mother_grid, basin_shp_file, how='intersection') 
intersection2 = gpd.overlay(intersection, reservoir_shp_file, how='union')  # Including the reservoir shape

intersection2.plot(edgecolor='orange')
intersection2.crs

intersection2.to_file(driver = 'ESRI Shapefile', filename= r"U:\GIS Files\Bigge_catchment_shp_file\Gridded\Bigge_grided_catchment.shp")
# convert CRS to equal-area projection
# the length unit is now `meter`

eqArea_intersection = intersection.to_crs(epsg=6933)

# compute areas in sq kilometers

areas = eqArea_intersection.area / 1000000

# Save the computed areas in a new column of the data frame

intersection['Actual Area (Km2)'] = areas
intersection['Actual Area (Km2)'].round(decimals=6)

# Calculate Portion of cell laying in the basin and Save it in a new column of the data frame

intersection['Portion of cell in the basin'] = intersection['Actual Area (Km2)'] / intersection['AREA_KM2'] *100

# Plot the intersection shp file coloured based on portion of cell in the basin

intersection.plot(column='Portion of cell in the basin', cmap='OrRd', edgecolor='k', legend=True)

# Save the columns 'ARCID' and 'Portion of cell in the basin' in a new dataframe as basin cell

columns_names = ['Cell_ID', 'Portion of Cell in Basin (%)']
Basin_Cells = pd.DataFrame(columns = columns_names)
Basin_Cells['Cell_ID'] = intersection['ARCID']
Basin_Cells['Portion of Cell in Basin (%)'] = intersection['Portion of cell in the basin']

# Save list of Basin_Cells dataframe as csv formatand also as a list
Basin_Cells.to_csv(r"U:\Codes\Python_codes\List_of_cells_in_Bigge_basin.csv")
Basin_Cells_list = list(Basin_Cells['Cell_ID'])
print(Basin_Cells_list)

#%%
# Plot the loading for each cell by Month and by category
# The intersection gdf should be first calculates as shown in the above cell

# Step 1 filter by the month of interest
month = 1
df_load = pd.read_csv("U:\WriteUps\Plots\TP_Load_maps\Load_by_cell_id.csv", index_col=False)
df_load = df_load[df_load.Month != "Yearly load"]
df_load['Month'] = pd.to_numeric(df_load['Month'], errors='coerce')
df_load_month = df_load[df_load['Month'] == month]

# Step 2 Add the loading columns in to the intersection gdf by first changing the indices
intersection_copy = intersection.copy()
intersection_copy = intersection_copy.set_index('ARCID')
df_load_month = df_load_month.set_index('Cell_ID')
intersection_updated = pd.concat([intersection_copy, df_load_month], axis=1)
intersection_updated = intersection_updated.drop(['Month', 'Unnamed: 0'], axis=1)

# Step 3 Plot the new intersection file
intersection_updated.columns
intersection_updated.plot(column='DomesticSeweredLoad', cmap='OrRd', edgecolor='k', legend=True)
intersection_updated.plot(column='InorganicFertilizerLoad', cmap='OrRd', edgecolor='k', legend=True)

#%%
# Perform look up using np.dot

df_RawData = pd.DataFrame({'Letters': {0:'A', 1:'B', 2:'C', 3:'D'}, 
                           'Values':{0:10,1:20,2:30,3:40}, })
df_LookupData = pd.DataFrame({'Number': {0:20, 1:10, 2:40, 3:30},
                              'Color':{0:'Green',1:'Red',2:'Yellow',3:'Blue'}, })

result = np.dot(
                (df_RawData['Values'].values[:,None] == df_LookupData['Number'].values), # If this is true,
                df_LookupData['Color']    # Then, give this as an output
                )
print(result)

# Add the result as a new column to the raw data

df_RawData['Colour'] = result

#%% Plotting weather stations
Germnay_Shp_file = gpd.read_file(r"U:\GIS Files\DEU_adm\DEU_adm2.shp")
Weather_stations_thiessen_shp = gpd.read_file(r"U:\GIS Files\WeatherStationsDWD\Weather_Stations_with_Thiessen_weights\Thiessen_polygon_weather_stations_moehne.shp")
Weather_stations_thiessen_shp.plot()
# Plot the Moehne basin map over Germany's map

fig, ax1 = plt.subplots(figsize=(10, 7))
Germnay_Shp_file.plot(ax = ax1, color='y', edgecolor='black', lw=0.7)
basin_shp_file.plot(ax = ax1, color='m')

# Plot Weather Stations in Moehne Basin
fig, ax2 = plt.subplots(figsize=(10, 5))
WeatherStations = pd.read_excel(r'U:\Data\DWD_Weather_Data\Moehne_Catchment\Weather_Stations_in_Moehne_Basin.xlsx', header = 0)
WeatherStations_gdf = gpd.GeoDataFrame(WeatherStations, geometry=gpd.points_from_xy(WeatherStations['Longitude'], WeatherStations['Latitude']))

# ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'

# WeatherStations_gdf.to_file(filename = r'U:\GIS Files\WeatherStationsDWD\WeatherStations_in_Moehne_basin.shp', driver = 'ESRI Shapefile')#, crs_wkt = ESRI_WKT)
Weather_stations_thiessen_shp.plot(ax = ax2, color=None, edgecolor = 'black')
WeatherStations_gdf.plot(ax = ax2, markersize = 50, color='b')






