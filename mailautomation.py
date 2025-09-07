from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)
def main(email,eventid,secretcode):
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

            👉 You can check your event status directly on RollCall3 by entering these details.

            Best,
            RollCall3 Team"""
            mail.send(msg)
            print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Mail error:", str(e))

if __name__ == "__main__":
    main("sreeramvg100@gmail.com",2005,2005)

    