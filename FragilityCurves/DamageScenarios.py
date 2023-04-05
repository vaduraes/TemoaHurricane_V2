import numpy as np
from FragilityCurves import fragility

def GetClosestCellID(LatLong_Site,GeoData_LatLong):
    GeoData_LatLong=GeoData_LatLong*2*np.pi/360
    LatLong_Site=LatLong_Site*2*np.pi/360
    
    LatLong_Site=np.reshape(LatLong_Site,(1,2))
    dLat=LatLong_Site[:,0]-GeoData_LatLong[:,0]
    dLong=LatLong_Site[:,1]-GeoData_LatLong[:,1]
    
    a=np.power(np.sin(dLat/2),2)+np.cos(GeoData_LatLong[:,0])*np.cos(LatLong_Site[:,0])*np.power(np.sin(dLong/2),2)
    c=2*np.arcsin(np.minimum(1,np.sqrt(a)))
    d=6367*c    
    ClosestID=np.argmin(d)
    
    return ClosestID

GeoData=np.load("GeoData.npz")

Population=GeoData["Population"]
Population=Population/np.sum(Population) #Percentage population
Population=np.reshape(Population,(len(Population),1))

Cell_ID_C=GeoData["Cell_ID"]
Hurricane_MPH=GeoData["Hurricane_MPH"]+20
Hurricane_MPH[Hurricane_MPH<1]=1 #To avoid numerical problems 1/0

LatLong=GeoData["LatLong"]
GeoData.close()


#Get lat long reference for wind, wave and ocean current
ID_WindReference=np.where(Cell_ID_C==37055970102)[0][0]
ID_WindReference_OF=LatLong[Cell_ID_C==37055970102,:]
ID_Wave=LatLong[Cell_ID_C==37055970102,:]
ID_Ocean=LatLong[Cell_ID_C==37055970102,:]

#Following the paper: https://doi.org/10.1038/s41560-020-00758-6
curves = {"trans": "trans_UK_base",
          "sub": "sub_HAZUS_severe_k3",
          "dist_cond": "dist_cond_TX",
          "dist_twr": "dist_60yr",
          "wind": "wind_nonyaw",
          "solar": "solar_utility",
          "coal_biomass": "secbh_severe",
          "natgas_petrol": "secbm_severe",
          "battery": "secbl_severe",
          "hydro": "cecbl_severe",
          "UGND":  "secbm_severe",
          "wind_M10":  "wind_M10",
          "wind_P10": "wind_P10",
          "Victor_OC": "Nothing",#"Victor_OC", UGND, wind_P10
          "wind_nonyaw": "wind_nonyaw",}

#Only 7 elements [1/10,1/20,1/50,1/100,1/200,1/500,1/1000]
Fragility_trans_Pop          =np.sum(fragility(Hurricane_MPH, curve=curves["trans"])*Population,axis=0)
Fragility_sub_Pop            =np.sum(fragility(Hurricane_MPH, curve=curves["sub"])*Population,axis=0)
Fragility_dist_cond_Pop      =np.sum(fragility(Hurricane_MPH, curve=curves["dist_cond"])*Population,axis=0)
Fragility_dist_twr_Pop       =np.sum(fragility(Hurricane_MPH, curve=curves["dist_twr"])*Population,axis=0)
Fragility_solar_Pop          =np.sum(fragility(Hurricane_MPH, curve=curves["solar"])*Population,axis=0)
Fragility_coal_biomass_Pop   =np.sum(fragility(Hurricane_MPH, curve=curves["coal_biomass"])*Population,axis=0)
Fragility_natgas_petrol_Pop  =np.sum(fragility(Hurricane_MPH, curve=curves["natgas_petrol"])*Population,axis=0)
Fragility_battery_Pop        =np.sum(fragility(Hurricane_MPH, curve=curves["battery"])*Population,axis=0)
Fragility_hydro_Pop          =np.sum(fragility(Hurricane_MPH, curve=curves["hydro"])*Population,axis=0)
Fragility_UGND_Pop           =np.sum(fragility(Hurricane_MPH, curve=curves["UGND"])*Population,axis=0)
Fragility_wind_Pop           =np.sum(fragility(Hurricane_MPH, curve=curves["wind_nonyaw"])*Population,axis=0)
Fragility_Dummy_Pop          =np.zeros(7)
#Exception not based on the population
Fragility_OF_wind_Pop         =fragility(Hurricane_MPH, curve=curves["wind_nonyaw"])[ID_WindReference,:]
Fragility_OF_wind_P10_Pop     =fragility(Hurricane_MPH, curve=curves["wind_P10"])[ID_WindReference,:]
Fragility_OF_wind_M10_Pop     =fragility(Hurricane_MPH, curve=curves["wind_M10"])[ID_WindReference,:]
Fragility_OF_ocean_Pop        =fragility(Hurricane_MPH, curve=curves["Victor_OC"])[ID_WindReference,:]



