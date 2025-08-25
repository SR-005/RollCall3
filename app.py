from flask import Flask, request, render_template,redirect
import os
from dotenv import load_dotenv

load_dotenv()
CLIENTID=os.getenv("CLIENT_ID")
CLIENTSECRET=os.getenv("CLIENT_SECRET")
REDIRECTURI = "http://localhost:5000/callback"

app=Flask(__name__)
@app.route("/")
def index():
    zoom_auth_url = (
        "https://zoom.us/oauth/authorize"
        f"?response_type=code&client_id={CLIENTID}&redirect_uri={REDIRECTURI}"
    )
    return redirect(zoom_auth_url)

if __name__=="__main__":
    app.run(debug=True)