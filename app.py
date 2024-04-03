from flask import Flask, render_template, request, url_for, flash, redirect, g
from flask_mail import Mail, Message
import sqlite3
import os
import passwords as p

DATABASE = './databases/main.db'
user = None

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

@app.route("/")
def index():
    print(user)
    return render_template("index.html", user=user)

@app.route('/createuser', methods=('GET','POST'))
def create():
    try:
        if request.method == 'POST':
            userID = int(request.form['userID'])
            username = request.form['username']
            password = request.form['password']
            if not userID:
                flash('UserID is required!')
            elif not username:
                flash('username is required!')
            elif not p.validate_passwords(password):
                flash('Password is not strong enough!')
            else:
                if(make_new_user(userID, username, p.get_password_hash(password))):
                    return redirect(url_for('index', user=None))
                else:
                    flash("UserId already has Associated Account")
    except ValueError:
        flash("UserID must be Valid Integer")
    except:
        flash("Something Went Terribly Wrong")
    return render_template("create_user.html")

@app.route('/login', methods=('GET','POST'))
def login():
    try:
        if request.method == 'POST':
            if request.form.get("Cancel"):
                return redirect(url_for('index', user=None))
            if request.form.get("Forgot Password"):
                return redirect(url_for('forgot_password'))
            if request.form.get("Log In"):
                username = request.form['username']
                password = request.form['password']
                if not username:
                    flash('username is required!')
                elif not password:
                    flash('Password is not strong enough!')
                else:
                    global user 
                    user = get_user_login(username, p.get_password_hash(password))
                    if(user != None):
                        return redirect(url_for('index', user=user))
                    else:
                        flash('Either Username or Password is Incorrect')
    except:
        print('uh oh')
    return render_template("log_in.html")

@app.route("/forgotpassword")
def forgot_password():
    return render_template("forgot_password.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def make_new_user(id: int, username: str, password: str) -> None:
    conn = get_db()
    cur = conn.cursor()
    
    info = (id, username, password)
    
    print("Hello")
    if(auth_new_user(info, conn)):
        query = f"""INSERT INTO users (
            userID, username, password)
            VALUES {info}"""
        
        try:
            cur.execute(query)
            conn.commit()
        except:
            conn.rollback()
            conn.close()
            return False
        conn.close()
        return True
    else:
        conn.close()
        return False
    

def auth_new_user(info: tuple, conn: any) -> bool:
    query1 = f"""SELECT * FROM users"""
    query2 = f"""SELECT userID FROM users"""
    cur = conn.cursor()
    
    try:
        cur.execute(query1)
        results = cur.fetchall()
        cur.execute(query2)
        results2 = cur.fetchall()
        print((info[0],) not in results2)
        return (info not in results) and ((info[0],) not in results2)
    except:
        return False

def get_user_login(user: str, password: str) -> any:
    query = f"""SELECT * FROM users WHERE username == ? AND password == ?"""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        res = cur.execute(query, (user, password)).fetchone()
        return res
    except:
        return None
        
