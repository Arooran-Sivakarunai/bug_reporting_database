from flask import Flask, request, render_template
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

    @app.route("/", methods=['GET', 'POST'])


    def index():
        return render_template("forgot_username.html")
    
    @app.route("/send_username", methods=["POST"])

    def send_username():
        email = request.form.get("email")

        if email: 

            msg = Message (
            'Here is Your Username!', 
            sender = 'dummy123@fastmail.com',
            recipients=["dummy123@fastmail.com", email] 
            )
            msg.body = "Username: XYZ"
        
            with app.app_context():
                mail.send(msg)
            return "Username Sent. Please check your mail."
        else: 
            return "Account does not exist."
    
    return app


if __name__ == "__main__":
    # Run the app on port 5001
    app = create_app()
    app.run(port=5001)