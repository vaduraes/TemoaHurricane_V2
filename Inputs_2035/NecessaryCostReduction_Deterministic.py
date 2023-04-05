import datetime as dt
import os
from ConvertNPZ_2TEMOA import TEMOA_INPUTS, WriteTEMOA_File
import pandas as pd
import sqlite3
import numpy as np

def getCapacity (NewSQLFile):
    SQL = sqlite3.connect(NewSQLFile[:-4]+".sqlite")
    CapacityALL = pd.read_sql_query("SELECT * from Output_CapacityByPeriodAndTech", SQL)
    CapacityOcean = CapacityALL[CapacityALL.tech == "GeneralOcean"]
    CapacityOcean2035 = CapacityOcean[CapacityOcean.t_periods == 2035]["capacity"]

    
    if len(CapacityOcean2035)!=0:
        CapacityOcean2035=float(CapacityOcean2035)
    else:
        CapacityOcean2035=0
        
    SQL.close()    
    return CapacityOcean2035


# CAPEX, OPEX, CF_TEMOA,LCOE,TotalInstalledCap=TEMOA_INPUTS(LOCE_target, PathCapex_Opex_And_Simulations,PathPortOPT_Result, StartDate)
# WriteTEMOA_File(CAPEX, OPEX, CF_TEMOA, BaseDukeFile, NewSQLFile)

LOCE_target="L" #H, M, L -> high, medium, low (LCOE)
PathCapex_Opex_And_Simulations="./Inputs/Original_Inputs/"
NewSQLFile="./temoatools/temoa_stochastic/data_files/Duke_CapEx.sql"
StartDate=dt.datetime(2009,1,1,0) #Start Date of the datasets used
BaseDukeFile="./Inputs/Original_Inputs/Duke_CapEx.sql"#path



# PathPortOPT_Result="PortfolioOptimizationWindWaveOcean(0_0_50).npz"
# Case_Study="(0_0_50)_"

AllPathsResults=[
    "PortfolioOptimizationWindWaveOcean(0_0_50).npz"]

NameAllCases=[
    "_(0_0_50)"]

MinInput=np.array([0.1,0.08,0.21,0.12])
MaxInput=np.array([0.24,0.21,0.45,0.28])

Count=-1
for PathPortOPT_Result, Case_Study in zip(AllPathsResults,NameAllCases):
    
    CAPEX, OPEX, CF_TEMOA, LCOE, TotalInstalledCap=TEMOA_INPUTS(LOCE_target, PathCapex_Opex_And_Simulations,PathPortOPT_Result, StartDate)
    TotalInstalledCap=np.sum(TotalInstalledCap)
    
    Count+=1
    Year=2035

    Case=LOCE_target+"_"+Case_Study + str(Year)
    file_object = open("Record_"+Case+".txt", 'w')
    file_object.close()

    #Maybe multiply by 1.5 if the technology is cheap
    Capex_Max=CAPEX*MaxInput[Count]
    Opex_Max=OPEX*MaxInput[Count]

    Capex_Min=CAPEX*MinInput[Count]
    Opex_Min=OPEX*MinInput[Count]
    
    CAPEX_R=(Capex_Max+Capex_Min)/2
    OPEX_R=(Opex_Max+Opex_Min)/2    
        
    for i in range(10):
        
        WriteTEMOA_File(CAPEX_R, OPEX_R, CF_TEMOA, BaseDukeFile, NewSQLFile)

        PWD=os.getcwd()
        os.chdir(PWD+'/temoatools/temoa_stochastic')
        os.system('conda run -n Temoa python temoa_model/ --config=temoa_model/config_sample')
        os.chdir('../..')

        CapacityOcean2035 = getCapacity(NewSQLFile)

        Generation=CapacityOcean2035
        if CapacityOcean2035>=TotalInstalledCap:
            Capex_Min=CAPEX_R
            Opex_Min=OPEX_R
        else:
            Capex_Max=CAPEX_R
            Opex_Max=OPEX_R

        file_object = open("Record_"+Case+".txt", 'a')
        file_object.write("LCOE:;"+str(LCOE)+";"+str(100-100*CAPEX_R/CAPEX)+";Generation [GW:];"+str(Generation)+"\n")
        file_object.close()
        
        CAPEX_R=(Capex_Max+Capex_Min)/2
        OPEX_R=(Opex_Max+Opex_Min)/2
        
        if (Capex_Max-Capex_Min)/CAPEX<0.008:
            break
            
            
            
            
            
            
            