import os
from dotenv import load_dotenv
import requests
import json
from mailautomation import main as sendmail

#LOADING CREDENTIALS FROM .ENV
load_dotenv()
API_KEY = os.getenv("POAP_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def main(eventname,description,iconpath,city,country,startdate,enddate,expirydate,secretcode,email,privateevent,virtualevent):
    print("Event Name:", eventname)
    print("Description:", description)
    print("Icon Path: ",iconpath)
    print("City:", city)
    print("Country:", country)
    print("Start Date:", startdate)
    print("End Date:", enddate)
    print("Expiry Date:", expirydate)
    print("Secret Code:", secretcode)
    print("Email:", email)
    print("Private Event:", privateevent)
    print("Virtual Event:", virtualevent)
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
        "private_event": privateevent,
        "notify_issuer": "true",
        "name": eventname,
        "description": description,
        "city": city,
        "country": country,
        "start_date": startdate,
        "end_date": enddate,
        "expiry_date": expirydate,
        "email": "test@example.com",
        "secret_code": secretcode
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
        eventdata = response.json()
        eventid = eventdata.get("id")
        '''sendmail(email,eventid,secretcode)'''
    else:
        print(response.text)

    return eventid,secretcode


def mintlinkgeneration(eventid,secretcode):
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
    ACCESS_TOKEN=data["access_token"]
    if ACCESS_TOKEN!=None:
        print("Access Token Generated Successfully")
    else:
        print("Error in Generating Access Token")
    '''print("Access Token:", ACCESS_TOKEN)'''


    url = "https://api.poap.tech/event/200582/qr-codes"

    payload = {
        "qr_codes_count": 10,        
        "secret_code": "234789"      
    }

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code, res.text)
    if res.status_code==200 and res.text!="[]":
        status=1
    else:
        status=0
    return status

if __name__ == "__main__":
    mintlinkgeneration(200582,234789)