from flask import Flask, render_template, request, url_for, flash, redirect, g
from flask_mail import Mail, Message
import sqlite3
import os
import users as u

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
    return render_template("index.html", user=user)

@app.route('/createuser', methods=('GET','POST'))
def create():
    try:
        if request.method == 'POST':
            userID = int(request.form['userID'])
            username = request.form['username']
            password = request.form['password']
            make_new_user(u.User.validate_info(user_id = userID, username = username, user_password = password))
            return redirect(url_for('index', user=None))
        
    except ValueError:
        flash("UserID must be Valid Integer")
    except u.UserIDRequired:
        flash('UserID is required!')
    except u.UserNameRequired:
        flash('username is required!')
    except u.PasswordRequired:
        flash('Password is not strong enough!')
    except u.UserIDTaken:
        flash("UserId already has Associated Account")
    except Exception as e:
        print(e)
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
                    user = get_user_login(username, u.User.get_password_hash(password))
                    if(user != None):
                        return redirect(url_for('index'))
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


def make_new_user(info) -> None:
    conn = get_db()
    cur = conn.cursor()

    if(auth_new_user(info, conn)):
        query = f"""INSERT INTO users (
            userID, username, password)
            VALUES (?, ?, ?)"""
        
        try:
            cur.execute(query, info)
            conn.commit()
        except:
            conn.rollback()
            conn.close()
            return False
        conn.close()
        return True
    else:
        conn.close()
        raise u.UserIDTaken
    

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
        return u.User(res)
    except:
        return None
        
