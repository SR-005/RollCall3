from flask import Flask, request, render_template
import os
from datetime import datetime
from apihandler import main as apifunction
from reporthandler import main as reportfunction

app=Flask(__name__)
app.config["UPLOADFOLDER"]="uploads"

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
        eventname,startdate,enddate=reportfunction(filepath)    #csv handling function call

        #converting Start Date and End Date to formats HTML Autofill Values
        if isinstance(startdate, datetime):
            startdate = startdate.strftime("%Y-%m-%d")
        if isinstance(enddate, datetime):
            enddate = enddate.strftime("%Y-%m-%d")
        
    return render_template("index.html",alerts1=alerts1,fileindicator=fileindicator,eventname=eventname,startdate=startdate,enddate=enddate)

#function for 'Generate POAP' button
@app.route("/vevent",methods=["GET", "POST"])
def vevent():
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
    alerts2=None
    
    if request.method=="POST":
        eventname = request.form.get("eventname")
        description = request.form.get("description")
        city = request.form.get("cityname")
        country = request.form.get("countryname")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        expirydate = request.form.get("expirydate")
        secretcode = request.form.get("secretcode")
        email = request.form.get("email")
        privateevent=request.form.get("privateevent")
        virtualevent=request.form.get("virtualevent")

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
            reportfunction(filepath)
        apifunction(eventname,description,city,country,startdate,enddate,expirydate,secretcode,email,privateevent,virtualevent)
        
    return render_template("index.html",alerts2=alerts2,fileindicator=True)

#Function for External Events Page
@app.route("/externalevent",methods=["GET", "POST"])
def externalevent():
    alerts3=None
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

    if request.method=="POST":
        eventname = request.form.get("eventname")
        description = request.form.get("description")
        city = request.form.get("cityname")
        country = request.form.get("countryname")
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        expirydate = request.form.get("expirydate")
        secretcode = request.form.get("secretcode")
        email = request.form.get("email")
        privateevent=request.form.get("privateevent")
        virtualevent=request.form.get("virtualevent")

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
        reportfunction(filepath)
        apifunction(eventname,description,city,country,startdate,enddate,expirydate,secretcode,email,privateevent,virtualevent)

    return render_template("externalevent.html",alerts3=alerts3)



if __name__=="__main__":
    app.run(debug=True)