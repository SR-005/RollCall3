import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import requests
import json

def main():
    #LOADING CREDENTIALS FROM .ENV
    load_dotenv()
    API_KEY = os.getenv("POAP_API_KEY")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    #----------------------------------------------------------------------DATA SECTION----------------------------------------------------------------------

    #DATA HANDLING AND PROCESSING
    dforg=pd.read_csv("sample.csv")
    print("SUCCESFULLY RECIEVED CSV FILE")
    #converting str->datetime
    dforg["Start Time"]=pd.to_datetime(dforg["Start Time"])
    dforg["End Time"]=pd.to_datetime(dforg["End Time"])
    dforg["Session Duration"]=(dforg["End Time"]-dforg["Start Time"]).dt.total_seconds() / 60   #calculating meeting duration and converting it to minutes
    dforg["Session Duration"]=dforg["Session Duration"].astype(int) #converting it to int values
    dfmain=dforg.drop(["Join Time","Leave Time","Guest","Meeting ID","Topic","Start Time","End Time"],axis=1) #dropping uncessesary datas; Axis=1-coloumn

    #calculating minimum presence time
    minimumtime=dfmain.loc[0, "Session Duration"]
    minimumtime=round((minimumtime/100)*75) #75% attendence given
    print("Minimum Time of Presence in Event",minimumtime)

    dfmain["Status"]=np.where(dfmain["Duration"] >= minimumtime,"Present","Absent") #created a present/absent coloumn
    dfmain = dfmain.dropna()    #dropping and rows with null values

    present_users = dfmain[dfmain["Status"] == "Present"]["User Email"].tolist()    #made the emails of present students into a list
    print(present_users)



    #----------------------------------------------------------------------API SECTION----------------------------------------------------------------------

    #Creating Event through API Requests
    url = "https://api.poap.tech/events"    
    #Image for Badge logo
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
    if response.status_code==200:
        print("Event Created Succesfully")
    else:
        print(response.text)


    #Verifying Event Creationg - Data Fetching
    url = "https://api.poap.tech/events/id/200582"
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code==200:
        print("Event Creation Verified Succesfully")
    else:
        print(response.text)


    #Generating Access Token
    url = "https://auth.accounts.poap.xyz/oauth/token"
    payload = {
        "audience": "https://api.poap.tech",   
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data=response.json()
    '''print("Status Code:", response.status_code)
    print("Response:", response.json())'''
    ACCESS_TOKEN=data["access_token"]
    if ACCESS_TOKEN!=None:
        print("Access Token Generated Successfully")
    else:
        print("Error in Generating Access Token")
    '''print("Access Token:", ACCESS_TOKEN)'''


    url = "https://api.poap.tech/event/200582/qr-codes"

    payload = {
        "qr_codes_count": 10,        # how many mint links you want
        "secret_code": "234789"      # must match the event's secret_code
    }

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code, res.text)
main()