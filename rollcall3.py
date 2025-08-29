import pandas as pd

dforg=pd.read_csv("sample.csv")
dforg["Start Time"]=pd.to_datetime(dforg["Start Time"])
dforg["End Time"]=pd.to_datetime(dforg["End Time"])
dforg["Session Duration"]=(dforg["End Time"]-dforg["Start Time"])
dfmain=dforg.drop(["Join Time","Leave Time","Guest","Meeting ID","Topic","Start Time","End Time"],axis=1) #dropping uncessesary datas; Axis=1-coloumn
 
print(dfmain.info())
print(dfmain)
'''print((dfmain["Start Time"]-dfmain["End Time"]))'''