# 7 elements [1/10,1/20,1/50,1/100,1/200,1/500,1/1000] for each county
Fragility_trans           =fragility(Hurricane_MPH, curve=curves["trans"])
Fragility_sub             =fragility(Hurricane_MPH, curve=curves["sub"])
Fragility_dist_cond       =fragility(Hurricane_MPH, curve=curves["dist_cond"])
Fragility_dist_twr        =fragility(Hurricane_MPH, curve=curves["dist_twr"])
Fragility_solar           =fragility(Hurricane_MPH, curve=curves["solar"])
Fragility_coal_biomass    =fragility(Hurricane_MPH, curve=curves["coal_biomass"])
Fragility_natgas_petrol   =fragility(Hurricane_MPH, curve=curves["natgas_petrol"])
Fragility_battery         =fragility(Hurricane_MPH, curve=curves["battery"])
Fragility_hydro           =fragility(Hurricane_MPH, curve=curves["hydro"])
Fragility_UGND            =fragility(Hurricane_MPH, curve=curves["UGND"])
Fragility_wind            =fragility(Hurricane_MPH, curve=curves["wind_nonyaw"])
Fragility_OF_wind         =fragility(Hurricane_MPH, curve=curves["wind_nonyaw"])
Fragility_OF_ocean        =fragility(Hurricane_MPH, curve=curves["Victor_OC"])
Fragility_OF_wind_P10     =fragility(Hurricane_MPH, curve=curves["wind_P10"])
Fragility_OF_wind_M10     =fragility(Hurricane_MPH, curve=curves["wind_M10"])
Fragility_Dummy           =np.zeros((Fragility_OF_wind_M10.shape[0],7))


Fragility_Damages = {
    "Fragility_trans_Pop"        :Fragility_trans_Pop         , 
    "Fragility_sub_Pop"          :Fragility_sub_Pop           ,  
    "Fragility_dist_cond_Pop"    :Fragility_dist_cond_Pop     ,  
    "Fragility_dist_twr_Pop"     :Fragility_dist_twr_Pop      ,  
    "Fragility_solar_Pop"        :Fragility_solar_Pop         ,  
    "Fragility_coal_biomass_Pop" :Fragility_coal_biomass_Pop  ,  
    "Fragility_natgas_petrol_Pop":Fragility_natgas_petrol_Pop ,  
    "Fragility_battery_Pop"      :Fragility_battery_Pop       ,  
    "Fragility_hydro_Pop"        :Fragility_hydro_Pop         ,  
    "Fragility_UGND_Pop"         :Fragility_UGND_Pop          ,  
    "Fragility_wind_Pop"         :Fragility_wind_Pop          ,  
    "Fragility_OF_wind_Pop"      :Fragility_OF_wind_Pop       ,  
    "Fragility_OF_wind_P10_Pop"  :Fragility_OF_wind_P10_Pop   ,  
    "Fragility_OF_wind_M10_Pop"  :Fragility_OF_wind_M10_Pop   ,
    "Fragility_Dummy_Pop"        :Fragility_Dummy_Pop         ,
    "Fragility_OF_ocean_Pop"     :Fragility_OF_ocean_Pop      ,
    
    "Fragility_trans"            :Fragility_trans             ,  
    "Fragility_sub"              :Fragility_sub               ,  
    "Fragility_dist_cond"        :Fragility_dist_cond         ,  
    "Fragility_dist_twr"         :Fragility_dist_twr          ,  
    "Fragility_solar"            :Fragility_solar             ,  
    "Fragility_coal_biomass"     :Fragility_coal_biomass      ,  
    "Fragility_natgas_petrol"    :Fragility_natgas_petrol     ,  
    "Fragility_battery"          :Fragility_battery           ,  
    "Fragility_hydro"            :Fragility_hydro             ,  
    "Fragility_UGND"             :Fragility_UGND              ,  
    "Fragility_wind"             :Fragility_wind              ,  
    "Fragility_OF_ocean"         :Fragility_OF_ocean      ,
    "Fragility_OF_wind"          :Fragility_OF_wind        ,  
    "Fragility_OF_wind_P10"      :Fragility_OF_wind_P10   ,  
    "Fragility_OF_wind_M10"      :Fragility_OF_wind_M10,
    "Fragility_Dummy":Fragility_Dummy}      
          


np.savez("FragilityData.npz", Fragility_Damages=Fragility_Damages, LatLong=LatLong)