# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 12:14:17 2023

@author: tilahun
"""

import time as tm
start_run_time = tm.time()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

from InputDataFetchFunctions import CountryEmmisionFactor
from InputDataFetchFunctions import CountryConcInReturnFlows
from InputDataFetchFunctions import CountryPopulation
from InputDataFetchFunctions import CountryReturnFlows
from InputDataFetchFunctions import CountryConnectionToTreatment
from InputDataFetchFunctions import RemovalRate
from InputDataFetchFunctions import Cell_ID_To_GCRC
from InputDataFetchFunctions import IDFaoReg_from_Country_Id
from BinaryFileHandler import ReadBin
from BinaryFileHandler import Path_Concatenate
from InputDataFetchFunctions import LivestockExcretionRate

import Paths_and_params as PP

""" Domestic Sewered """

def DomesticSewered(country_tot_pop, country_urb_pop, country_rur_pop, cell_urb_pop, cell_rur_pop, con_prim, con_sec, con_tert, con_untr,
                     rem_prim, rem_sec, rem_tert, rem_untr, stp_failure, ef, Cell_monthly_correction_factor, con_urb, con_rur, con_quat, rem_quat):  
    

    total_connection = con_prim + con_sec + con_tert + con_untr + con_quat
    
    frac_prim = con_prim / total_connection * 100
    frac_sec = con_sec / total_connection * 100 
    frac_tert = con_tert / total_connection * 100 
    frac_quat = con_quat / total_connection * 100
    frac_treat_unknown = con_untr / total_connection * 100
    
    Ld_ds_before_treatment_country = ef * ((country_urb_pop * con_urb/100) + (country_rur_pop * con_rur/100)) / 1000  # in tons/year    
    
    if stp_failure is not None and not math.isnan(stp_failure):
        Leftover_percentage_after_Treatment = frac_prim / 100 * (100 - rem_prim*stp_failure/100) / 100 + \
                        frac_sec / 100 * (100 - rem_sec*stp_failure/100) / 100 + \
                        frac_tert / 100 * (100 - rem_tert*stp_failure/100) / 100 + \
                        frac_quat / 100 * (100 - rem_quat*stp_failure/100) / 100 + \
                        frac_treat_unknown / 100 * (100 - rem_untr) / 100 
    else:
        Leftover_percentage_after_Treatment = frac_prim / 100 * (100 - rem_prim) / 100 + \
                        frac_sec / 100 * (100 - rem_sec) / 100 + \
                        frac_tert / 100 * (100 - rem_tert) / 100 + \
                        frac_quat / 100 * (100 - rem_quat) / 100 + \
                        frac_treat_unknown / 100 * (100 - rem_untr) / 100
                    
    Ld_ds_treated_country_yearly = Ld_ds_before_treatment_country * Leftover_percentage_after_Treatment
    
    Ld_ds_cell_yearly = ef * ((cell_urb_pop * con_urb/100) + (cell_rur_pop * con_rur/100)) / 1000 * Leftover_percentage_after_Treatment * Cell_monthly_correction_factor
    Ld_ds_cell_monthly = Ld_ds_cell_yearly / 12
    
    return Ld_ds_cell_monthly, Ld_ds_cell_yearly, Ld_ds_treated_country_yearly  

""" Manufacturing Loads"""

def Manufacturing(country_rtf_man, cell_rtf_man, Conc_mf, con_sec, con_tert, rem_sec, rem_tert, stp_failure, Cell_monthly_correction_factor):
            
    if con_sec == None or con_tert == None:
        frac_sec = 50
        frac_tert = 50
    else:
        frac_sec = con_sec / (con_sec + con_tert)  * 100
        frac_tert = con_tert / (con_sec + con_tert)  * 100
        
    Ld_mf_untreated_country = Conc_mf * country_rtf_man / 1000000  # to convert to tons/year
    
    if stp_failure is not None and not math.isnan(stp_failure):
        Leftover_percentage_after_Treatment =  \
        frac_sec/100*(100 - rem_sec*stp_failure/100)/100 + frac_tert/100*(100 - rem_tert*stp_failure/100)/100
    else:
        Leftover_percentage_after_Treatment =  \
        frac_sec/100*(100 - rem_sec)/100 + frac_tert/100*(100 - rem_tert)/100
    
    # Only secondary and tertiary treatment plants are considered and for european industries 100 % of it is assumed to be connected both to secondary and tertiary plants (Williams paper)       
    Ld_mf_treated_country = Ld_mf_untreated_country * Leftover_percentage_after_Treatment
    if country_rtf_man is not None and country_rtf_man != 0:
        Ld_mf_cell_yearly = Ld_mf_treated_country * cell_rtf_man / country_rtf_man * Cell_monthly_correction_factor
    else:
        country_rtf_man = 1000000000
        Ld_mf_cell_yearly = Ld_mf_treated_country * cell_rtf_man / country_rtf_man * Cell_monthly_correction_factor
        print("Error: Invalid country_rtf_man value encountered. A value of 10e9 is assumed.")
    Ld_mf_cell_monthly =  Ld_mf_cell_yearly / 12   
    return Ld_mf_cell_monthly , Ld_mf_cell_yearly                                                     # monthly Phosphorus load on a grid cell in tons

""" Calculation of Eroded portion coefficient to be applied on inorganic Fertilizers, Livestock and Atmospheric deposition loadings """

def Cell_Yearly_ErodedPortion(cell, IDReg, SoilErosionData, MeanRunoff_Data,
                        Yearly_Runoff_Data, Lmax_value, a, b, c, Cell_GCRC):            # Check the values of Lmax, a, b, c from Fink                            
    
    # Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)      
    Cell_yearRunoff = Yearly_Runoff_Data[Cell_GCRC-1] 
    Cell_meanRunoff = MeanRunoff_Data[Cell_GCRC-1]                              # From waterGAP hydrology model  
    SI = SoilErosionData[Cell_GCRC-1]
    
    Cell_eroded_portion_yearly = ((Lmax_value / (1 + (Cell_yearRunoff/a)**(b) )) + 
                                  (SI * c * Cell_yearRunoff / Cell_meanRunoff)) #* Cell_net_Area
       
    return Cell_eroded_portion_yearly

def Cell_Yearly_to_monthly_Load_Converter(cell, country_id, IDReg, month, Actual_Surface_Runoff, Yearly_Actual_Surface_Runoff, Cell_GCRC):
    # Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg) 
    # Yearly_Actual_Surface_Runoff is a single yearly layer data while Actual_Surface_Runoff is a 12 months layer data
    Cell_monthly_Actual_Surface_Runoff = Actual_Surface_Runoff[12*Cell_GCRC + month - 13]
    # Cell_ActSurfaceRunoffSummer = ActSurfaceRunoffSummer[Cell_GCRC-1]
    Cell_monthly_to_yearly_ratio = Cell_monthly_Actual_Surface_Runoff / Yearly_Actual_Surface_Runoff[Cell_GCRC-1]
    # Cell_monthly_to_yearly_ratio = Cell_monthly_Actual_Surface_Runoff / Cell_ActSurfaceRunoffSummer
    return Cell_monthly_to_yearly_ratio

""" Inorganic Fertilizers """

def Inorganic_Fertilizer_new_method(cell, IDReg, P_rate_ton_Data, CropLand_Corrected_Data, BuiltUPRatioData,
                         Eroded_portion, yearly_to_monthly_coeficient, Cell_GCRC):
    # Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)
    P_rate_ton_km2 = P_rate_ton_Data[Cell_GCRC-1]
    Cell_CropLand_area = CropLand_Corrected_Data[Cell_GCRC-1]
    BuiltUP_Ratio_Cell = BuiltUPRatioData[Cell_GCRC-1]
    
    Cell_Ld_inorg_yearly = P_rate_ton_km2 * Eroded_portion * Cell_CropLand_area * (1 - BuiltUP_Ratio_Cell)
    Cell_monthly_inorg_load = Cell_Ld_inorg_yearly * yearly_to_monthly_coeficient   # in tons/month
    return Cell_monthly_inorg_load, Cell_Ld_inorg_yearly , P_rate_ton_km2

""" Agricultural TP Loading from Manure of Livestock """

def AgricultureLivestock(cell, country_id, IDReg, Livestock_densityData, ls_exr_rate,
                         Eroded_portion, yearly_to_monthly_coeficient, Cell_GCRC):            # Check the values of Lmax, a, b, c from Fink                            
    
    # Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)
    
    ex =[]
    j = 0
    for i in range(12*(Cell_GCRC-1) , 12*Cell_GCRC):
            ex.append(Livestock_densityData[i] * ls_exr_rate[j])
            j = j+1
    F_org = sum(ex)
            
    Cell_Ld_org_yearly = F_org * Eroded_portion                           # in tons/year/cell

    Cell_monthly_org_load = Cell_Ld_org_yearly *  yearly_to_monthly_coeficient          # in tons/month/cell
    
    return Cell_monthly_org_load, Cell_Ld_org_yearly 

""" Domestic Non-Sewered / Scattered Settlements"""
        
def DomesticNonsewered(ef, cell_rur_pop, cell_urb_pop, country_urb_pop, country_rur_pop, country_tot_pop, 
                       to_treat_and_unknown, to_hanging_t, to_open_def, rem_untr, 
                       con_prim, rem_prim, con_sec, rem_sec, con_tert, rem_tert, 
                       con_untr, stp_failure, SPO_treated, yearly_to_monthly_coeficient, treat_failure, con_urb, con_rur, con_quat, rem_quat):

    if to_treat_and_unknown == None or math.isnan(to_treat_and_unknown):
        to_treat_and_unknown = 0
    if to_hanging_t == None or math.isnan(to_hanging_t):
        to_hanging_t = 0
    if to_open_def == None or math.isnan(to_open_def):
        to_open_def = 0
    if SPO_treated == None or math.isnan(SPO_treated):
        SPO_treated = 0  
    if treat_failure == None or math.isnan(treat_failure):
        treat_failure = 0
        
    if stp_failure is not None and not math.isnan(stp_failure):
        stp_failure = 0
        
    total_connection = con_prim + con_sec + con_tert + con_untr + con_quat
    
    if ( (100-con_urb)>-0.0001 and (100-con_urb)<0.0001 ):  # to take care of floating pt error (it just means con_urb==100 percent)
        x = 0.0
    else:
        x = 100-con_urb                                                        # not connected urban percentage (w/c means scattered)
        
    if ( (100-con_rur)>-0.002 and (100-con_rur)<0.002 ):
        y = 0.0
    else:
        y = 100-con_rur                                                        # not connected rural percentage (w/c means scattered)
       
    NotConnectedPeople = ((country_urb_pop * x/100) + (country_rur_pop * y/100))
    
    ld_untr_sc = ef * NotConnectedPeople / 1000  
    
    if to_hanging_t != None and to_open_def != None and to_treat_and_unknown != None:
        # (if detailed information is given)
        sum_ld_sc = to_treat_and_unknown + to_hanging_t + to_open_def
        if (100 - (total_connection + sum_ld_sc)) > -0.0001 and (100 - (total_connection + sum_ld_sc)) < 0.0001:
            miss_con_rate = 0
        else:
            miss_con_rate = 100 - total_connection - sum_ld_sc
        sum_ld_sc += miss_con_rate
        if sum_ld_sc != 0:
            ld_diff_untr_sc = to_open_def / (sum_ld_sc / 10000)
            ld_treat_sc = (SPO_treated /(sum_ld_sc/100)) * (100 - rem_sec*treat_failure/100) +\
                    ((to_treat_and_unknown + miss_con_rate -SPO_treated)/(sum_ld_sc/100))*(100.0-treat_failure)
        else:
            ld_treat_sc = 0
            
    else: # Less detailed information is available assume only primary and secondary work
        if total_connection == 0:
            frac_sec = 100
            frac_prim = 0
            frac_tert = 0
            frac_quat = 0
            frac_treat_unknown = 0
        else: 
            frac_prim = con_prim / total_connection * 100
            frac_sec = (con_sec  + con_tert + frac_quat)/ total_connection * 100 
            frac_tert = 0
            frac_quat = 0
            frac_treat_unknown = con_untr / total_connection * 100
 
        ld_diff_untr_sc = frac_treat_unknown * (100 - rem_untr) / 100
        if treat_failure != 0:
            ld_treat_sc = frac_prim * (100 - rem_prim*treat_failure/100) / 100 + \
                        frac_sec / 100 * (100 - rem_sec*treat_failure/100) / 100 + \
                        frac_tert / 100 * (100 - rem_tert*treat_failure/100) / 100 + \
                        frac_quat / 100 * (100 - rem_quat*treat_failure/100) / 100
        else:
            ld_treat_sc = frac_prim * (100 - rem_prim) / 100 + \
                        frac_sec / 100 * (100 - rem_sec) / 100 + \
                        frac_tert / 100 * (100 - rem_tert) / 100 + \
                        frac_quat / 100 * (100 - rem_quat) / 100
        
    ld_treat_sc *= ld_untr_sc / 10000
    ld_diff_untr_sc *= ld_untr_sc / 10000                
    ld_hanging_l = (ld_untr_sc * to_hanging_t / (sum_ld_sc / 100)) / 100 
    
    # Downscale to cell level
    ld_treat_sc_cell = ld_treat_sc * ((cell_urb_pop *( 1-con_urb / 100)) + (cell_rur_pop * (1-con_rur / 100))) / (country_tot_pop*(1 - total_connection/100))
        
    ld_untr_sc_cell = ld_untr_sc * ((cell_urb_pop * x / 100) + (cell_rur_pop * y / 100)) / (country_tot_pop*(1 - total_connection/100))
                                      
    ld_diff_untr_sc_cell = ld_diff_untr_sc * ((cell_urb_pop * x / 100) + (cell_rur_pop * y / 100)) / (country_tot_pop*(1 - total_connection/100))

    ld_hanging_l_cell = ld_hanging_l * ((cell_urb_pop * x / 100) + (cell_rur_pop * y / 100)) / (country_tot_pop*(1 - total_connection/100))
    ld_treat_sc_cell_monthly = yearly_to_monthly_coeficient * ld_treat_sc_cell
    
    return ld_treat_sc_cell_monthly, ld_treat_sc_cell, ld_untr_sc_cell, ld_hanging_l_cell, ld_diff_untr_sc_cell                                                  # monthly Phosphorus load on a grid cell in tons

""" Atmospheric Deposition Phosphorus Loading"""

def BackgroundAtm(cell, country_id, IDReg, P_atm_Dep_Data,
                  Eroded_portion, yearly_to_monthly_coeficient,
                  GR_Data, Area_Data, Land_Area_PercentageData, BuiltUPRatioData, Cell_GCRC):            # Check the values of Lmax, a, b, c from Fink                            
    
    # Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)
    
    Fatm = P_atm_Dep_Data[Cell_GCRC-1]
    
    Cell_GR = GR_Data[Cell_GCRC-1]
    Cell_Area = Area_Data[Cell_GR-1]
    
    Cell_Land_Area = Cell_Area * int(Land_Area_PercentageData[Cell_GCRC-1]) / 100
    BuiltUP_Ratio_Cell = BuiltUPRatioData[Cell_GCRC-1]
    Cell_net_Area = Cell_Land_Area*(1-BuiltUP_Ratio_Cell)
        
    Cell_Ld_atm_yearly = Fatm * Eroded_portion * Cell_net_Area / 1000                                        # in tons/year/cell
    
    Cell_monthly_atm_load = Cell_Ld_atm_yearly * yearly_to_monthly_coeficient         # in tons/month/cell
    
    return Cell_monthly_atm_load, Cell_Ld_atm_yearly 


"""Background Chemical Weathering Phosphorus Loading"""

def BackgroundCW(cell, country_id, IDReg, PWeathering_Data, Area_Data, Land_Area_PercentageData, BuiltUPRatioData,
                 Yearly_Runoff_Data, MeanRunoff_Data, yearly_to_monthly_coeficient, Cell_GCRC, GR_Data):

    # Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)
    Ld_cw = PWeathering_Data[Cell_GCRC-1]
    
    Cell_GR = GR_Data[Cell_GCRC-1]
    Cell_Area = Area_Data[Cell_GR-1]
    
    Cell_Land_Area = Cell_Area * int(Land_Area_PercentageData[Cell_GCRC-1]) / 100
    BuiltUP_Ratio_Cell = BuiltUPRatioData[Cell_GCRC-1]
    Cell_net_Area = Cell_Land_Area*(1-BuiltUP_Ratio_Cell)
    
    Cell_yearRunoff = Yearly_Runoff_Data[Cell_GCRC-1] 
    Cell_meanRunoff = MeanRunoff_Data[Cell_GCRC-1]
    
    Ld_cw_yearly = Ld_cw * Cell_yearRunoff/Cell_meanRunoff * Cell_net_Area / 1000
    Ld_cw_monthly = Ld_cw_yearly * yearly_to_monthly_coeficient
    return Ld_cw_monthly, Ld_cw_yearly                                                          # in tons/cell/year

""" Urban Surface Runoff Phosphorus Loading"""

def UrbanSurfaceRunoff(cell, country_id, IDReg, month, UrbanRunoffData, EventMeanConc, Area_Data, Land_Area_PercentageData, BuiltUPRatioData,
                       con_prim, con_sec, con_tert, con_untr, rem_prim, rem_sec, rem_tert, rem_untr, stp_failure, Cell_GCRC, GR_Data, con_quat, rem_quat): 
    
    total_connection = con_prim + con_sec + con_tert + con_untr + con_quat
    frac_prim = con_prim / total_connection * 100
    frac_sec = con_sec / total_connection * 100 
    frac_tert = con_tert / total_connection * 100
    frac_quat = con_quat / total_connection * 100
    frac_treat_unknown = con_untr / total_connection * 100  
    
    
    # Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)   

    Cell_monthly_Urban_Surface_Runoff = UrbanRunoffData[12*Cell_GCRC + month - 13] 
                      
    # Rus_cell = UrbanRunoffData[Cell_GCRC-1]  # which month?
    
    Cell_GR = GR_Data[Cell_GCRC-1]
    Cell_Area = Area_Data[Cell_GR-1]  
    Cell_Land_Area = Cell_Area * Land_Area_PercentageData[Cell_GCRC-1] / 100
    BuiltUP_Ratio_Cell = BuiltUPRatioData[Cell_GCRC-1]

    Ld_usr = Cell_monthly_Urban_Surface_Runoff * EventMeanConc * Cell_Land_Area * BuiltUP_Ratio_Cell / 1000
    
    if stp_failure is not None and not math.isnan(stp_failure):
    
        Ld_usr_cell = Ld_usr * frac_prim / 100 * (100 - rem_prim*stp_failure/100) / 100 + \
                     Ld_usr * frac_sec / 100 * (100 - rem_sec*stp_failure/100) / 100 + \
                     Ld_usr * frac_tert / 100 * (100 - rem_tert*stp_failure/100) / 100 + \
                     Ld_usr * frac_quat / 100 * (100 - rem_quat*stp_failure/100) / 100 + \
                     Ld_usr * frac_treat_unknown / 100 * (100 - rem_untr) / 100
    else:
        Ld_usr_cell = Ld_usr * frac_prim / 100 * (100 - rem_prim) / 100 + \
                     Ld_usr * frac_sec / 100 * (100 - rem_sec) / 100 + \
                     Ld_usr * frac_tert / 100 * (100 - rem_tert) / 100 + \
                     Ld_usr * frac_quat / 100 * (100 - rem_quat) / 100 + \
                     Ld_usr * frac_treat_unknown / 100 * (100 - rem_untr) / 100
                
    return Ld_usr_cell     # monthly phosphorus load in


def Load_After_Retention_factor(HL, a_ret = 13.2, b_ret = -0.93):
    return 1 / (1 + a_ret*HL**b_ret) if HL!= 0 else 1

print("Functions definition completed.")

""" 
Filtering Parameters
"""

initial_year = PP.initial_year
final_year_included = PP.final_year_included
years = range(initial_year,final_year_included+1)
parameter_id = PP.parameter_id                                  # Phosphorus = 60 (read at wq_load_general database)
months = PP.months                                              # February = 2 (months 1-12 means range(1,13))
country_id = PP.country_id                                      # Country ID (read at wq_general database)
IDScen = PP.IDScen                                              # Scenario ID = 9 is selected 
dbname_cell = PP.dbname_cell                                    # Database name where cell inputs and parameters are stored for europe
dbname1 = PP.dbname1                                            # Database name where country inputs and parameters are stored 
continent_index = PP.continent_index                            # index number of the continent from the list 'name' written below
IDReg = 1                                                       # eu=1, af=2, as=3, au=4,na=5,sa=6                                                                   
Point_load_corr = PP.Point_load_corr


name = PP.name
ng =  PP.ng                                                     # Total cells in the continent (Default)
nrow =  PP.nrow                                                 # Number of rows forming the matrix including water outside the continent (Default)
ncol =  PP.ncol                                                 # Number of columns forming the matrix including water outside the continent (Default)


Basin_cells_with_percentage = pd.read_csv(PP.Basin_cells_list_csv_path)                                                                   # Cell_id (Grid cell)
Basin_grid_cells = list(Basin_cells_with_percentage['Cell_ID'])
years = range(initial_year,final_year_included+PP.time_step, PP.time_step)
IDFAOReg = IDFaoReg_from_Country_Id(country_id)                                 # OECD from Database= "wq_general" and Table= "_fao_reg"


GLCC_path = PP.Other_UNF_files_folder + "/GLCC2000.UNF2"
GC_path = PP.Other_UNF_files_folder +  "/GC.UNF2"
GR_path = PP.Other_UNF_files_folder +  "/GR.UNF2"
CellAreaPath = PP.Other_UNF_files_folder + "/GAREA.UNF0"
LandAreaPercentagePath = PP.Other_UNF_files_folder + "/G_LAND_AREA.UNF1"
BuiltUPRatioPath = PP.Other_UNF_files_folder + "/GBUILTUP.UNF0"
SoilErosionPath = PP.Other_UNF_files_folder + "/G_SOILEROS.UNF0"
MeanRunoff_path = PP.Surface_Runoff_folder + "/G_SURFACE_RUNOFF_MEAN.UNF0"
Gfreqw_path = PP.Other_UNF_files_folder + "/GFREQW.UNF1"                             # Water area percentage in the cells
P_atm_Dep_Path = PP.Other_UNF_files_folder + "/G_PATMDEPOS.UNF0"
PWeathering_Path = PP.Other_UNF_files_folder + "/G_PWEATHERING.UNF0"


# GLCC_data = ReadBin(GLCC_path, ng[continent_index])
GR_Data = ReadBin(GR_path, ng[continent_index])                                 # List of Row of each cell ordered by GCRC of each cell
MeanRunoff_Data = ReadBin(MeanRunoff_path, ng[continent_index])
Area_Data = ReadBin(CellAreaPath, nrow[continent_index])                        # Ordered by cell row
Land_Area_PercentageData = ReadBin(LandAreaPercentagePath, ng[continent_index])
BuiltUPRatioData = ReadBin(BuiltUPRatioPath, ng[continent_index])
SoilErosionData = ReadBin(SoilErosionPath, ng[continent_index])
Gfreqw_Data = ReadBin(Gfreqw_path, ng[continent_index])                  # Percentage of water area in each cell
P_atm_Dep_Data = ReadBin(P_atm_Dep_Path, ng[continent_index])
PWeathering_Data = ReadBin(PWeathering_Path, ng[continent_index])


""" 
Actual Calculations
"""
 
def Model(X):                            # X is list of TP Erosion parameters (Lmax, a, b, c)
    
    Mean_Squared_Error_list = []
    
    column_names_monthly_sum = ['Year', 'DomesticSeweredLoad', 'Scattered Load', 'ManufacturingLoad',
                                'InorganicFertilizerLoad', 'AgricultureLivestockLoad', 'AtmBackgroundLoad',
                                'CWBackgroundLoad', 'UrbanSurfaceRunoffLoad', 'SummedLoadings']
        
    monthly_sum_by_year = pd.DataFrame(columns = column_names_monthly_sum)
    
    for time in years:
        
        """"Cell Input files folder"""
        
        if PP.run_type == 'Future':
            df_continent_cell_input = pd.read_csv(Path_Concatenate(r"U:\Paper_2\Updates_to_database\To be uploaded to database\0 FINAL\cell_input\EU\{}\europe_cell_input_".format(PP.Scenario),time,".csv"))
        elif PP.run_type == 'Historical':
            df_continent_cell_input = pd.read_csv(Path_Concatenate(r"U:\Codes\Europe_Cell_Input_Files\europe_cell_input_",time,".csv"))
        
        """ UNF files location in the folder (Path)"""
        if PP.run_type == 'Historical':
            Runoff_path = Path_Concatenate(PP.Surface_Runoff_folder + "/G_SURFACE_RUNOFF_", time, ".12.UNF0")
            UrbanRunoffPath = Path_Concatenate(PP.Urban_Runoff_folder + "/G_URBAN_RUNOFF_", time, ".12.UNF0")
            Livestock_Density_Path = Path_Concatenate(PP.Livestock_Density_folder + "/G_LIVESTOCK_NR_", time, ".12.UNF0") # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
            Correction_Factor_Path = Path_Concatenate(PP.Correction_Factor_folder + "/G_CORR_FACT_RTF_", time, ".12.UNF0")
            P_Rate_ton_path = Path_Concatenate(PP.P_Rate_ton_folder + "/P_RATE_TON_KM2_", time, ".UNF0")
            CropLand_Corrected_Path = Path_Concatenate(PP.CropLand_Corrected_folder + "/CROPLAND_CORR_KM2_", time, ".UNF0")
        elif PP.run_type == 'Future':
            Runoff_path = Path_Concatenate(PP.Future_UNF_files + '/Hydrology/' + PP.name[continent_index] + '/' + PP.rcp + '_' + PP.GCM + "/G_SURFACE_RUNOFF_", time, ".12.UNF0")
            UrbanRunoffPath = Path_Concatenate(PP.Future_UNF_files + '/Hydrology/' + PP.name[continent_index] + '/' + PP.rcp + '_' + PP.GCM + "/G_URBAN_RUNOFF_", time, ".12.UNF0")
            Livestock_Density_Path = Path_Concatenate(PP.Future_UNF_files + '/LIVESTOCK_NR/' + PP.Scenario + '/' + PP.name[continent_index] + '/' + "/G_LIVESTOCK_NR_", time, ".12.UNF0") # /projects/WaterGAP/runs/jriverac/globewq_loadings/TP/eu/input
            Correction_Factor_Path = Path_Concatenate(PP.Future_UNF_files + '/correction_factors/' + PP.rcp + '_' + PP.Scenario + '/' + PP.name[continent_index] + '/' + PP.GCM + "/G_CORR_FACT_RTF_", time, ".12.UNF0")
            P_Rate_ton_path = Path_Concatenate(PP.Future_UNF_files + '/P_RATE_TON_KM2/' + PP.Scenario + '/' + PP.name[continent_index] + "/P_RATE_TON_KM2_"+PP.Scenario+"_",time,"_"+PP.name[continent_index]+".UNF0")
            CropLand_Corrected_Path = Path_Concatenate(PP.Future_UNF_files + '/CROPLAND_AREA_KM2/' + PP.Scenario + '/' + PP.name[continent_index] + "/"+PP.Scenario+"_",time, "_5arcmin_cropland_"+PP.name[continent_index]+".UNF0")
            
        """"Erosion Parameters"""
        Lmax = X[0]
        a = X[1]
        b = X[2]
        c = X[3]
        sc_corr = X[4]
        bg_corr = X[5]
        
        """ Input Data processing from UNF Files """
                                                                           
        Runoff_Data = ReadBin(Runoff_path, ng[continent_index])                         # Monthly Data
        UrbanRunoffData = ReadBin(UrbanRunoffPath, ng[continent_index])                 # Monthly Data
        Livestock_densityData = ReadBin(Livestock_Density_Path, ng[continent_index])
        Correction_Factor_Data = ReadBin(Correction_Factor_Path, ng[continent_index])   # Monthly Data
        P_rate_ton_Data = ReadBin(P_Rate_ton_path, ng[continent_index])
        CropLand_Corrected_Data = ReadBin(CropLand_Corrected_Path, ng[continent_index])
        
        print("Input data from UNF files have been fetched without error.")
        print("Pre-processing of input data in progress . . .")
        
        Actual_Surface_Runoff = []
        zip_object = zip(Runoff_Data, UrbanRunoffData)
        for list1_i, list2_i in zip_object:
            difference = list1_i-list2_i
            if difference < 0:
                difference = 0
            Actual_Surface_Runoff.append(difference)
            
        Yearly_Runoff_Data = []
        Yearly_Actual_Surface_Runoff = []
        ActSurfaceRunoffSummer = []
        for i in range(0 , len(Runoff_Data) , 12):
            Yearly_Runoff_Data.append(sum(Runoff_Data[i:(i+12)]))
            Yearly_Actual_Surface_Runoff.append(sum(Actual_Surface_Runoff[i:(i+12)]))
            ActSurfaceRunoffSummer.append(sum(Actual_Surface_Runoff[(i+1):(i+9)]))     # Second to nineth month
        
        """ Input data processing from the Database"""
        if PP.data_source  == 'DB':
            country_urb_pop = CountryPopulation(dbname1, IDScen, time, country_id)[1]
            country_rur_pop = CountryPopulation(dbname1, IDScen, time, country_id)[2]
            country_tot_pop = CountryPopulation(dbname1, IDScen, time, country_id)[0]
            country_urb_pop_percentage = country_urb_pop / country_tot_pop * 100
            # country_rur_pop_percentage = country_rur_pop / country_tot_pop * 100
            
            ef = CountryEmmisionFactor(dbname1, parameter_id, time, country_id)[0]            # Kg/cap/year
            # ef = 0.4
            con_prim = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[0]                 # In percentage
            con_sec = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[1]                  # In percentage
            con_tert = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[2]                 # In percentage
            con_untr = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[3]                 # In percentage   
            stp_failure = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[4]              # In percentage 
            con_quat = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[11]
            con_quat = (con_quat if con_quat is not None else 0)
            con_tot = con_prim + con_sec + con_tert + con_untr + con_quat                                           # Total connected percentage of the country
            
              
            rem_prim = RemovalRate(dbname1, IDScen, time, parameter_id)[0]
            rem_sec = RemovalRate(dbname1, IDScen, time, parameter_id)[1]
            rem_tert = RemovalRate(dbname1, IDScen, time, parameter_id)[2]
            rem_quat = RemovalRate(dbname1, IDScen, time, parameter_id)[8]
            rem_quat = (rem_quat if rem_quat is not None else 0)
            rem_untr = RemovalRate(dbname1, IDScen, time, parameter_id)[3]
            treat_failure = RemovalRate(dbname1, IDScen, time, parameter_id)[4]
            to_treat_and_unknown = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[5] 
            to_hanging_t = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[6] 
            to_open_def = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[7]
            UrbSewerConn = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[8]
            RurSewerConn = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[9]
            SPO_treated = CountryConnectionToTreatment(dbname1, IDScen, time, country_id)[10]
            
            country_rtf_man = CountryReturnFlows(dbname1, IDScen, time, country_id)[0]        # mg/l
            Conc_mf = CountryConcInReturnFlows(dbname1, parameter_id, time, country_id)[6]    # conc_man_nd (mg/l)
            EventMeanConc = CountryConcInReturnFlows(dbname1, parameter_id, time, country_id)[8]     # Event mean concentration (conc_urb)

        elif PP.data_source  == 'Excel':
            df_country_input = pd.read_csv(PP.data_path + r"\country_input\{}_country_input.csv".format(PP.Scenario))
            df_country_parameter_input = pd.read_csv(PP.data_path + r"\country_parameter_input\{}_country_parameter_input.csv".format(PP.Scenario))
            df_parameter_input = pd.read_csv(PP.data_path + r"\parameter_input\{}_parameter_input.csv".format(PP.Scenario))
            
            """Country input (Population and connections to treatment)""" 
            criteria = (df_country_input['IDScen'] == PP.Future_IDScen) & (df_country_input['country_id'] == country_id) & (df_country_input['time'] == time)
            
            # Access the value using the .loc[] method
            country_urb_pop = df_country_input.loc[criteria, 'pop_urb'].iloc[0]
            country_rur_pop = df_country_input.loc[criteria, 'pop_rur'].iloc[0]
            country_tot_pop = df_country_input.loc[criteria, 'pop_tot'].iloc[0]
            country_urb_pop_percentage = country_urb_pop / country_tot_pop * 100
            
            
            con_prim = df_country_input.loc[criteria, 'con_prim'].iloc[0]
            con_sec = df_country_input.loc[criteria, 'con_sec'].iloc[0]
            con_tert = df_country_input.loc[criteria, 'con_tert'].iloc[0]
            con_quat = df_country_input.loc[criteria, 'con_quat'].iloc[0]
            con_untr = df_country_input.loc[criteria, 'con_untr'].iloc[0]
            stp_failure = df_country_input.loc[criteria, 'stp_failure'].iloc[0]
            country_rtf_man = df_country_input.loc[criteria, 'rtf_man'].iloc[0]
            con_tot = con_prim + con_sec + con_tert + con_untr
            
            to_treat_and_unknown = df_country_input.loc[criteria, 'to_treat_and_unknown'].iloc[0]
            to_hanging_t = df_country_input.loc[criteria, 'to_hanging_t'].iloc[0]
            to_open_def = df_country_input.loc[criteria, 'to_open_def'].iloc[0]
            UrbSewerConn = df_country_input.loc[criteria, 'UrbSewerConn'].iloc[0]
            RurSewerConn = df_country_input.loc[criteria, 'RurSewerConn'].iloc[0]
            SPO_treated = df_country_input.loc[criteria, 'SPO_treat'].iloc[0]
            
            """Country parameter input"""
            criteria2 = (df_country_parameter_input['IDScen'] == PP.Future_IDScen) & (df_country_parameter_input['country_id'] == country_id)\
                        & (df_country_parameter_input['parameter_id'] == parameter_id) & (df_country_parameter_input['time'] == time)
            
            ef = df_country_parameter_input.loc[criteria2, 'ef'].iloc[0]
            Conc_mf = df_country_parameter_input.loc[criteria2, 'conc_man_nd'].iloc[0]
            EventMeanConc = df_country_parameter_input.loc[criteria2, 'conc_urb'].iloc[0]
            
            """parameter input"""
            
            criteria3 = (df_parameter_input['IDScen'] == PP.Future_IDScen) & (df_parameter_input['parameter_id'] == parameter_id) & (df_parameter_input['time'] == time)
            
            rem_prim = df_parameter_input.loc[criteria3, 'rem_prim'].iloc[0]
            rem_sec = df_parameter_input.loc[criteria3, 'rem_sec'].iloc[0]
            rem_tert = df_parameter_input.loc[criteria3, 'rem_tert'].iloc[0]
            rem_untr = df_parameter_input.loc[criteria3, 'rem_untr'].iloc[0]
            treat_failure = df_parameter_input.loc[criteria3, 'treat_failure'].iloc[0]
            rem_quat = df_parameter_input.loc[criteria3, 'rem_quat'].iloc[0]
        else:
            "Define the source of sanitation and pop data in the Paths_and_params.py"


        # if country_urb_pop_percentage < con_tot:                                                # To give priority for urban population
        #     con_urb = 100                                                                       # Percentage of Urban population connected to sewer
        #     con_rur = country_rur_pop/country_tot_pop * (con_tot - country_urb_pop_percentage)  # Percentage of Rural population connected to sewer
        # else:
        #     con_rur = 0                                                                         # Percentage of Rural population connected to sewer
        #     con_urb = country_tot_pop/country_urb_pop * con_tot                                 # Percentage of Urban population connected to sewer
        
        if country_tot_pop ==0:
            con_rur = 0
            con_urb = 0      
        elif country_rur_pop == 0:
            con_rur = 0
            con_urb = UrbSewerConn
        elif country_urb_pop ==0:
            con_rur = RurSewerConn
            con_urb = 0
        else:
            con_rur = RurSewerConn
            con_urb = UrbSewerConn
        
        ls_exr_rate = LivestockExcretionRate(dbname1, parameter_id, IDFAOReg)
           
        print("Preprocessing of the input data from UNF files has been done without error.")
        
        """ Summed Phosphorus Loading Yearly"""
        column_names = ['Cell_ID', 'Month', 'DomesticSeweredLoad', 'Scattered Load','ManufacturingLoad', 'InorganicFertilizerLoad', 
                          'AgricultureLivestockLoad', 'AtmBackgroundLoad', 'CWBackgroundLoad', 'UrbanSurfaceRunoffLoad','SummedLoadings']
        
        df_summary = pd.DataFrame(columns = column_names)
        
        """Calculation of Basin Hydraulic Load """
        Basin_Water_Surface_Area = 0
        Basin_annual_runoff = 0
        for cell in Basin_grid_cells:
            Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)
            Cell_GR = GR_Data[Cell_GCRC-1]
            percentage_part_of_cell_in_the_basin = float(Basin_cells_with_percentage[Basin_cells_with_percentage['Cell_ID'] == cell]['Portion of Cell in Basin (%)'])
            Cell_Water_Area = Gfreqw_Data[Cell_GCRC-1] / 100 * Area_Data[Cell_GR-1] * percentage_part_of_cell_in_the_basin/ 100.823 # Km2
            Basin_Water_Surface_Area = Basin_Water_Surface_Area + Cell_Water_Area
            cell_annual_runoff_Km3 = Yearly_Runoff_Data[Cell_GCRC-1] /(10**6) * Area_Data[Cell_GR-1] * percentage_part_of_cell_in_the_basin /100.823 # Km3
            Basin_annual_runoff = Basin_annual_runoff + cell_annual_runoff_Km3
        HL = Basin_annual_runoff/ Basin_Water_Surface_Area * 1000  if Basin_Water_Surface_Area != 0 else 0             # Km3 / Km2 = Km = 1000m
        retention_factor  = Load_After_Retention_factor(HL)
        
        """Calculation of TP Loads """
        
        for cell in Basin_grid_cells:
            is_cell = df_continent_cell_input['cell']== cell
            cell_urb_pop = df_continent_cell_input[is_cell]["pop_urb"].item()
            cell_rur_pop = df_continent_cell_input[is_cell]["pop_rur"].item()
            # cell_tot_pop = df_continent_cell_input[is_cell]["pop_tot"].item()
            cell_rtf_man = df_continent_cell_input[is_cell]["rtf_man"].item()                # (m3/year)
            # print("Cell man return flow is {}".format(cell_rtf_man))
            Cell_GCRC = Cell_ID_To_GCRC(cell, IDReg)
            urbanloadyearly = 0  # initialization
            
            
            for month in months:
        
                Cell_monthly_correction_factor = Correction_Factor_Data[12*Cell_GCRC + month - 13]
                
                # DomesticSeweredLoad = DomesticSewered(country_tot_pop, country_urb_pop, country_rur_pop, cell_urb_pop, cell_rur_pop, con_prim, con_sec, 
                #              con_tert, con_untr, rem_prim, rem_sec, rem_tert, rem_untr, stp_failure, ef, Cell_monthly_correction_factor, con_urb, con_rur)
                DomesticSeweredLoad = DomesticSewered(country_tot_pop, country_urb_pop, country_rur_pop, cell_urb_pop, cell_rur_pop, con_prim, con_sec, con_tert, con_untr,
                      rem_prim, rem_sec, rem_tert, rem_untr, stp_failure, ef, Cell_monthly_correction_factor, con_urb, con_rur, con_quat, rem_quat)
                # print(DomesticSeweredLoad[0])
                ManufacturingLoad = Manufacturing(country_rtf_man, cell_rtf_man, Conc_mf, con_sec, 
                                          con_tert, rem_sec, rem_tert, stp_failure, Cell_monthly_correction_factor)
        
                Eroded_portion = Cell_Yearly_ErodedPortion(cell, IDReg, SoilErosionData, MeanRunoff_Data,
                                Yearly_Runoff_Data, Lmax, a, b, c, Cell_GCRC)              # Check the values of Lmax, a, b, c from Fink  
                yearly_to_monthly_coeficient = Cell_Yearly_to_monthly_Load_Converter(cell, country_id, IDReg, month, 
                                                                             Actual_Surface_Runoff, Yearly_Actual_Surface_Runoff, Cell_GCRC)
                InorganicFertilizerLoad = Inorganic_Fertilizer_new_method(cell, IDReg, P_rate_ton_Data, CropLand_Corrected_Data, BuiltUPRatioData,
                                 Eroded_portion, yearly_to_monthly_coeficient, Cell_GCRC) 
        
                AgricultureLivestockLoad = AgricultureLivestock(cell, country_id, IDReg, Livestock_densityData, ls_exr_rate,
                                                        Eroded_portion, yearly_to_monthly_coeficient, Cell_GCRC)
        
                Scattered__treated_Load = DomesticNonsewered(ef, cell_rur_pop, cell_urb_pop, country_urb_pop, country_rur_pop, country_tot_pop,
                               to_treat_and_unknown, to_hanging_t, to_open_def, rem_untr, 
                               con_prim, rem_prim, con_sec, rem_sec, con_tert, rem_tert, 
                               con_untr, stp_failure, SPO_treated, yearly_to_monthly_coeficient, treat_failure, con_urb, con_rur, con_quat, rem_quat)[0:2]
        
                BackgroundAtmLoad = BackgroundAtm(cell, country_id, IDReg, P_atm_Dep_Data,
                          Eroded_portion, yearly_to_monthly_coeficient,
                          GR_Data, Area_Data, Land_Area_PercentageData, BuiltUPRatioData, Cell_GCRC)
        
                BackgroundCWLoad = BackgroundCW(cell, country_id, IDReg, PWeathering_Data, Area_Data, Land_Area_PercentageData, BuiltUPRatioData,
                         Yearly_Runoff_Data, MeanRunoff_Data, yearly_to_monthly_coeficient, Cell_GCRC, GR_Data)
        
                UrbanSurfaceRunoffLoad =  UrbanSurfaceRunoff(cell, country_id, IDReg, month, UrbanRunoffData, EventMeanConc, Area_Data, Land_Area_PercentageData, BuiltUPRatioData,
                               con_prim, con_sec, con_tert, con_untr, rem_prim, rem_sec, rem_tert, rem_untr, stp_failure, Cell_GCRC, GR_Data, con_quat, rem_quat)
                SummedLoadings = DomesticSeweredLoad[0]*Point_load_corr + Scattered__treated_Load[0] * sc_corr + ManufacturingLoad[0]*Point_load_corr +\
                        InorganicFertilizerLoad[0] + AgricultureLivestockLoad[0] + BackgroundAtmLoad[0] +\
                            BackgroundCWLoad[0] * bg_corr + UrbanSurfaceRunoffLoad
                urbanloadyearly += UrbanSurfaceRunoffLoad
                
                """
                Save monthly load results to df_summary by appending results form each month (iteration) run to it
                """
                resulting_data = {'Cell_ID': [cell], 'Month':[month],'DomesticSeweredLoad': [DomesticSeweredLoad[0]*Point_load_corr], 'Scattered Load' : [Scattered__treated_Load[0] * sc_corr],
                          'ManufacturingLoad': [ManufacturingLoad[0]*Point_load_corr], 'InorganicFertilizerLoad': [InorganicFertilizerLoad[0]], 
                          'AgricultureLivestockLoad': [AgricultureLivestockLoad[0]], 'AtmBackgroundLoad': [BackgroundAtmLoad[0]], 'CWBackgroundLoad': [BackgroundCWLoad[0] *bg_corr], 
                          'UrbanSurfaceRunoffLoad': [UrbanSurfaceRunoffLoad],
                          'SummedLoadings': [SummedLoadings] }
                df = pd.DataFrame(resulting_data)
                # df_summary = df_summary.append(df)
                df_summary = pd.concat([df_summary, df])
        
                
                print("Loadings Calculation for cell " + str(cell) + " for year " + str(time) +" for month " + str(month) + " has been completed.")
                
            """
            Save yearly results to df_summary by appending yearly total load values for each cell    
            """
            SummedLoadingsYear = DomesticSeweredLoad[1]*Point_load_corr + Scattered__treated_Load[1] * sc_corr + ManufacturingLoad[1]*Point_load_corr +\
                        InorganicFertilizerLoad[1] + AgricultureLivestockLoad[1] + BackgroundAtmLoad[1] +\
                            BackgroundCWLoad[1] * bg_corr + urbanloadyearly
            resulting_data_yearly = {'Cell_ID': [cell], 'Month':["Yearly load"],'DomesticSeweredLoad': [DomesticSeweredLoad[1]*Point_load_corr], 'Scattered Load' : [Scattered__treated_Load[1] * sc_corr],
                          'ManufacturingLoad': [ManufacturingLoad[1]*Point_load_corr], 'InorganicFertilizerLoad': [InorganicFertilizerLoad[1]], 
                          'AgricultureLivestockLoad': [AgricultureLivestockLoad[1]], 'AtmBackgroundLoad': [BackgroundAtmLoad[1]], 'CWBackgroundLoad':[BackgroundCWLoad[1] * bg_corr], 
                          'UrbanSurfaceRunoffLoad': [urbanloadyearly],'SummedLoadings': [SummedLoadingsYear] }
            df2 = pd.DataFrame(resulting_data_yearly)
            # df_summary = df_summary.append(df2)
            df_summary = pd.concat([df_summary, df2])
            
        """
        # Some cells are not fully in the basin  therefore Multiply the resulting values for each cell by their respective percentage portion of the cells lying inside the basin because 
        """
        
        lookup_percentage = np.dot(
                        (df_summary['Cell_ID'].values[:,None] == Basin_cells_with_percentage['Cell_ID'].values), # If this is true,
                        Basin_cells_with_percentage['Portion of Cell in Basin (%)']    # Then, give this as an output
                        )
        df_summary['Percentage of cell in the basin'] = lookup_percentage
        
        # df_summary = df_summary[['DomesticSeweredLoad', 'Scattered Load','ManufacturingLoad', 'InorganicFertilizerLoad', 
        #             'AgricultureLivestockLoad', 'BackgroundLoad', 'UrbanSurfaceRunoffLoad','SummedLoadings']].multiply(df_summary['Percentage of cell in the basin'], axis="index")
        df_summary.loc[:,['DomesticSeweredLoad', 'Scattered Load','ManufacturingLoad', 'InorganicFertilizerLoad', 
                     'AgricultureLivestockLoad', 'AtmBackgroundLoad', 'CWBackgroundLoad','UrbanSurfaceRunoffLoad','SummedLoadings']] = df_summary.loc[:,['DomesticSeweredLoad', 'Scattered Load','ManufacturingLoad', 'InorganicFertilizerLoad', 
                     'AgricultureLivestockLoad', 'AtmBackgroundLoad','CWBackgroundLoad', 'UrbanSurfaceRunoffLoad','SummedLoadings']].multiply(df_summary.loc[:, 'Percentage of cell in the basin'] / 100.823, axis="index") # Fully in grid cells are 100.823 percent inside (there is some error in the data)
        
                                                                                                                                                         
        """
        # Multiply the total load by retention factor to account for load retained(sedimented) in water bodies 
        """                                                                                                                           
        df_summary.loc[:,['DomesticSeweredLoad', 'Scattered Load','ManufacturingLoad', 'InorganicFertilizerLoad', 
             'AgricultureLivestockLoad', 'AtmBackgroundLoad', 'CWBackgroundLoad', 'UrbanSurfaceRunoffLoad','SummedLoadings']] = df_summary.loc[:,['DomesticSeweredLoad', 'Scattered Load','ManufacturingLoad', 'InorganicFertilizerLoad', 
             'AgricultureLivestockLoad', 'AtmBackgroundLoad', 'CWBackgroundLoad', 'UrbanSurfaceRunoffLoad','SummedLoadings']].multiply(retention_factor, axis="index")

        """
        Accumulate the resulting cell by cell load results to a catchment level by summing them up
        """
                                                                                                                                                  # df_summary_copy = df_summary.copy()                                                                                                                           
        df_summary = df_summary.drop(['Cell_ID','Percentage of cell in the basin'], axis = 1)

        monthly_sum = df_summary.groupby(['Month']).sum(numeric_only= False)
        
        monthly_sum['Year'] = time
        # shift column 'Year' to first position
        first_column = monthly_sum.pop('Year')
  
        # insert column using insert(position,column_name,first_column) function
        monthly_sum.insert(0, 'Year', first_column)
        monthly_sum = monthly_sum.drop('Yearly load')    # Drop the last row (yearly load)
        
        """
        Append the resulting table to 'monthly_sum_by_year' dataframe on every iteration (year)
        """
        monthly_sum_by_year = pd.concat([monthly_sum_by_year, monthly_sum])
        
        monthly_sum_by_year['Month'] = monthly_sum_by_year.index
        second_column = monthly_sum_by_year.pop('Month')
        monthly_sum_by_year.insert(1, 'Month', second_column)

    return monthly_sum_by_year

