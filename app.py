from flask import Flask, request, render_template,session
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from apihandler import main as apifunction
from apihandler import mintlinkgeneration as mintlinkgeneration
from reporthandler import main as reportfunction
from mailautomation import sendmails


app=Flask(__name__)
app.config["UPLOADFOLDER"]="uploads"
load_dotenv()
app.secret_key = os.getenv("SESSION_SECRET", os.urandom(24))

#Main Home Page
@app.route("/")
def index():
    return render_template("index.html",fileindicator=True)

fileindicator=True      #Indicator for whether the csv file has been recieved correctly
#Function for 'Auto Fill' Button
@app.route("/vcsv",methods=["GET", "POST"])
def vcsv():
    alerts=None
    fileindicator=True
    eventname=None
    startdate=None
    enddate=None
    totalemails=None
    if request.method=="POST":
        zoomreport = request.files.get("zoomreport")

        #checks if the file recieved is csv/excel file or not
        if zoomreport and zoomreport.filename != "":
            filename=zoomreport.filename.lower()
            if filename.endswith((".xls", ".xlsx", ".csv")):   
                filepath=os.path.join(app.config["UPLOADFOLDER"], filename)
                zoomreport.save(filepath)
                alerts1=False
                fileindicator=False
            else:
                alerts1=True
                fileindicator=True
                return render_template("index.html", alerts1=alerts1,fileindicator=fileindicator)
        eventname,startdate,enddate,verifiedmails,totalemails=reportfunction(filepath)    #csv handling function call
        session["verifiedmails"] = verifiedmails
        session["eventname"] = eventname
        session["totalemails"] = totalemails


        #converting Start Date and End Date to formats HTML Autofill Values
        if isinstance(startdate, datetime):
            startdate = startdate.strftime("%Y-%m-%d")
        if isinstance(enddate, datetime):
            enddate = enddate.strftime("%Y-%m-%d")
        
    return render_template("index.html",alerts1=alerts1,fileindicator=fileindicator,eventname=eventname,startdate=startdate,enddate=enddate)

#function for 'Generate POAP' button
@app.route("/vevent",methods=["GET", "POST"])
def vevent():
    eventid=None
    eventname=None
    description=None
    iconpath=None
    city=None
    country=None
    startdate=None
    enddate=None
    expirydate=None
    secretcode=None
    email=None
    eventurl=None
    privateevent=None
    virtualevent=None
    filepath=None
    alerts2=None
    iconalert=None
    verifiedmails=None
    totalemails=None
    
    if request.method=="POST":
        eventname = request.form.get("eventname")
        description = request.form.get("description")
        icon=request.files.get("icon")
        city = request.form.get("cityname")
        country = request.form.get("countryname")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        expirydate = request.form.get("expirydate")
        secretcode = request.form.get("secretcode")
        email = request.form.get("email")
        privateevent=request.form.get("privateevent")
        virtualevent=request.form.get("virtualevent")

        session["eventname"] = eventname

        if icon and icon.filename!="":
            iconname=icon.filename.lower()
            if iconname.endswith((".jpg", ".png")):
                iconpath=os.path.join(app.config["UPLOADFOLDER"], iconname)
                icon.save(iconpath)
                iconalert=False
            else:
                iconalert=True
                return render_template("index.html",alerts2=alerts2,iconalert=iconalert,fileindicator=True)

        #Converting Start Date, End Date and Expiry Date to formats required for POAP API call
        startdate=datetime.strptime(startdate,"%Y-%m-%d").strftime("%m-%d-%Y")
        enddate=datetime.strptime(enddate,"%Y-%m-%d").strftime("%m-%d-%Y")
        expirydate=datetime.strptime(expirydate,"%Y-%m-%d").strftime("%m-%d-%Y")

        #Clearing of Null values
        if privateevent==None:
            privateevent="false"
        if virtualevent==None:
            virtualevent="false"

        #If user enters the details manually
        try:
            zoomreport = request.files.get("zoomreport2")
            if zoomreport and zoomreport.filename != "":
                filename=zoomreport.filename.lower()
                if filename.endswith((".xls", ".xlsx", ".csv")):   
                    filepath=os.path.join(app.config["UPLOADFOLDER"], filename)
                    zoomreport.save(filepath)
                    alerts2=False
                else:
                    alerts2=True
                    
        except:
            pass
            
        print("Event Name:", eventname)
        print("Description:", description)
        print("Icon Path: ", iconpath)
        print("City:", city)
        print("Country:", country)
        print("Start Date:", startdate)
        print("End Date:", enddate)
        print("Expiry Date:", expirydate)
        print("Secret Code:", secretcode)
        print("Email:", email)
        print("Private Event:", privateevent)
        print("Virtual Event:", virtualevent)
        print("Filepath: ",filepath)
        if filepath!=None:
            eventname2,startdate,enddate,verifiedmails,totalemails=reportfunction(filepath)
            session["verifiedmails"] = verifiedmails
        verifiedmails=session.get("verifiedmails", [])


        totalemails=session.get("totalemails")
        eventid,secretcode=apifunction(eventname,description,iconpath,city,country,startdate,enddate,expirydate,secretcode,email,privateevent,virtualevent,totalemails)
        with open(f"uploads/{eventid}_verified.json", "w") as f:
            json.dump(verifiedmails, f)

    return render_template("index.html",alerts2=alerts2,iconalert=iconalert,fileindicator=True,eventid=eventid,secretcode=secretcode)

