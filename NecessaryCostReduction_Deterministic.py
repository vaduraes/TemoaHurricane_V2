import datetime as dt
import os
from ConvertNPZ_2TEMOA import TEMOA_INPUTS, WriteTEMOA_File
from InputFragilityEffect_Exploration import InputFragilityCurveEffect
import pandas as pd
import sqlite3
import numpy as np

def getCapacity (NewSQLFile, Year):
    SQL = sqlite3.connect(NewSQLFile[:-4]+".sqlite")
    CapacityALL = pd.read_sql_query("SELECT * from Output_CapacityByPeriodAndTech", SQL)
    CapacityOcean = CapacityALL[CapacityALL.tech == "GeneralOcean"]
    CapacityOcean = CapacityOcean[CapacityOcean.t_periods == Year]["capacity"]

    
    if len(CapacityOcean)!=0:
        CapacityOcean=float(CapacityOcean)
    else:
        CapacityOcean=0
        
    SQL.close()    
    return CapacityOcean


LOCE_target="L" #H, M, L -> high, medium, low (LCOE)
PathCapex_Opex_And_Simulations="./Inputs_2035/Original_Inputs/"
NewSQLFile="./temoatools/temoa_stochastic/data_files/Duke_CapEx.sql"
StartDate=dt.datetime(2009,1,1,0) #Start Date of the datasets used
BaseDukeFile="./Inputs_2035/Original_Inputs/Duke_CapEx.sql"#
FragilityDataPath="FragilityData.npz"



##########################
#Year_s=[2030,2035,2050] #Change General_SQL_OCEAN_Structure_2035 in ConvertNPZ_2TEMOA.py and Years in InputFragilityEffect.py
Year_s=[2035]
#Year_s=[2035,2030,2050]
##########################



# PathPortOPT_Result="PortfolioOptimizationWindWaveOcean(0_0_50).npz"
# Case_Study="(0_0_50)_"

# AllPathsResults=[
#     "PortfolioOptimizationWindWaveOcean(0_0_50).npz",
#     "PortfolioOptimizationWindWaveOcean(0_100_0).npz",
#     "PortfolioOptimizationWindWaveOcean(50_0_0).npz",
#     "PortfolioOptimizationWindWaveOcean(50_100_50).npz"]

# NameAllCases=[
#     "_(0_0_50)",
#     "_(0_100_0)",
#     "_(50_0_0)",
#     "_(50_100_50)"]

AllPathsResults=[
    "PortfolioOptimizationWindWaveOcean(0_0_50).npz"]

# AllPathsResults=[
#     "PortfolioOptimizationWindWaveOcean(50_0_0).npz"]

NameAllCases=[
    "_(0_0_50)"]

# NameAllCases=[
#     "_(50_0_0)"]

MinInput=np.array([0,0,0,0,0,0,0,0])
MaxInput=np.array([1,1,1,1,1,1,1,1])

for Year in Year_s:
    Count=-1
    for PathPortOPT_Result, Case_Study in zip(AllPathsResults,NameAllCases):
        
        CAPEX, OPEX, CF_TEMOA, LCOE, TotalInstalledCap=TEMOA_INPUTS(LOCE_target, PathCapex_Opex_And_Simulations,PathPortOPT_Result, StartDate)
        TotalInstalledCap=np.sum(TotalInstalledCap)
        
        Count+=1
        Case=LOCE_target+"_"+Case_Study + str(Year)
        file_object = open("Record_"+Case+".txt", 'w')
        file_object.close()
    
        # CAPEX=CAPEX*54.25/247.9
        # OPEX=OPEX*54.25/247.9
        #Maybe multiply by 1.5 if the technology is cheap
        Capex_Max=CAPEX*MaxInput[Count]
        Opex_Max=OPEX*MaxInput[Count]
    
        Capex_Min=CAPEX*MinInput[Count]
        Opex_Min=OPEX*MinInput[Count]
        
        CAPEX_R=(Capex_Max+Capex_Min)/2
        OPEX_R=(Opex_Max+Opex_Min)/2    
            
        for i in range(100):
            
            WriteTEMOA_File(CAPEX_R, OPEX_R, CF_TEMOA, BaseDukeFile, NewSQLFile)
            #InputFragilityCurveEffect(NewSQLFile, FragilityDataPath)
    
            PWD=os.getcwd()
            os.chdir(PWD+'/temoatools/temoa_stochastic')
            os.system('conda run -n Temoa python temoa_model/ --config=temoa_model/config_sample')
            os.chdir('../..')
    
            CapacityOcean = getCapacity(NewSQLFile, Year)
    
            Generation=CapacityOcean
            
            file_object = open("C:/Users/Remote/Desktop/Projects/OceanProject4_2_Moh/Code/TEMOA_Stochastic/Results/Deterministic_2035/Record_"+Case+".txt", 'a')
            file_object.write("LCOE:;"+str(LCOE)+";"+str(100-100*CAPEX_R/CAPEX)+";Generation [GW:];"+str(Generation)+"\n")
            file_object.close()
            
            if CapacityOcean>=TotalInstalledCap:
                Capex_Min=CAPEX_R
                Opex_Min=OPEX_R
            else:
                Capex_Max=CAPEX_R
                Opex_Max=OPEX_R
    

            
            CAPEX_R=(Capex_Max+Capex_Min)/2
            OPEX_R=(Opex_Max+Opex_Min)/2
            
            if (Capex_Max-Capex_Min)/CAPEX<0.00000000005:
                break
            