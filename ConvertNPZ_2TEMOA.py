import numpy as np
import datetime as dt
from datetime import timedelta
import shutil
import os
from General_SQL_OCEAN_Structure_2035 import Text1, Text_CF_L, Text_CF_R, CFixed_L, CFixed_R, CInvest_L, CInvest_R

def DistanceBetweenLatLong(LatLong1, LatLong2):
    LatLong1=LatLong1*2*np.pi/360
    LatLong2=LatLong2*2*np.pi/360
    
    dLat=np.reshape(LatLong1[:,0],(len(LatLong1[:,0]),1))-np.reshape(LatLong2[:,0],(1,len(LatLong2[:,0])))
    dLong=np.reshape(LatLong1[:,1],(len(LatLong1[:,1]),1))-np.reshape(LatLong2[:,1],(1,len(LatLong2[:,1])))
    
    P1=np.reshape(np.cos(LatLong1[:,0]),(LatLong1.shape[0],1))
    P2=np.reshape(np.cos(LatLong2[:,0]),(1,LatLong2.shape[0]))
    
    a=np.power(np.sin(dLat/2),2) + (P1*P2)*np.power(np.sin(dLong/2),2)
    c=2*np.arcsin(np.minimum(1,np.sqrt(a)))
    Distance=6367*c #[km]
    
    return Distance

def ComputeAVG_Capex_Opex (LatLong_Results, Y_NumTurbines, LatLong_Costs,Capex, Opex):
    
    Distance=DistanceBetweenLatLong(LatLong_Costs, LatLong_Results)
    Idx_ClosestSiteCost=np.argmin(Distance,axis=0)
    
    Capex=np.sum(Capex[Idx_ClosestSiteCost]*Y_NumTurbines)/sum(Y_NumTurbines)
    Opex=np.sum(Opex[Idx_ClosestSiteCost]*Y_NumTurbines)/sum(Y_NumTurbines)
    
    return Capex, Opex

def FixTimeResolutionCF(WindE_File, WaveE_File, OceanE_File):
    #The wind data starts at 1/1/2007 and ends at 12/31/2013
    WindEnergy=WindE_File['WindEnergy']
    
    #The wave data starts at 1/1/2009 and ends at 12/31/2013
    WaveEnergy=WaveE_File['Energy_pu']
    
    #The wave data starts at 1/1/2009 and ends at 11/30/2014
    OceanEnergy=OceanE_File['CurrentEnergy_pu']
    
#-------------------------- WIND-----------------#
    SIdxWind=(dt.datetime(2009,1,1,0)-dt.datetime(2007,1,1,0)).days*24# Start index
    EIdxWind=(dt.datetime(2014,1,1,0)-dt.datetime(2007,1,1,0)).days*24# Last index
    
    Num3HourIntervals=int((EIdxWind-SIdxWind)/3)-1
    CFWind=np.zeros((WindEnergy.shape[0],Num3HourIntervals),dtype=float)
    
    for H3_Steps in range(Num3HourIntervals):
        
        StartIdx=SIdxWind + 3*(H3_Steps)
        
        CFWind[:,H3_Steps]=(WindEnergy[:,StartIdx])
        
#-------------------------- WAVE-----------------#
    SIdxWave=(dt.datetime(2009,1,1,0)-dt.datetime(2009,1,1,0)).days*8
    EIdxWave=((dt.datetime(2014,1,1,0)-dt.datetime(2009,1,1,0)).days)*8
    CFWave=WaveEnergy[:,SIdxWave:EIdxWave]

#-------------------------- OCEAN CURRENT-----------------#   
    SIdxCurrent=(dt.datetime(2009,1,1,0)-dt.datetime(2009,1,1,0)).days*8
    EIdxCurrent=((dt.datetime(2014,1,1,0)-dt.datetime(2009,1,1,0)).days)*8-1
    CFOcean=OceanEnergy[:,SIdxCurrent:EIdxCurrent]
    

    return CFWind, CFWave, CFOcean

def ComputeEquivalentCF (LatLong_Results, Y_NumTurbines, LatLong_Costs, CF):
    
    Distance=DistanceBetweenLatLong(LatLong_Costs, LatLong_Results)
    Idx_ClosestSiteCost=np.argmin(Distance,axis=0)
    Y_NumTurbines=np.reshape(Y_NumTurbines,(Y_NumTurbines.shape[0],1))
    
    CF=np.sum(CF[Idx_ClosestSiteCost,:]*Y_NumTurbines,axis=0)/sum(Y_NumTurbines)
    
    return CF

