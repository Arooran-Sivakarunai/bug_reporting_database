from flask import Flask
from flask_mail import *

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["MAIL_SERVER"] = "smtp.fastmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "dummy123@fastmail.com"
    app.config["MAIL_PASSWORD"] = "7vk78zb6yj2cykwu"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail.init_app(app)

    @app.route("/")

    # check to see if provided email is in the database
    # if it is, send link with update_password.html form 
    # else, return "Account does not exist."
    

    def index():
        msg = Message (
            'Reset Password', 
            sender = 'dummy123@fastmail.com',
            recipients=["dummy123@fastmail.com", "melissamdelacruz@hotmail.com"] #hardcoding :p
        )
        msg.body = "Click the Link to Reset your Password: Link"
        
        with app.app_context():
            mail.send(msg)
        return "Password Reset Link Set, Please check your mail."
    
    return app
