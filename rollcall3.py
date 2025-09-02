import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("POAP_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

dforg=pd.read_csv("sample.csv")
#converting str->datetime
dforg["Start Time"]=pd.to_datetime(dforg["Start Time"])
dforg["End Time"]=pd.to_datetime(dforg["End Time"])
dforg["Session Duration"]=(dforg["End Time"]-dforg["Start Time"]).dt.total_seconds() / 60   #calculating meeting duration and converting it to minutes
dforg["Session Duration"]=dforg["Session Duration"].astype(int) #converting it to int values
dfmain=dforg.drop(["Join Time","Leave Time","Guest","Meeting ID","Topic","Start Time","End Time"],axis=1) #dropping uncessesary datas; Axis=1-coloumn

#calculating minimum presence time
minimumtime=dfmain.loc[0, "Session Duration"]
minimumtime=round((minimumtime/100)*75) #75% attendence given
print("Minimum Time ",minimumtime)

dfmain["Status"]=np.where(dfmain["Duration"] >= minimumtime,"Present","Absent") #created a present/absent coloumn
dfmain = dfmain.dropna()    #dropping and rows with null values

present_users = dfmain[dfmain["Status"] == "Present"]["User Email"].tolist()    #made the emails of present students into a list
print(present_users)

url = "https://api.poap.tech/events"
files = {
    "image": (
        "Screenshot%202025-08-06%20123712.png",
        open("C:/Users/sreer/Downloads/Screenshot 2025-08-06 123712.png", "rb"),
        "image/png"
    )
}
payload = {
    "virtual_event": "false",
    "event_template_id": "1",
    "private_event": "false",
    "notify_issuer": "true",
    "name": "Example Event 202",
    "description": "This is an example event",
    "city": "Buenos Aires",
    "country": "Argentina",
    "start_date": "10-09-2025",
    "end_date": "12-09-2025",
    "expiry_date": "12-09-2025",
    "event_url": "https://poap.xyz",
    "email": "test@example.com",
    "secret_code": "234789"
}
headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}
response = requests.post(url, data=payload, files=files, headers=headers)
print(response.text)

url = "https://api.poap.tech/events/id/200582"
headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}
response = requests.get(url, headers=headers)

print(response.text)