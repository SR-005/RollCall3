import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import requests

#LOADING CREDENTIALS FROM .ENV
load_dotenv()
API_KEY = os.getenv("POAP_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")



#----------------------------------------------------------------------DATA SECTION----------------------------------------------------------------------

#DATA HANDLING AND PROCESSING
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



#----------------------------------------------------------------------API SECTION----------------------------------------------------------------------

'''#Creating Event through API Requests
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
print(response.text)'''

#Verifying Event Creationg - Data Fetching
url = "https://api.poap.tech/events/id/200582"
headers = {
    "accept": "application/json",
    "x-api-key": API_KEY
}
response = requests.get(url, headers=headers)
print(response.text)

'''url = f"https://api.poap.tech/events/200582/mint-links"
headers = {
    "x-api-key": API_KEY,
    "accept": "application/json",
    "content-type": "application/json"
}

payload = {
    "secret_code": "example-secret-2025",   # choose any random string
    "email": "test@example.com",       # issuer email
    "links_count": 20                       # number of claim links you want
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    print("✅ Mint Links Generated:")
    for link in data.get("links", []):
        print(link)
else:
    print("❌ Error:", response.status_code, response.text)'''



url = "https://api.poap.tech/event/200582/qr-codes"

payload = { "secret_code": "234789" }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExQVB4Sy0tMjdnVUlSVFhGaXFtTSJ9.eyJpc3MiOiJodHRwczovL2Rldi0yamEzd3ZrdGQ1NGszbW5uLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJkYjFpcEpuekd4THRPVEdzbzhGazhNUjFnZWhJOVhwS0BjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9yb2xsY2FsbDMuYXBpIiwiaWF0IjoxNzU2ODIzMDExLCJleHAiOjE3NTY5MDk0MTEsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6ImRiMWlwSm56R3hMdE9UR3NvOEZrOE1SMWdlaEk5WHBLIn0.sKldG5_QaZj3MHQCnA4-lVKf3LlpnBnaoKxPXSN7YK4KZNTN2OHUs1ALzjPW57LDI2cz0dAU2Ezm8-h7FlSbN8Ct3_HudsV1TvnKoteWDk_JNc2xsb4FFnkr7BE_OWrdIIvgi-scGl4jp1356bsgbMClh72nLej692W5Xpu1Lqn2_LgVS7tgC9Cf4q11eefxYk8BQoH2Y38WNoWb5McyHncEGYIahE-J8gkc_CcBU0lRKvMMxkSLsgYihcoEVBSsFxin9U9cvtkTGB6lejxeuBwbWbebCUU378ltB9JkSkNPhsmddqKhTkGfbG_KnXO3Qk-vyabGC06jZrfH5AlqeQ",
    "x-api-key": "w0OvficGb8l5sJ2SaDANHQpPGhhsyiIhJ9eBcoOQGKrxRhfGYdO4PgstV5yczmuz8v8w9JlwpIvXRt52dABFpwUegEbJEmDpNJBxwoE9t7lXfCcn00szniKzdlj7NJ0B"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)