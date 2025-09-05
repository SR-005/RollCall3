import pandas as pd
import numpy as np
from datetime import datetime

def main(filepath):

    print(filepath)    
    #----------------------------------------------------------------------DATA SECTION----------------------------------------------------------------------

    #DATA HANDLING AND PROCESSING
    dforg=pd.read_csv(filepath)
    print("SUCCESFULLY RECIEVED CSV FILE")
    #converting str->datetime
    dforg["Start Time"]=pd.to_datetime(dforg["Start Time"])
    dforg["End Time"]=pd.to_datetime(dforg["End Time"])
    dforg["Session Duration"]=(dforg["End Time"]-dforg["Start Time"]).dt.total_seconds() / 60   #calculating meeting duration and converting it to minutes
    dforg["Session Duration"]=dforg["Session Duration"].astype(int) #converting it to int values
    dfmain=dforg.drop(["Join Time","Leave Time","Guest"],axis=1) #dropping uncessesary datas; Axis=1-coloumn

    #calculating minimum presence time
    minimumtime=dfmain.loc[0, "Session Duration"]
    minimumtime=round((minimumtime/100)*75) #75% attendence given
    print("Minimum Time of Presence in Event",minimumtime)

    eventname=dfmain.loc[0, "Topic"]
    startdate=dfmain.loc[0, "Start Time"]
    enddate=dfmain.loc[0, "End Time"]
    
    startdate = startdate.strftime("%Y-%m-%d")
    enddate = enddate.strftime("%Y-%m-%d")

    print(eventname)
    print(type(startdate))
    print(enddate)

    dfmain["Status"]=np.where(dfmain["Duration"] >= minimumtime,"Present","Absent") #created a present/absent coloumn
    dfmain = dfmain.dropna()    #dropping and rows with null values

    present_users = dfmain[dfmain["Status"] == "Present"]["User Email"].tolist()    #made the emails of present students into a list
    print(present_users)

    return eventname,startdate,enddate


if __name__ == "__main__":
    main("sample.csv") 