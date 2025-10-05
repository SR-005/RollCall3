from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)
def main(email,eventid,secretcode,totalemails):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USER")  
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASS")   
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USER")
    mail=Mail(app)

    try:
        with app.app_context():
            msg = Message("Your RollCall3 Event Details", recipients=[email])
            msg.body = f"""
            Hello 👋,

            Your POAP Event has been created successfully!

            Event ID: {eventid}
            Secret Code: {secretcode}

            NOTE: Number of Mint Links to be Requested: {totalemails}

            👉 You can check your event status directly on RollCall3 by entering these details.

            Best,
            RollCall3 Team"""
            mail.send(msg)
            print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Mail error:", str(e))

def sendmails(userdata,links,eventname):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USER")  
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASS")   
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USER")
    mail=Mail(app)

    names=list(userdata.keys())
    emails=list(userdata.values())

    iteration=0
    for email in emails:
        link=links[iteration]
        name=names[iteration]
        print(name)
        print(email)
        print(link)
        try:
            with app.app_context():
                msg = Message("Your RollCall3 Event Details", recipients=email)
                msg.body = f"""
                Hello {name},

                This is an automated mail service from the RollCall3 Team. You have been approved to be a Holder of a POAP Badge with regards of the Event you recently attended.
                

                Here is your Claim Link : {link}

                WARNING: DO NOT SHARE THIS LINK WITH ANYONE. THIS IS A ONE TIME CLAIMABLE LINK. SO BE SURE TO CLAIM IT AS FAST AS POSSIBLE.

                Best,
                RollCall3 Team"""
                mail.send(msg)
                print("✅ Email sent successfully")
        except Exception as e:
            print("❌ Mail error:", str(e))
        iteration=iteration+1
    


if __name__ == "__main__":
    main("sreeramvg100@gmail.com",2005,2005)

    