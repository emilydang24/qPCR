import os
import numpy as np
import pandas as pd
from datetime import datetime
#src plate src well LimsID workflow conc cap ID indicies plate info sample source
#i need initial ws to have assay sample source blockertype 
#Src_Plate Src_Well Sample_ID Capture_ID Sample_Vol Assay Blocker_Type	Dilution_Required	Transfer_Sample_Volume	Transfer_Diluent_Volume	Pooled_Transfer_Volume	Final_Diluent_Volume
initialWorklist = "G:\\Shared drives\\Process Development\\TAM\\AE_Method 3 to 7\\Wheatley Runs\\AE_Verif 1.4_Wheatley_31 Cap & PCR Mix_ACEv4\\AE3 CapturePooling Worksheets\\Sample List_AE3_Iggy1.9.xlsx"

xl_file = pd.ExcelFile(initialWorklist)
df = pd.DataFrame(pd.read_excel(initialWorklist, skiprows=range(0,5)))
# print(df)
instrument = "Iggy"
AAssay = "NX"
Blocker = "XGEN"
Sample_ID = []
PlateInfo = "PS000000018246"
CaptureID = []
SampleVol =[]
DilutionRequired = []
Transfer_Volume = []
Transfer_Diluent_Volume = []
Holder_Transfer_Diluent_Volume =[]
Pool_Transfer_Volume = []
Final_Diluent_Volume = []
now = datetime.now()
str_dt = now.strftime("%Y%m%d%H%M")

#================================================================================================================#
#                   BUILDING OUT THE SAMPLE ID & SAMPLE VOLUME STEPS
#================================================================================================================#

for x,y in enumerate(df["Sample ID"]):
    # print(x,y)
    new = str(y) + "_" +instrument+"_Sept1_" +str(x+1)
    # print(new)
    Sample_ID.append(new)

df["Sample_ID"] = Sample_ID
sampleVol = round(3000/4/df["Lunatic Conc, ng/uL"],1)
for sample in sampleVol:
    if sample < 2.5:
        DilutionRequired.append("TRUE")
        Transfer_Volume.append(sample*5)
    else:
        DilutionRequired.append("FALSE")
        Transfer_Volume.append(sample)

#================================================================================================================#
#                   BUILDING OUT THE DILUTION REQUIRED STEPS
#================================================================================================================#

for dilution in DilutionRequired:
    if dilution == "FALSE":
        Holder_Transfer_Diluent_Volume.append(0)
        # Pool_Transfer_Volume.append(0)
    else:
        Holder_Transfer_Diluent_Volume.append(Transfer_Volume)
        # Pool_Transfer_Volume.append(Transfer_Volume)
# print(len(Pool_Transfer_Volume))
counter = 0
temp = 0
addition = 0
UniqueCaptures = df["Captures"].unique()
CapturesLst = []
Captures = df["Captures"].values

for x in Captures:
    CapturesLst.append(x)

listCapNum = []
for x in UniqueCaptures:
    # print(x)
    countCap = CapturesLst.count(x)
    listCapNum.append(countCap)
    # print(countCap)
print(listCapNum)
# for x,y in enumerate(CaptureID):


for x,y in enumerate(Holder_Transfer_Diluent_Volume):
    if x %4 ==0:
        for four in range(0,4):
            side = Holder_Transfer_Diluent_Volume[temp+four] 
            addition = addition + side
        temp = temp + 4
        TransVol = addition  *4
        Transfer_Diluent_Volume.append(TransVol)
        Pool_Transfer_Volume.append(addition)
        counter = counter + 1
    else:
        Transfer_Diluent_Volume.append(0)
        Pool_Transfer_Volume.append(0)
# print(len(Pool_Transfer_Volume))
#================================================================================================================#
#                   BUILDING OUT THE CAPTURE ID STEP
#================================================================================================================#
totalSamples= len(df["Sample ID"])
numCapture = 0

for num in range(0,totalSamples):   
    if num%4 == 0:
        numCapture += 1
        CaptureID.append(instrument +"_Capture"+str(numCapture))
    else:
        CaptureID.append(instrument +"_Capture"+str(numCapture))

#================================================================================================================#
#                   BUILDING OUT THE ASSAY/BLOCKER STEP (not needed)
#================================================================================================================#

def onesizefitsAll(input,Array):
    Array = []
    for value in df["Sample_ID"]:
        Array.append(input)
    return(Array)
        
#================================================================================================================#
#                   BUILDING OUT THE FINAL DILUTION STEP
#================================================================================================================#
sum = 0 
tempIndex = 0 
counter = 0
CapNumCounter = 0
holderDilVol = []

for num in range(0,len(UniqueCaptures)):
    for four in range(0,listCapNum[CapNumCounter]):
        side = sampleVol[tempIndex+four] 
        sum = float(sum)+ float(side)
    tempIndex = tempIndex+listCapNum[CapNumCounter]
    finalVol = 360-sum
    holderDilVol.append(finalVol)
    sum = 0
    CapNumCounter = CapNumCounter + 1 
print(holderDilVol)
print(len(sampleVol))
CapNumCounter = 0
for x in range(0,len(sampleVol)):
    if x % listCapNum[CapNumCounter] ==0:
        print(listCapNum[CapNumCounter])
        Final_Diluent_Volume.append(holderDilVol[counter])
        counter = counter + 1
        # print(counter)
    else:
        Final_Diluent_Volume.append(0)
    CapNumCounter = CapNumCounter +1
    print(Final_Diluent_Volume)

print(Final_Diluent_Volume)

finalAE3CSV = pd.DataFrame({"Src_Plate":df["Plate"], 
                    "Src_Well": df["Well"], 
                    "Sample_ID": df["Sample_ID"],
                    "Capture_ID": CaptureID,
                    "Sample_Vol": sampleVol, 
                    "Assay": AAssay,
                    "Blocker_Type": Blocker,
                    "Dilution_Required": DilutionRequired,
                    "Transfer_Sample_Volume": Transfer_Volume,
                    "Transfer_Diluent_Volume": Transfer_Diluent_Volume,
                    "Pooled_Transfer_Volume": Pool_Transfer_Volume,
                    "Final_Diluent_Volume": Final_Diluent_Volume}
                    )
# print(finalAE3CSV)
# name = "G:\\Shared drives\\Process Development\\TAM\\AE_Method 3 to 7\\Wheatley Runs\\AE_Verif 1.4_Wheatley_31 Cap & PCR Mix_ACEv4\\AE3 CapturePooling Worksheets\\CapturePooling_" + str_dt +".csv"
# finalAE3CSV.to_csv(name, index=False)