def CovnertCF_2_TEMOA_resolution (CF, StartDate):

    MH_Data=np.zeros((12,24), dtype=float)
    MH_Data_Count=np.zeros((12,24), dtype=float)
    h=0
    for i in range(CF.shape[0]):
        CurrentDate=StartDate+timedelta(hours=i*3)
        
        IdxMonth=CurrentDate.month-1
        
        MH_Data[IdxMonth,h]=MH_Data[IdxMonth,h]+CF[i]
        MH_Data[IdxMonth,h+1]=MH_Data[IdxMonth,h+1]+CF[i]
        MH_Data[IdxMonth,h+2]=MH_Data[IdxMonth,h+2]+CF[i]
        
        MH_Data_Count[IdxMonth,h]=MH_Data_Count[IdxMonth,h]+1
        MH_Data_Count[IdxMonth,h+1]=MH_Data_Count[IdxMonth,h+1]+1
        MH_Data_Count[IdxMonth,h+2]=MH_Data_Count[IdxMonth,h+2]+1
    
        h=h+3
        if h==24:
            h=0
            
    MH_Data=MH_Data/MH_Data_Count    
    
    #Only four seasons
    CF_Temoa_W=np.average(MH_Data[[0,1,11],:],axis=0)
    CF_Temoa_Sp=np.average(MH_Data[[2,3,4],:],axis=0)
    CF_Temoa_Su=np.average(MH_Data[[5,6,7],:],axis=0)
    CF_Temoa_F=np.average(MH_Data[[8,9,10],:],axis=0)    
    
    CF_Temoa=np.concatenate((CF_Temoa_W,CF_Temoa_Sp,CF_Temoa_Su,CF_Temoa_F))
    
    return CF_Temoa


def TEMOA_INPUTS(LOCE_target, PathCapex_Opex_And_Simulations,PathPortOPT_Result, StartDate):
    WindData=np.load(PathCapex_Opex_And_Simulations+"WindEnergyNREL_100m_Haliade150_6MW.npz")
    WaveData=np.load(PathCapex_Opex_And_Simulations+"WaveEnergy_Pelamis_2009_2013.npz")
    OceanData=np.load(PathCapex_Opex_And_Simulations+"OceanCurrentEnergyRM4.npz")
    
    
    RatedPowerWind=WindData["RatedPower"]*10**-9 #[GW]
    RatedPowerWave=WaveData["RatedPower"]*10**-9
    RatedPowerOcean=OceanData["RatedPower"]*10**-9
    
    WindC_latlong=WindData["WindEnergy"]
    WaveC_latlong=WaveData["LatLong"]
    OceanC_latlong=OceanData["LatLong"]
    
    
    Wind_CF, Wave_CF,Ocean_CF=FixTimeResolutionCF(WindData, WaveData, OceanData)
    
    
    #Capex and Opex in [M$/GW]
    WindCapex=WindData["Capex"]/RatedPowerWind
    WindOpex=WindData["Opex"]/RatedPowerWind
    
    WaveCapex=WaveData["Capex"]/RatedPowerWave
    WaveOpex=WaveData["Opex"]/RatedPowerWave
    
    OceanCapex=OceanData["Capex"]/RatedPowerOcean
    OceanOpex=OceanData["Opex"]/RatedPowerOcean
    
    #Capacity Factor
    PortOPT_R=np.load(PathCapex_Opex_And_Simulations+PathPortOPT_Result,allow_pickle=True)
    TotalInstalledCap=PortOPT_R["TotalNumTurbines"]*[RatedPowerWind, RatedPowerWave, RatedPowerOcean]
    
    LCOEs=PortOPT_R["MINLPSolutionsLCOE"]
    LCOEs=LCOEs[LCOEs!=None]
    
    if LOCE_target=="L":
        CaseIDX=len(LCOEs)-1
        
    if LOCE_target=="H":
        CaseIDX=0
        
    if LOCE_target=="M":
        Avg=(LCOEs[0]+LCOEs[-1])/2
        CaseIDX=np.argmin(np.abs(LCOEs-Avg))
    
    LCOE=LCOEs[CaseIDX]
    
    Y_NumTurbines_Wind=PortOPT_R["OptimalYSolutionsWind"]
    Y_NumTurbines_Wave=PortOPT_R["OptimalYSolutionsWave"]
    Y_NumTurbines_Ocean=PortOPT_R["OptimalYSolutionsOcean"]
    
    WindR_latlong =PortOPT_R["MINLPSolutionsLatLongWind"]
    WaveR_latlong =PortOPT_R["MINLPSolutionsLatLongWave"]
    OceanR_latlong=PortOPT_R["MINLPSolutionsLatLongOcean"]
    
    #Wind
    EquivalentCapex=np.array([0,0,0])
    EquivalentOpex=np.array([0,0,0])
    EquivalentCF=np.array([Wind_CF[0,:]*0,Wave_CF[0,:]*0,Ocean_CF[0,:]*0])
    
    if TotalInstalledCap[0]!=0:
        EquivalentCapex[0], EquivalentOpex[0]=ComputeAVG_Capex_Opex(WindR_latlong[CaseIDX], Y_NumTurbines_Wind[CaseIDX], WindC_latlong, WindCapex, WindOpex)
        EquivalentCF[0]=ComputeEquivalentCF (WindR_latlong[CaseIDX], Y_NumTurbines_Wind[CaseIDX], WindC_latlong, Wind_CF)
        
        
    if TotalInstalledCap[1]!=0:
        EquivalentCapex[1], EquivalentOpex[1]=ComputeAVG_Capex_Opex(WaveR_latlong[CaseIDX], Y_NumTurbines_Wave[CaseIDX], WaveC_latlong, WaveCapex, WaveOpex)
        EquivalentCF[1]=ComputeEquivalentCF (WaveR_latlong[CaseIDX], Y_NumTurbines_Wave[CaseIDX], WaveC_latlong, Wave_CF)
        
        
    if TotalInstalledCap[2]!=0:
        EquivalentCapex[2], EquivalentOpex[2]=ComputeAVG_Capex_Opex(OceanR_latlong[CaseIDX], Y_NumTurbines_Ocean[CaseIDX], OceanC_latlong, OceanCapex, OceanOpex)
        EquivalentCF[2]=ComputeEquivalentCF (OceanR_latlong[CaseIDX], Y_NumTurbines_Ocean[CaseIDX], OceanC_latlong, Ocean_CF)
        
        
    EquivalentCapex=sum(EquivalentCapex*TotalInstalledCap)/sum(TotalInstalledCap)
    EquivalentOpex=sum(EquivalentOpex*TotalInstalledCap)/sum(TotalInstalledCap)
    EquivalentCF=sum(EquivalentCF*TotalInstalledCap.reshape(3,1))/sum(TotalInstalledCap)
    EquivalentCF=CovnertCF_2_TEMOA_resolution (EquivalentCF, StartDate)


    return EquivalentCapex, EquivalentOpex, EquivalentCF, LCOE, TotalInstalledCap

    
