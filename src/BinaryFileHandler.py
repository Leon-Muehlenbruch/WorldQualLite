# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 15:54:14 2021

@author: tilahun
"""



#%%
""" 1. Function to get information about the file """

def getFileInfo(filepath):
    
    filename = filepath.split("/")[-1]                                          # Gives the exact file name together with the extension
    
    # Number of layers (Example 12 for monthly data, 31 for daily data etc...)
    
    after_first_dot = filename.split(".")[1]                                    # Gives the immediate word after the first dot (i.e Either file extension or number of layers Ex. if .12.UNF1 then after_first_dot=12 , if UNF1 then after_first_dot=UNF1    
    if after_first_dot.startswith("U"):                                         # i.e when the number of layers is not explicitly mentioned in the file name
        nlayers = 1
    else:                                                                       # i.e when the number of layers is explicitly mentioned in the file name
        nlayers = int(after_first_dot)
    
    # Number of bytes that represent a single element Ex. 1 byte for character, 2 byte for integers ...
    
    file_extension = filename.split(".")[-1]                                    # Type of the file (the file extension ex. UNF0, UNF1, UNF2 or UNF4)
    if file_extension[-1] == "0":                                               # UNF0
        Size = 4
    elif file_extension[-1] == "1":                                             # UNF1
        Size = 1
    elif file_extension[-1] == "2":                                             # UNF2
        Size = 2
    elif file_extension[-1] == "4":                                             # UNF4
        Size = 4
    else:
        print("The file is not an UNF type of file.")
        
    # Type of the file (the file extension UNF0, UNF1, UNF2 or UNF4)
    Type = str(file_extension)
    
    return nlayers, Size, Type

#%%
""" 2. Function to Read a Binary file (input filepath not just a file name)"""
import struct
def ReadBin(filepath, ng):                                                      # ng = Number of cells per layer to be read in the file (only land cells)
    Type = getFileInfo(filepath)[2]
    nbytes = getFileInfo(filepath)[1]
    nlayers = getFileInfo(filepath)[0]
    data = []
    with open(filepath, "rb") as file:
        for i in range(ng*nlayers):
            try:
                b = file.read(nbytes)
                if Type == "UNF0":                                              # Float data types
                    data.append(struct.unpack('>f', b)[0])
                    # data.append(struct.unpack('>d', b)[0])
                elif Type == "UNF1":                                            # Character string data types
                    # data.append(b.decode('UTF-8'))
                    data.append(int.from_bytes(b , byteorder = "big"))
                elif Type == "UNF2":                                            # Integer data types
                    data.append(int.from_bytes(b , byteorder = "big"))
                elif Type == "UNF4":                                            # Large integer data types ?
                    data.append(int.from_bytes(b , byteorder = "big"))
                else:                                                           # For other than UNF files assume items are of integer values
                    data.append(int.from_bytes(b , byteorder = "big"))
            except EOFError:
                break
    return data
#%%
""" 3. Function to transform the file to a multidimensional numpy array and to plot it """
import numpy as np
name = ["eu", "af","as","au","na","sa","wg2","wa","clm","clm025"]
ng = [180721, 371410, 841703, 109084, 461694, 226852, 66896, 67420,70412,281648]  # Total cells in the continent (Default)
nrow = [641,1090,1258,740,915,824,360,360,360,720]                                # Number of rows forming the matrix including water outside the continent (Default)
ncol = [1000,1237,4320,4309,1519,1356,720,720,720,1440]                           # Number of columns forming the matrix including water outside the continent (Default)

def FileToArray(file_path, GC_path, GR_path, continent_index,
                 continent_list = name, No_of_cells_list = ng, nrows_list = nrow, ncol_list= ncol):     # Default values  # indexing starts from zero                   

    nlayers = getFileInfo(file_path)[0]
    cellsInContinent =  No_of_cells_list[continent_index]
    file_values = ReadBin(file_path, cellsInContinent)
    GC = ReadBin(GC_path, cellsInContinent)
    GR = ReadBin(GR_path, cellsInContinent)
    ndarray = np.zeros((nlayers, nrow[continent_index], ncol[continent_index])) # (No. of layers, rows, columns)
    # ndarray = np.full((nlayers, nrow[continent_index], ncol[continent_index]), -9999) # (No. of layers, rows, columns)
    # for i in range(cellsInContinent*nlayers):  
    for i in range(cellsInContinent):
        for j in range(nlayers):                                                
            Ncol = GC[i]
            Nrow = GR[i]
            item = file_values[nlayers*(i-1) + j + nlayers]
            ndarray[j][Nrow-1][Ncol-1] = item                                   # -1 because index starts from zero unlike the provided data in GC and GR    
    return ndarray
#%%
""" Function to plot an array file using gdal"""

from osgeo import gdal
from osgeo import osr
# from osgeo import gdal_array
# import matplotlib.pylab as plt

def ArrayToRaster(array, outfile, xmin,ymax,xres,yres,ncols, nrows,
                  xrot = 0, yrot = 0, epsg = 4326):
    
    geotransform=(xmin,xres,xrot,ymax,yrot, -yres)
    output_raster = gdal.GetDriverByName('GTiff').Create(outfile,ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
    output_raster.SetGeoTransform(geotransform)                                  # Specify its coordinates
    srs = osr.SpatialReference()                                                 # Establish its coordinate encoding
    srs.ImportFromEPSG(epsg)                                                     # This one specifies WGS84 lat long.
    output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(array)   # Writes my array to the raster
    output_raster.FlushCache()
    return 

#%%

""" Function to Write a Binary file (only integers as a list)"""

def writeBin(filename, text, nbytes = 1):
    with open(filename, 'wb') as file:
        for b in text:
            file.write(b.to_bytes(nbytes, byteorder = "big"))
    return

# filename = "Ammanuel.bin"
# text = [3,5,2,5,8,25]
# writeBin(filename, text, nbytes = 1)
# ReadBin(filename, nbytes=1, nlayers = 1, ng=3)
#%%
def Path_Concatenate(first, year, last):
    result = first + str(year) + last 
    return result  
# first = r"U:\Codes\Europe_Input_UNF_Files\G_SURFACE_RUNOFF\G_SURFACE_RUNOFF_"
# year = 2016
# last = ".12.UNF0"
# Runoff_path = Path_Concatenate(first, year, last)
# print(Runoff_path)
# Runoff_path = r"U:\Codes\Europe_Input_UNF_Files\G_SURFACE_RUNOFF\G_SURFACE_RUNOFF_2016.12.UNF0" 

#%%
# def ReadClimateUNF0(filepath):
#     with open(filepath, mode='rb') as file: # b is important -> binary
#         fileContent = file.read()
#         data = []
#         for i in range(0, len(fileContent), 4): 
#             element = struct.unpack(">f", fileContent[i:i+4])[0]
#             data.append(element)
#     return data
            
# clim_dir2 = "U:\Codes\Europe_UNF_input_WaterGAP_Lite\ewembi"
# humidity = r"{}\GHUMIDITY_RELATIVE_1980_5.31.UNF0".format(clim_dir2)
# humid_data = ReadClimateUNF(humidity)