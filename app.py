from flask import Flask, request, render_template

app=Flask(__name__)
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
        eventurl = request.form.get("eventurl")
        zoomreport = request.files.get("zoomreport")
        print("Event Name:", eventname)
        print("Description:", description)
        print("City:", city)
        print("Country:", country)
        print("Start Date:", startdate)
        print("End Date:", enddate)
        print("Expiry Date:", expirydate)
        print("Secret Code:", secretcode)
        print("Email:", email)
        print("Event URL:", eventurl)
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)