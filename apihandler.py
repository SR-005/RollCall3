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


def main(eventname,description,iconpath,city,country,startdate,enddate,expirydate,secretcode,email,privateevent,virtualevent,totalemails):
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
            os.path.basename(iconpath),   
            open(iconpath, "rb"),        
            "image/png" if iconpath.lower().endswith(".png") else "image/jpg"
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
        "email": email,
        "secret_code": secretcode
    }
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY
    }
    response = requests.post(url, data=payload, files=files, headers=headers)
    if response.status_code==200:
        eventdata=response.json()   
        eventid=eventdata.get("id")   
        print("Event Created Succesfully")
    else:
        print(response.text)


    #Verifying Event Creationg - Data Fetching
    url = f"https://api.poap.tech/events/id/{eventid}"
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code==200:
        print("Event Creation Verified Succesfully")
        sendmail(email,eventid,secretcode,totalemails)
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


    url = f"https://api.poap.tech/event/{eventid}/qr-codes"

    payload = {
        "qr_codes_count": 10,        
        "secret_code": secretcode      
    }

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, headers=headers, json=payload)
    print(res.status_code, res)
    if res.status_code==200 and res.text!="[]":
        claimlinks=[]
        for dict in res.json():
                qr=dict["qr_hash"]
                link=f"https://poap.xyz/claim/{qr}"
                claimlinks.append(link)
        status=1
    else:
        status=0
    print(claimlinks)
    return status,claimlinks


if __name__ == "__main__":
    mintlinkgeneration(0,0)