# initial_Lmax = 9e-02        # 0.0669481343     # 0.131   # 0.035        # 0.04
# initial_a = 1000            # 900                    # 800
# initial_b = -2              # -2      # -2
# initial_c = 1.445e-10       # 3.03744285e-10 # 1.96e-10           # 3e-10          # 1.3e-8   4.27e-10
# initial_sc_corr = 1.5e-02   # 1.34752459e-02 # 9.31e-2     # 0.01   1 in the original model 0.005
# initial_bg_corr = 6.556e-01 # 8.24970607e-01 # 9.31e-2
#                                                     # Multiply domestic and manufacturing loadds by this factor

# initial_guess = [initial_Lmax, initial_a, initial_b, initial_c, initial_sc_corr, initial_bg_corr]

# Lmax_calib = 6.34e-02
# a_calib = 900            
# b_calib = -2             
# c_calib = 1e-12#3e-9 #7.78e-10       
# sc_corr_calib = 0.005#0.05 #1.06e-01   
# bg_corr_calib = 0.8#0.1 #5.55e-01 

Lmax_calib = PP.Lmax_calib
a_calib = PP.a_calib            
b_calib = PP.b_calib             
c_calib = PP.c_calib#3e-9 #7.78e-10       
sc_corr_calib = PP.sc_corr_calib#0.05 #1.06e-01   
bg_corr_calib = PP.bg_corr_calib#0.1 #5.55e-01 

