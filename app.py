from flask import Flask, request, render_template, flash, redirect, url_for
import os


app=Flask(__name__)
app.config["UPLOADFOLDER"]="uploads"

@app.route("/",methods=["GET", "POST"])
def index():
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
    alerts=None
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
        zoomreport = request.files.get("zoomreport")
        if zoomreport and zoomreport.filename != "":
            filename=zoomreport.filename.lower()
            if filename.endswith((".xls", ".xlsx", ".csv")):   
                filepath=os.path.join(app.config["UPLOADFOLDER"], filename)
                zoomreport.save(filepath)
                alerts=False
            else:
                alerts=True
                return render_template("index.html", alerts=alerts)
            
        print("Event Name:", eventname)
        print("Description:", description)
        print("City:", city)
        print("Country:", country)
        print("Start Date:", startdate)
        print("End Date:", enddate)
        print("Expiry Date:", expirydate)
        print("Secret Code:", secretcode)
        print("Email:", email)
        
    return render_template("index.html",alerts=alerts)

if __name__=="__main__":
    app.run(debug=True)