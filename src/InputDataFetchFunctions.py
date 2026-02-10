# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:06:05 2021

@author: tilahun
"""
""" Define a fuction to Load a database"""
import mysql.connector
import pandas as pd
def LoadDatabase(dbname):
    
    dbase = mysql.connector.connect(
    host = "134.147.42.33",
    user = "ammanuel",
    passwd = "Aqua$2020",
    database = dbname)  
    
    return dbase

""" Filtering Parameters"""

"""------->>>>>>> Basin_grid_cells, IDScen, time and dbname_cell should be filled here in this module as well as in WorldQual_Lite module"""

# parameter_id = 60                                                               # Phosphorus = 60 (read at wq_load_general database)
# for time in range(1993,2017):
time = 1992                                                                     # Considered year
# IDFAOReg = 4                                                                    # North America is region 4 (read at wq_load_general database)
# country_id = 276                                                                # Country ID of USA = 840 (read at wq_load_general database)
IDScen = 27                                                                      # Scenario ID = 9 is selected 
# cell = 80963                                                                   # Grid cell
# Basin_grid_cells = [80963,80964]
dbname_cell = "globewq_wq_load_eu"                                                 # Database name where cell inputs and parameters are stored 
# dbname1 = "globe_wq_load"                                                        # Database name where country inputs and parameters are stored 

""" 0. Cell Inputs """

def CellInputs(dbname, IDScen, time):    
    db = LoadDatabase(dbname)
    mycursor = db.cursor()

    query = "SELECT cell, pop_urb, pop_rur, pop_tot, rtf_man, rtf_dom, rtf_irr, gdp, salinity, humidity, lu \
            FROM cell_input \
            WHERE IDScen = %s AND time = %s"

    values = (IDScen, time)
    mycursor.execute(query, values) 
    return mycursor.fetchall()

# dataframe_cell_input = pd.DataFrame(CellInputs(dbname_cell, IDScen, time), columns = ["cell", "pop_urb", "pop_rur", "pop_tot", "rtf_man", "rtf_dom", "rtf_irr", "gdp", "salinity", "humidity", "lu"])
# dataframe_cell_input.to_csv(r"U:\Codes\Europe_Cell_Input_Files\europe_cell_input_"+str(time)+".csv")


def CellPopulation(dbname, IDScen, time, cell):    
    db = LoadDatabase(dbname)
    mycursor = db.cursor()

    query = "SELECT pop_urb, pop_rur, pop_tot\
           FROM cell_input \
           WHERE IDScen = %s AND time = %s AND cell = %s"

    values = (IDScen, time, cell)
    mycursor.execute(query, values) 
    return mycursor.fetchone()                                                 # Returns pop_urb, pop_rur, pop_tot respectively

def CellReturnFlows(dbname, IDScen, time, cell):    
    db = LoadDatabase(dbname)
    mycursor = db.cursor()

    query = "SELECT rtf_man, rtf_dom, rtf_irr\
           FROM cell_input \
           WHERE IDScen = %s AND time = %s AND cell = %s"

    values = (IDScen, time, cell)
    mycursor.execute(query, values) 
    return mycursor.fetchone()                                                 # Returns rtf_man, rtf_dom, rtf_ir respectively

def CellParameters(dbname, IDScen, time, cell):    
    db = LoadDatabase(dbname)
    mycursor = db.cursor()

    query = "SELECT gdp, salinity, humidity, lu \
           FROM cell_input \
           WHERE IDScen = %s AND time = %s AND cell = %s"

    values = (IDScen, time, cell)
    mycursor.execute(query, values) 
    return mycursor.fetchone()                                                 # Returns gdp, salinity, humidity, lu of cell respectively

""" 1. Emission Factor from Population (Kg|cap|year) and Phosphorus conc in return flows from manufacturing industries (mg/l) """

# def EmmisionFactorAndConcInReturnFlows(dbname, parameter_id, time, country_id): 
#     db = LoadDatabase(dbname)
#     mycursor = db.cursor()

#     query = "SELECT ef, conc_man_f, conc_man_t, conc_man_p, conc_man_c, conc_man_g, conc_man_m, conc_man_nd, c_geogen, conc_urb \
#            FROM country_parameter_input \
#            WHERE parameter_id = %s AND time = %s AND country_id = %s"
           
#     values = (parameter_id, time, country_id)                                      # (parameter_id, time, country_id)          
#     mycursor.execute(query, values)  
#     return mycursor.fetchone()       
                                                                                     
# [ef, conc_man_f, conc_man_t, conc_man_p, conc_man_c, conc_man_g, conc_man_m, conc_man_nd, c_geogen, conc_urb] \
#                     = EmmisionFactorAndConcInReturnFlows(dbname1, parameter_id, time, country_id)

def CountryConcInReturnFlows(dbname, parameter_id, time, country_id): 
    db = LoadDatabase(dbname)
    mycursor = db.cursor()

    query = "SELECT conc_man_f, conc_man_t, conc_man_p, conc_man_c, conc_man_g, conc_man_m, conc_man_nd, c_geogen, conc_urb \
           FROM country_parameter_input \
           WHERE parameter_id = %s AND time = %s AND country_id = %s"
           
    values = (parameter_id, time, country_id)                                     # (parameter_id, time, country_id)          
    mycursor.execute(query, values)  
    return mycursor.fetchone()                                                    # Returns concentration in return flows  (in mg/l)



def CountryEmmisionFactor(dbname, parameter_id, time, country_id): 
    db = LoadDatabase(dbname)
    mycursor = db.cursor()

    query = "SELECT ef \
           FROM country_parameter_input \
           WHERE parameter_id = %s AND time = %s AND country_id = %s"
           
    values = (parameter_id, time, country_id)                                     # (parameter_id, time, country_id)          
    mycursor.execute(query, values)  
    return mycursor.fetchone()   

""" 2. Population of the country, return flows (m3/a) and Connectivity to treatment plants (%) """


def CountryPopulation(dbname, IDScen, time, country_id):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()
    
    query = "SELECT pop_tot, pop_urb, pop_rur\
               FROM country_input \
               WHERE IDScen = %s AND time = %s AND country_id = %s"
               
    values = (IDScen, time, country_id)   
    mycursor.execute(query, values) 
    return mycursor.fetchone()

def CountryReturnFlows(dbname, IDScen, time, country_id):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()
    
    query = "SELECT rtf_man, fra_man_f, fra_man_t, fra_man_p, fra_man_c, fra_man_g, fra_man_m, fra_man_nd, rtf_dom, rtf_irr \
               FROM country_input \
               WHERE IDScen = %s AND time = %s AND country_id = %s"
               
    values = (IDScen, time, country_id)   
    mycursor.execute(query, values) 
    return mycursor.fetchone()

def CountryConnectionToTreatment(dbname, IDScen, time, country_id):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()
    
    query = "SELECT con_prim, con_sec, con_tert, con_untr, stp_failure, to_treat_and_unknown, to_hanging_t, to_open_def, UrbSewerConn, RurSewerConn, SPO_treat, con_quat\
               FROM country_input \
               WHERE IDScen = %s AND time = %s AND country_id = %s"
               
    values = (IDScen, time, country_id)   
    mycursor.execute(query, values) 
    return mycursor.fetchone()                                                 

""" 3. Nutrient Removal Rate, Soil Parameters and Temperature Parameters  """

# def RemovalRateSoilParametersAndTemperatureParameters(dbname, IDScen, time, parameter_id):
#     db = LoadDatabase(dbname)
#     mycursor = db.cursor()   
     
#     query = "SELECT rem_prim, rem_sec, rem_tert, rem_untr, treat_failure, rem_soil, red_fac_org, red_fac_inor, k_storage, k_soil, ks, \
#                 sed_veloc, ke_tss_reg_alpha, ke_tss_reg_beta, teta, teta_lake\
#            FROM parameter_input \
#            WHERE IDScen = %s AND time = %s AND parameter_id = %s "
           
#     values = (IDScen, time, parameter_id)
#     mycursor.execute(query, values) 
#     return mycursor.fetchone()

# [rem_prim, rem_sec, rem_tert, rem_untr, treat_failure, rem_soil, red_fac_org, red_fac_inor, k_storage, k_soil, ks, \
#  sed_veloc, ke_tss_reg_alpha, ke_tss_reg_beta, teta, teta_lake] \
#     = RemovalRateSoilParametersAndTemperatureParameters(dbname1, IDScen, time, parameter_id)
    
def RemovalRate(dbname, IDScen, time, parameter_id):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()   
     
    query = "SELECT rem_prim, rem_sec, rem_tert, rem_untr, treat_failure, rem_soil, red_fac_org, red_fac_inor, rem_quat\
           FROM parameter_input \
           WHERE IDScen = %s AND time = %s AND parameter_id = %s "
           
    values = (IDScen, time, parameter_id)
    mycursor.execute(query, values) 
    return mycursor.fetchone()

def SoilParametersForFC(dbname, IDScen, time, parameter_id):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()   
     
    query = "SELECT k_storage, k_soil, ks, sed_veloc, ke_tss_reg_alpha, ke_tss_reg_beta, teta, teta_lake\
           FROM parameter_input \
           WHERE IDScen = %s AND time = %s AND parameter_id = %s "
           
    values = (IDScen, time, parameter_id)
    mycursor.execute(query, values) 
    return mycursor.fetchone()

def TemperatureParameters(dbname, IDScen, time, parameter_id):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()   
     
    query = "SELECT teta, teta_lake\
           FROM parameter_input \
           WHERE IDScen = %s AND time = %s AND parameter_id = %s "
           
    values = (IDScen, time, parameter_id)
    mycursor.execute(query, values) 
    return mycursor.fetchone()
""" 4. Nutrient(N and P) Application Rate in the form of fertilizers (tons/km2) for 21 crop types"""

def Fertilizer_P_ApplicationRate(dbname, country_id, time):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()
    
    query = "SELECT rate_P\
           FROM ind_fert_use_input \
           WHERE country_id = %s AND YearFrom = %s AND crop_type_id = %s"
    rate_P = []
    for crop_type_id in range(21):
        values = (country_id, time, crop_type_id)
        mycursor.execute(query, values) 
        v = mycursor.fetchone()[0]
        rate_P.append(v)
    return rate_P

def Fertilizer_N_ApplicationRate(dbname, country_id, time):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()
    
    query = "SELECT rate_N\
           FROM ind_fert_use_input \
           WHERE country_id = %s AND YearFrom = %s AND crop_type_id = %s"
    rate_N = []
    for crop_type_id in range(21):
        values = (country_id, time, crop_type_id)
        mycursor.execute(query, values) 
        v = mycursor.fetchone()[0]
        rate_N.append(v)
    return rate_N

""" 5. Livestock Excretion rate"""

def LivestockExcretionRate(dbname, parameter_id, IDFAOReg):   
    db = LoadDatabase(dbname)
    mycursor = db.cursor()
    
    query = "SELECT ls_exr_rate\
           FROM ls_exr_input \
           WHERE parameter_id = %s AND IDFAOReg = %s AND LS = %s"

    ls_exr_rate = []
    for LS in range(12):    
        values = (parameter_id, IDFAOReg, LS)
        mycursor.execute(query, values) 
        ls_exr_rate.append(mycursor.fetchone()[0])
    return ls_exr_rate

# ls_exr_rate = LivestockExcretionRate(dbname1, parameter_id, IDFAOReg)

""" 6. Geogenic Background deposition rate """

def GeogenicBackgroundDeposition(dbname, parameter_id, lu):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()
    
    query = "SELECT geo_back\
               FROM geogenic_background_input \
               WHERE parameter_id = %s AND LU = %s"
               
    values = (parameter_id, lu)
    mycursor.execute(query, values) 
    return mycursor.fetchone()[0]

# lu = CellParameters(dbname_cell, IDScen, time, cell)[3]
# geo_back = GeogenicBackgroundDeposition(dbname1, parameter_id, lu)


""" Cell_id to GCRC Conversion"""

def Cell_ID_To_GCRC(cell, IDReg, dbname = "watergap_unf"):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()   
     
    query = "SELECT cell_land_water\
           FROM gcrc \
           WHERE IDVersion = 3 AND cell = %s AND IDReg = %s "
           
    values = (cell, IDReg)
    mycursor.execute(query, values) 
    return mycursor.fetchone()[0]

""" Crop type from GLCC"""

def Crop_ID_From_GLCC(GLCC, dbname = "wq_general"):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()   
     
    query = "SELECT crop_type_id\
           FROM _crop_type \
           WHERE GLCC = %s"
    Valid_GLCC_list = range(101,118)
    if ((GLCC in Valid_GLCC_list) and (GLCC != 108)) or GLCC==999:
        values = (GLCC,)
        mycursor.execute(query, values)
        crop_type_id = mycursor.fetchone()
    else:
        crop_type_id = -9999   
    return crop_type_id

# crop_type_id = Crop_ID_From_GLCC(108)

""" IDFaoReg from Country_Id"""

def IDFaoReg_from_Country_Id(country_id, dbname = "wq_general"):
    db = LoadDatabase(dbname)
    mycursor = db.cursor()   
     
    query = "SELECT IDFAOReg \
           FROM _country \
           WHERE country_id = %s "
    values = (country_id,)   
    mycursor.execute(query, values)
    return mycursor.fetchone()[0]
# country_id = 840
# gg = IDFaoReg_from_Country_Id(country_id)