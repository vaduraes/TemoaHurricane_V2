#Usefull to first understands the effect of fragility curver before running the more expensive stochastic models
import sqlite3
import pandas as pd
import numpy as np
from Tech2FragilityCurve import Tech2FragilityCurve

# TemoaSqlitePath="./temoatools/temoa_stochastic/data_files/Test.sql"
# FragilityDataPath="FragilityData.npz"


def GetClosestIDX (Hurricane_LatLong, LatLong1): #Clor
   
    Hurricane_LatLong=Hurricane_LatLong*2*np.pi/360
    LatLong1=LatLong1*2*np.pi/360
    
    LatLong1=np.reshape(LatLong1,(1,2))
    dLat=LatLong1[:,0]-Hurricane_LatLong[:,0]
    dLong=LatLong1[:,1]-Hurricane_LatLong[:,1]
    
    a=np.power(np.sin(dLat/2),2)+np.cos(Hurricane_LatLong[:,0])*np.cos(LatLong1[:,0])*np.power(np.sin(dLong/2),2)
    c=2*np.arcsin(np.minimum(1,np.sqrt(a)))
    d=6367*c
    
    Arg=np.argmin(d) 
    
    return Arg

def Fragility(Tech_ref, Cost, TechLatLong_Tab, Longitude_Tech, Latitude_Tech, LatLong_Hurricane, Fragility_Damages):
    Tech2Fragility_dic=Tech2FragilityCurve()
    Probabilities=np.array([1/10,1/20,1/50,1/100,1/200,1/500,1/1000])
    
    for i in range(len(TechLatLong_Tab)):
        if Tech_ref==TechLatLong_Tab[i]:
            LatTech=Latitude_Tech[i]
            LongTech=Longitude_Tech[i]
            break
            
    #Get closest hurricane condition
    if LatTech!=-999:
        Hurricane_Idx=GetClosestIDX (LatLong_Hurricane, np.array([LatTech, LongTech]))
        ExpectedYearlyDamage=np.sum(Fragility_Damages[Tech2Fragility_dic[Tech_ref]][Hurricane_Idx]*Probabilities)
        ExpectedYearlyCost=Cost*ExpectedYearlyDamage
    
    if LatTech==-999:
        ExpectedYearlyDamage=np.sum(Fragility_Damages[Tech2Fragility_dic[Tech_ref]+"_Pop"]*Probabilities)
        ExpectedYearlyCost=Cost*ExpectedYearlyDamage
        
    return ExpectedYearlyCost

def InputFragilityCurveEffect(TemoaSqlitePath, FragilityDataPath):
 
    FragilityData=np.load(FragilityDataPath, allow_pickle=True)  
    
    Fragility_Damages=FragilityData["Fragility_Damages"][()]
    LatLong_Hurricane_Damages=FragilityData["LatLong"]
    
    SqlFile = sqlite3.connect(TemoaSqlitePath[:-4]+".sqlite")
    
    LatLong_Tab = pd.read_sql_query("SELECT * from LatLong", SqlFile)
    TechLatLong_Tab=LatLong_Tab["tech"]
    Longitude_Tech=LatLong_Tab["Longitude"]
    Latitude_Tech=LatLong_Tab["Latitude"]
    
    CostInvest_Tab = pd.read_sql_query("SELECT * from CostInvest", SqlFile)
    CI_Technologies=CostInvest_Tab["tech"]
    Cost_Invest_Value=CostInvest_Tab["cost_invest"]
    Cost_Invest_Year=CostInvest_Tab["vintage"]
    DeltaCostInvest=np.array(Cost_Invest_Value)
    
    CostFixed_Tab = pd.read_sql_query("SELECT * from CostFixed", SqlFile)
    CF_Technologies=CostFixed_Tab["tech"]
    Cost_Fixed_Value=CostFixed_Tab["cost_fixed"]
    Cost_Fixed_Year=CostFixed_Tab["vintage"]
    
    cursor = SqlFile.cursor()
    
    
    for i in range(len(CI_Technologies)):
        DeltaCostInvest[i]=Fragility(CI_Technologies[i] ,Cost_Invest_Value[i], TechLatLong_Tab,Longitude_Tech, Latitude_Tech, LatLong_Hurricane_Damages, Fragility_Damages)    
      
    NewFixedCostIdx=[]
    for i in range(len(CI_Technologies)):
    
        rowid=np.where((CF_Technologies==CI_Technologies[i])*(Cost_Fixed_Year==Cost_Invest_Year[i]))[0]+1
        
        if np.sum(rowid)==0:
            NewFixedCostIdx.append(i)
        
        for ID in rowid:
            CurrentValue=Cost_Fixed_Value[ID-1]
            sql_update_query="Update CostFixed set cost_fixed = %.5f where rowid=%d" % (DeltaCostInvest[i]+CurrentValue,ID)
            cursor.execute(sql_update_query)
    
    if len(NewFixedCostIdx)!=0:
        for i in NewFixedCostIdx:
            tech=CI_Technologies[i]
            vintage=int(Cost_Invest_Year[i])
            cost_fixed=DeltaCostInvest[i]
            Years=np.array([2017,2020,2025,2030,2035])
            #Years=np.array([2017,2020,2025,2030,2035,2040,2045,2050])
            Years=Years[Years>=vintage]
            for period in Years:
                sql = ''' INSERT INTO CostFixed (periods, tech, vintage, cost_fixed, cost_fixed_units, cost_fixed_notes)
                          VALUES(?,?,?,?,?,?) '''
                
                cursor.execute(sql, (int(period), tech, vintage, cost_fixed,'#','#'))         
           
    SqlFile.commit()
    cursor.close()
    SqlFile.close()   

