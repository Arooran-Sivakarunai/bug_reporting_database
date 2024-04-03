from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from passwords import get_password_hash, validate_passwords
from checkCreds import check_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_credentials.db'
db = SQLAlchemy(app)


class UserCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)


def goodPass(new_password, conf_password):
    email = request.form.get('email')
    if check_email(email):
        if validate_passwords(new_password) and new_password == conf_password:
            return True
        elif validate_passwords(new_password) and new_password != conf_password:
            print("Passwords must be identical.")
            return False
        else:
            print("Password does not fulfill requirements.")
            return False
    else:
        return None

def update_password(new_password, conf_password):
    if goodPass(new_password, conf_password):
        hashPass = get_password_hash(new_password)
        email = request.form.get('email')
        user = UserCredentials(email=email, hashed_password=hashPass)

        db.session.add(user)
        db.session.commit()
        print("Password Updated.")

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("update_password.html")

@app.route("/update_password", methods=["POST"])
def handle_update_password():
    new_password = request.form.get("new_password")
    conf_password = request.form.get("conf_password")
  
    result = update_password(new_password, conf_password)
    return result

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Run the app on port 5001
    app.run(port=5001)
