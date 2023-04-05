import numpy as np
import csv


##---------------------------------------------------##
##---------------------------------------------------##
#Read Hurricane Data
HurricaneFile=open("HurricaneMPH.txt","r")
HurricaneFile_r=csv.reader(HurricaneFile,delimiter=",")

Cell_ID_H=[]
Hurricane_MPH=[]
LatLong=[]
#CountLine
for eachline in HurricaneFile_r:

    if HurricaneFile_r.line_num>=2:
        MPH=np.zeros((7))# f10yr,f20yr,f50yr,f100yr,f200yr,f500yr,f1000yr
        Cell_ID_H.append(int(eachline[0]))
        LatLong.append(np.array([float(eachline[7]),float(eachline[8])]))
        
        MPH[0]=float(eachline[11])
        MPH[1]=float(eachline[12])
        MPH[2]=float(eachline[13])
        MPH[3]=float(eachline[14])
        MPH[4]=float(eachline[15])
        MPH[5]=float(eachline[16])
        MPH[6]=float(eachline[17])
        Hurricane_MPH.append(MPH)

HurricaneFile.close()
Cell_ID_H=np.array(Cell_ID_H)
LatLong=np.array(LatLong)
Hurricane_MPH=np.array(Hurricane_MPH)
##---------------------------------------------------##
##---------------------------------------------------##
#Read Census Data
CensusFile=open("Census.csv","r")
CensusFile_r=csv.reader(CensusFile,delimiter=",")

Cell_ID_C=[]
Population=[]
#CountLine
for eachline in CensusFile_r:

    if CensusFile_r.line_num>=2:
        Cell_ID_C.append(int(eachline[0]))
        Population.append(float(eachline[43]))

CensusFile.close()
Cell_ID_C=np.array(Cell_ID_C)
Population=np.array(Population)

##---------------------------------------------------##
##---------------------------------------------------##
#Coordinate Data
Sort=np.argsort(Cell_ID_H)
Cell_ID_H=Cell_ID_H[Sort]
LatLong=LatLong[Sort,:]
Hurricane_MPH=Hurricane_MPH[Sort,:]

Sort=np.argsort(Cell_ID_C)
Cell_ID_C=Cell_ID_C[Sort]
Population=Population[Sort]
#np.sum(Cell_ID_C-Cell_ID_H) must be equal to zero

np.savez("GeoData", Population=Population, Cell_ID=Cell_ID_C, Hurricane_MPH=Hurricane_MPH, LatLong=LatLong)

