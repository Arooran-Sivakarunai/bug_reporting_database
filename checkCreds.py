from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# should be connected to the original user database !!!
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_credentials.db'
db = SQLAlchemy(app)

class UserCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/check_email', methods=['GET','POST'])
def check_email():

    if request.method == 'GET':
        email = request.args.get('email')
    
    elif request.method == 'POST':
        email = request.form.get('email')

    user = UserCredentials.query.filter_by(email=email).first()

    if user:
        return jsonify({'status': 'success', 'message': 'Email exists in the database'})
        return True
    
    else:
        return jsonify({'status': 'error', 'message': 'Email does not exist'})
        return False

@app.route('/')
def index():
    return render_template('forgot_password.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