#Function for External Events Page
@app.route("/externalevent",methods=["GET", "POST"])
def externalevent():
    alerts3=None
    eventid=None
    eventname=None
    description=None
    city=None
    country=None
    startdate=None
    enddate=None
    expirydate=None
    secretcode=None
    email=None
    eventurl=None
    privateevent=None
    virtualevent=None
    filepath=None
    iconalert=None

    if request.method=="POST":
        eventname = request.form.get("eventname")
        description = request.form.get("description")
        icon=request.files.get("icon")
        city = request.form.get("cityname")
        country = request.form.get("countryname")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        expirydate = request.form.get("expirydate")
        secretcode = request.form.get("secretcode")
        email = request.form.get("email")
        privateevent=request.form.get("privateevent")
        virtualevent=request.form.get("virtualevent")

        session["eventname"] = eventname

        if icon and icon.filename!="":
            iconname=icon.filename.lower()
            if iconname.endswith((".jpg", ".png")):
                iconpath=os.path.join(app.config["UPLOADFOLDER"], iconname)
                icon.save(iconpath)
                iconalert=False
            else:
                iconalert=True
                return render_template("index.html",alerts3=alerts3,iconalert=iconalert)

        #Converting Start Date, End Date and Expiry Date to formats required for POAP API call
        startdate=datetime.strptime(startdate,"%Y-%m-%d").strftime("%m-%d-%Y")
        enddate=datetime.strptime(enddate,"%Y-%m-%d").strftime("%m-%d-%Y")
        expirydate=datetime.strptime(expirydate,"%Y-%m-%d").strftime("%m-%d-%Y")

        #Clearing of Null values
        if privateevent==None:
            privateevent="false"
        if virtualevent==None:
            virtualevent="false"

        zoomreport = request.files.get("zoomreport2")
        if zoomreport and zoomreport.filename != "":
            filename=zoomreport.filename.lower()
            if filename.endswith((".xls", ".xlsx", ".csv")):   
                filepath=os.path.join(app.config["UPLOADFOLDER"], filename)
                zoomreport.save(filepath)
                alerts3=False
            else:
                alerts3=True

            
        print("Event Name:", eventname)
        print("Description:", description)
        print("City:", city)
        print("Country:", country)
        print("Start Date:", startdate)
        print("End Date:", enddate)
        print("Expiry Date:", expirydate)
        print("Secret Code:", secretcode)
        print("Email:", email)
        print("Private Event:", privateevent)
        print("Virtual Event:", virtualevent)
        print("Filepath: ",filepath)

        eventname2,startdate,enddate,verifiedmails=reportfunction(filepath)
        eventid,secretcode=apifunction(eventname,description,iconpath,city,country,startdate,enddate,expirydate,secretcode,email,privateevent,virtualevent)
        verifiedmails=session.get("verifiedmails", [])
        with open(f"uploads/{eventid}_verified.json", "w") as f:
            json.dump(verifiedmails, f)

    return render_template("externalevent.html",alerts3=alerts3,eventid=eventid,secretcode=secretcode)

@app.route("/help")
def helppage():
    return render_template("help.html")

@app.route("/search",methods=["GET", "POST"])
def search():
    eventid=None
    secretcode=None
    status=None
    claimlinks=None
    
    if request.method=="POST":
        eventid=request.form.get("eventid")
        secretcode=request.form.get("secretcode")
        status,claimlinks=mintlinkgeneration(eventid,secretcode)
        session["claimlinks"]=claimlinks
        session["eventid"]=eventid

    return render_template("index.html",status=status)

@app.route("/sendlinks",methods=["GET", "POST"])
def sendlinks():
    verifiedmails=None

    if request.method=="POST":
        verifiedmails=session.get("verifiedmails", [])
        claimlinks=session.get("claimlinks", [])
        eventname=session.get("eventname")

        eventid = session.get("eventid")
        print(eventid)
        if (not verifiedmails) and eventid:
            try:
                with open(f"uploads/{eventid}_verified.json") as f:
                    verifiedmails = json.load(f)
            except FileNotFoundError:
                verifiedmails = []

        print("Mails:", verifiedmails)
        print("Links",claimlinks)
        sendmails(verifiedmails,claimlinks,eventname)
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)