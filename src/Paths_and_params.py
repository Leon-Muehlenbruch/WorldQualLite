# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:15:59 2023

@author: tilahun
"""

""" 
Filtering Parameters
"""
run_type = 'Future' # 'Historical' or 'Future'
Scenario = 'SSP2'   # 'SSP1', 'SSP2', 'SSP5'
rcp = 'rcp6p0'  # 'rcp8p5', 'rcp2p6', 'rcp6p0'
GCM = 'MIROC5' # 'GFDL-ESM2M', 'HadGEM2-ES', 'IPSL-CM5a-LR', 'MIROC5'
data_source  = 'DB' # 'Excel' or 'DB'
# data_path = "U:/Paper_2/Updates_to_database/To be uploaded to database/0 FINAL"
data_path = r"U:\Paper_2\Updates_to_database\To be uploaded to database\09-10-2023_final_updated_data"


# if Scenario == 'SSP5':
#     Future_IDScen = 19
# elif Scenario == 'SSP1':
#     Future_IDScen = 18
# elif Scenario == 'SSP2':
#     Future_IDScen = 20

Future_IDScen = 27

initial_year = 2020
final_year_included = 2021
time_step = 10
parameter_id = 60                                                               # Phosphorus = 60 (read at wq_load_general database)
months = range(1,13)                                                            # February = 2 (months 1-12 means range(1,13))
country_id = 276                                                                # Country ID (read at wq_general database)
IDScen = 27 #3                                                                  # Scenario ID = 3 is for historical scenario
IDReg = 1                                                                       # eu=1, af=2, as=3, au=4,na=5,sa=6                                                                   
Basin_cells_list_csv_path =  r"U:\Codes\Python_codes\List_of_cells_in_Moehne_basin.csv" # Change it to your list of cells result from your Basindelineation.py run
# Basin_cells_list_csv_path =  r"U:\Codes\Python_codes\Example_cell.csv"
Point_load_corr = 1

name = ["eu", "af","as","au","na","sa","wg2","wa","clm","clm025"]
ng = [180721, 371410, 841703, 109084, 461694, 226852, 66896, 67420,70412,281648]  # Total cells in the continent (Default)
nrow = [641,1090,1258,740,915,824,360,360,360,720]                                # Number of rows forming the matrix including water outside the continent (Default)
ncol = [1000,1237,4320,4309,1519,1356,720,720,720,1440]                           # Number of columns forming the matrix including water outside the continent (Default)

continent_index = 0                                                             # index number of the continent from the list 'name' written below
dbname_cell = "globewq_wq_load_"+ name[continent_index]                           # Database name where cell inputs and parameters are stored for europe
dbname1 = "globewq_wq_load"                                                       # Database name where country inputs and parameters are stored 

""" Parameters """
# Lmax_calib = 0.04
# a_calib = 800            
# b_calib = -2             
# c_calib = 1.3e-8#3e-9 #7.78e-10       
# sc_corr_calib = 1#0.05 #1.06e-01   
# bg_corr_calib = 1#0.1 #5.55e-01 

Lmax_calib = 6.34e-02
a_calib = 900            
b_calib = -2             
c_calib = 1e-12#3e-9 #7.78e-10       
sc_corr_calib = 1#0.05 #1.06e-01   
bg_corr_calib = 1#0.1 #5.55e-01 


""" UNF files location folder (Path)"""

Surface_Runoff_folder = r"Europe_Input_UNF_Files\G_SURFACE_RUNOFF"                              # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input 
Urban_Runoff_folder = r"Europe_Input_UNF_Files\G_URBAN_RUNOFF"
Livestock_Density_folder = r"Europe_Input_UNF_Files\G_LIVESTOCK_NR"                             # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
Correction_Factor_folder = r"Europe_Input_UNF_Files\G_CORR_FACT_RTF"                            # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
P_Rate_ton_folder = r"Europe_Input_UNF_Files\P_RATE_TON_KM2"                   # /projects/WaterGAP/runs/jriverac/Ammanuel/Fertilizers/TP/eu/
CropLand_Corrected_folder = r"Europe_Input_UNF_Files\CROPLAND_CORR_KM2"        # /projects/WaterGAP/runs/jriverac/Ammanuel/Croplands/eu/
Other_UNF_files_folder = r"Europe_Input_UNF_Files\OTHER_UNF_FILES"                              # /projects/WaterGAP/data/irrigation_input/3.1/eu/

Future_UNF_files = r"Future_UNF_files"
"""
Files in Other_UNF_files folder
"""
# GC location in the cluster                                     # /projects/WaterGAP/data/hydro_input/3.1/eu/INPUT_ewembi
# GR location in the cluster                                     # /projects/WaterGAP/data/hydro_input/3.1/eu/INPUT_ewembi          
# Cell Area location in the cluster                              # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input                                  
# LandAreaPercentagePath                                         # Jaime sent it to me with email
# BuiltUP Ratio location in the cluster                          # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
# Soil Erosion location in the cluster                           # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
# P_atm_Dep location in the cluster                              # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
# PWeathering location in the cluster                            # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