def WriteTEMOA_File(CAPEX, OPEX, CF_TEMOA, BaseSQL, CaseSQL):
    
    shutil.copyfile(BaseSQL, CaseSQL)
    file_object = open(CaseSQL, 'a')
    
    for i in range(len(Text1)):
        file_object.write(Text1[i]+"\n")
        
    for i in range(len(Text_CF_L)):
        file_object.write(Text_CF_L[i]+str(CF_TEMOA[i])+Text_CF_R[i]+"\n")
        
    for i in range(len(CFixed_L)):
        file_object.write(CFixed_L[i]+str(OPEX)+CFixed_R[i]+"\n")
    
    for i in range(len(CInvest_L)):
        file_object.write(CInvest_L[i]+str(CAPEX)+CInvest_R[i]+"\n")
        
    file_object.write('COMMIT;\n')
    file_object.close()
    
    if os.path.exists(CaseSQL[:-4]+".sqlite"):
        os.remove(CaseSQL[:-4]+".sqlite")
        
    os.system("sqlite3 "+ CaseSQL[:-4]+".sqlite < "+CaseSQL)


def CreateConfigfile(ConfiFilePath_Name, dat_Path, ScenarioName):
    file_object = open(ConfiFilePath_Name, 'w')
              
    file_object.write("--input="+dat_Path+"\\"+ScenarioName+".sqlite\n")     
    file_object.write("--output="+dat_Path+"\\"+ScenarioName+".sqlite\n")    
    file_object.write("--scenario=GeneralOcean"+"\n")    
    file_object.write("--path_to_db_io="+dat_Path+"\n")    
    file_object.write("--solver=gurobi  "+"\n")    
    file_object.write("--keep_pyomo_lp_file"+"\n")    
    file_object.close()
        

# LOCE_target="L" #H, M, L -> high, medium, low (LCOE)
# PathCapex_Opex_And_Simulations="./Inputs/Original_Inputs/"
# PathPortOPT_Result="PortfolioOptimizationWindWaveOcean(0_0_50).npz"
# NewSQLFile="./Inputs/Original_Inputs/"+"CaseOcean1.sql"
# StartDate=dt.datetime(2009,1,1,0) #Start Date of the datasets used
# BaseDukeFile="./Inputs/Original_Inputs/Duke_CapEx.sql"#path

# CAPEX, OPEX, CF_TEMOA,LCOE,TotalInstalledCap=TEMOA_INPUTS(LOCE_target, PathCapex_Opex_And_Simulations,PathPortOPT_Result, StartDate)
# WriteTEMOA_File(CAPEX, OPEX, CF_TEMOA, BaseDukeFile, NewSQLFile)