calib_params = [Lmax_calib, a_calib, b_calib, c_calib, sc_corr_calib, bg_corr_calib] 
Predicted_df2 = Model(calib_params)

end_run_time = tm.time()
print("The time it took to run the model is ", round(end_run_time - start_run_time, 2), " Seconds")

"""
# Save the monthly and yearly results to csv files
"""
# Predicted_df2.to_csv(r'U:\Codes\WorldQual_Lite_Run_Outputs\Moehne_Basin\Calibrated_with_2002_2016_after_point_load_corr.csv')

Predicted_df2[['DomesticSeweredLoad', 'Scattered Load',
        'ManufacturingLoad', 'InorganicFertilizerLoad',
        'AgricultureLivestockLoad', 'AtmBackgroundLoad', 'CWBackgroundLoad',
        'UrbanSurfaceRunoffLoad', 'SummedLoadings']
              ] = Predicted_df2[
        ['DomesticSeweredLoad', 'Scattered Load',
        'ManufacturingLoad', 'InorganicFertilizerLoad',
        'AgricultureLivestockLoad', 'AtmBackgroundLoad', 'CWBackgroundLoad',
        'UrbanSurfaceRunoffLoad', 'SummedLoadings']].astype(float)
                  
Predicted_df2_yearly = Predicted_df2.groupby('Year').sum()
Predicted_df2_yearly = Predicted_df2_yearly.drop(['Month', 'SummedLoadings'], axis=1)

