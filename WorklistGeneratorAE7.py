import os
import numpy as np
import pandas as pd
from datetime import datetime

#Emily Dang's Worklist Extravaganza for Sequence Pooling AE6 -> AE7
#=================================================================================================================================================================#
#                   Initializing all the variable set CaptureForPooling as captures u want for seq make sure spelling is corect 
#=================================================================================================================================================================#
os.chdir("G:\\Shared drives\\Process Development\\TAM\\AE_Method 3 to 7\\Iggy Runs\\AE_Verif 1.9_Iggy_Test Agilent Custom Kit\\qPCR_Iggy 1.9")
directory = "G:\\Shared drives\\Process Development\\TAM\\AE_Method 3 to 7\\Iggy Runs\\AE_Verif 1.9_Iggy_Test Agilent Custom Kit\\qPCR_Iggy 1.9"
FileName = "qPCR_Iggy 1.9_Agilent Custom Kit_Max 47 Cap_12102021.xlsx"

CaptureForPooling = ["Iggy_Capture1","Iggy_Capture7","Iggy_Capture10","Iggy_Capture11","Iggy_Capture21","Iggy_Capture22","Iggy_Capture26","Iggy_Capture27","Iggy_Capture37","Iggy_Capture42","Iggy_Capture47"]
str_assay = "NX"
finaltubeVol= 800
finaltubeConc = 1.5
str_instrument = "Iggy"
str_date = "Dec10"
str_sourceBarcode = "PS000000017284"
int_sampleVolume = 28
CapturePart = []
temp= ["hello"]
ESP_HGCP =[] 
PoolTubeID = []
Source_Barcode = []
Sample_Volume = []
dilpool_Volume = []
intpool_Volume = []
holdpool_Volume = []
finalDilutionVolume = []

now = datetime.now()
str_dt = now.strftime("%Y%m%d%H%M")
print(str_dt)

str_PoolingTubeID = str_instrument + "_"+ str_date + "_Pool1"

#================================================================================================================#
#                   Reading qPCR template and extracting the dataframe
#================================================================================================================#
df1 = pd.read_excel(os.path.join(directory,FileName), sheet_name="Sample Review", usecols="A:I",index_col=0)
print(df1)

def concentration(captures,finaltubeVol,finaltubeConc):
    totalCaptures = len(captures)
    print(totalCaptures)
    totalrows = totalCaptures*2
    molarity = (finaltubeVol*finaltubeConc)/totalCaptures
    print(molarity)
    return molarity

#================================================================================================================#
#                   Locating specific captures in the dataframe to new dataframe + reformatting
#================================================================================================================#
df2= df1.loc[CaptureForPooling]

# df2 = df2[["96 Well ID","Average Conc. nM"]].copy()
df2 = df2.drop(["Cq Rep 1","Cq Rep 2","Cq Rep 3","Conc. Rep 1 nM ","Conc. Rep 2 nM ","Conc. Rep 3 nM "], axis = 1)
df2.reset_index(inplace=True)
print(df2)
length = len(df2["Sample Name"]) 
print("Total Number of Samples for Pooling: ", length)
#================================================================================================================#
#                  Figuring out if HGCP vs ESP and depending on the Assay multiply concenctration
#                    by a certain ratio to find the capture part to find the poolVolume needed
#                       # NX: ESP = 0.8275 * molarity, HGCP = 0.1725* molarity
#                         V2: 
#                         V3: 
#================================================================================================================#

for x,name in enumerate(df2["Sample Name"]):
    if name == temp[x]:
        ESP_HGCP.append("HGCP")
        temp.append(name)
    else:
        ESP_HGCP.append("ESP")
        temp.append(name)

for type in ESP_HGCP:
    if str_assay == "NX" and type == "ESP":
        intermediate = 0.8275*concentration(CaptureForPooling,finaltubeVol, finaltubeConc)
        CapturePart.append(intermediate)
        # print(CapturePart)
    elif str_assay == "NX" and type == "HGCP":
        intermediate = 0.1725*concentration(CaptureForPooling,finaltubeVol, finaltubeConc)
        CapturePart.append(intermediate)
print(CapturePart)

Pool_Vol = round(CapturePart/df2["Average Conc. nM"],2)
df2.rename(columns={"96 Well ID": "Source_Well"}, inplace = True)

#================================================================================================================#
#                   Diluting Sample Volume & intermediate Volume as needed
#                   If Pool_Vol <2.5 &>1.0, dil = 7
#                   If Pool_Vol <1.0, dil = 5
#================================================================================================================#

for dilvolume in Pool_Vol:
    if dilvolume >= 2.5:
        dilpool_Volume.append(0) #no dilution required
    elif dilvolume >=1.0 and dilvolume <2.5:
        dilpool_Volume.append(7) #will take 7uL for dilution
    elif dilvolume >= 0.1 and dilvolume <1.0:
        dilpool_Volume.append(5) #will take 5uL for dilution

for x,intermediateVolume in enumerate(Pool_Vol):
    if intermediateVolume >= 2.5:
        intpool_Volume.append(0) #no dilution
    elif intermediateVolume <2.5:
        holdvar = (((dilpool_Volume[x]**2)/intermediateVolume)-dilpool_Volume[x])
        # print(holdvar)
        intpool_Volume.append(round(holdvar,2))
        holdvar = 0

# print(intpool_Volume)

#================================================================================================================#
#                   Getting total volume need for dilution if vol<2.5 insert dilution volume (5 or 7uL)
#================================================================================================================#

for x,poolVolume in enumerate(Pool_Vol):
    if poolVolume <2.5:
        intermedVol = dilpool_Volume[x]
        holdpool_Volume.append(intermedVol)
    else:
        holdpool_Volume.append(poolVolume)

poolDilVolume = finaltubeVol-sum(holdpool_Volume)
print("This is the total Dilution Volume: ", poolDilVolume)

for x in range(len(Pool_Vol)):
    if x==0:
        finalDilutionVolume.append(poolDilVolume)
    else:
        finalDilutionVolume.append(0)

#================================================================================================================#
#                   Final DF to be exported to CSV for worklist for AE7
#================================================================================================================#
df3 = pd.DataFrame({"Source_Barcode": str_sourceBarcode, 
                    "Source_Well": df2["Source_Well"], 
                    "Sample_Volume": int_sampleVolume, 
                    "Pool_Tube_ID": str_PoolingTubeID,
                    "Pool_Volume": Pool_Vol,
                    "Diluted_Sample_Volume": dilpool_Volume,
                    "Intermediate_Dil_Volume": intpool_Volume,
                    "ESPHCGP": ESP_HGCP,
                    "CaptureID": df2["Sample Name"],
                    "Pool_Dil_Volume": finalDilutionVolume})

df3.sort_values(by=['ESPHCGP'])
print(df3)

                
name = "SeqPooling_" + str_sourceBarcode[-4:]+ "_"+str_dt+".csv"
# df3.to_csv(name, index=False)