# Reorder columns
Predicted_df2_yearly = Predicted_df2_yearly.reindex(columns=['DomesticSeweredLoad', 'ManufacturingLoad', 'Scattered Load',
       'InorganicFertilizerLoad', 'AgricultureLivestockLoad',
       'AtmBackgroundLoad', 'CWBackgroundLoad', 'UrbanSurfaceRunoffLoad'])

Predicted_df2_yearly.to_csv('U:/trial2_yearly.csv')
#%%
"""
Stacked bar Plot for predicted result by Month and year
"""
df_to_plot = Predicted_df2_yearly
ax = df_to_plot.plot(kind='bar', stacked=True)

# Set the chart title and axis labels
ax.set_title('TP Load')
ax.set_xlabel('Year')
ax.set_ylabel('TP load (ton)')

# Display the chart
plt.show()
#%%
"""
RMSE calculation
"""
Mesaured_Data = pd.read_excel(r"U:\Codes\Creating_own_model\Measured_Loading_Moehne_2002_2016.xlsx")  # 2002 - 2016
merged_df = pd.merge(Predicted_df2, Mesaured_Data, on=['Year', 'Month'])

from sklearn.metrics import mean_squared_error
RMSE = np.sqrt(mean_squared_error(merged_df['TP Load (tons)'], merged_df['SummedLoadings']))

import scipy.stats as stats
r, p = stats.pearsonr(merged_df['TP Load (tons)'], merged_df['SummedLoadings'])
Rsquared = r**2

print('RMSE =', np.round(RMSE,2), 'R2 =', np.round(Rsquared, 2))


"""
Compare measured vs simulated with plot
"""
# Merge the two DataFrames on the 'Year' column

merged_df['YearMonth'] = merged_df['Year'].astype(str) + '-' + merged_df['Month'].astype(str)
# Plot the two columns as a line plot
plt.plot(merged_df['YearMonth'], merged_df['SummedLoadings'], label='Simulated')
plt.plot(merged_df['YearMonth'], merged_df['TP Load (tons)'], label='Measured')

# Adjust the tick frequency and rotation
plt.xticks(merged_df['YearMonth'][::6], rotation=45)

# Add axis labels and a legend
plt.xlabel('Year')
plt.ylabel('TP Load (ton/month)')
plt.legend()

plt.text(2, 6.5, f'R2 = {Rsquared:.2f}\nRMSE = {RMSE:.2f}', fontsize=10, color='green')

# Show the plot
plt.show()


