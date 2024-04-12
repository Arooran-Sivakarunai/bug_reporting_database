from flask import Flask, render_template, request, url_for, flash, redirect, g
from flask_mail import Mail, Message
import sqlite3
import os
import users as u
import bugs as b

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
        # print(e)
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
    except Exception as e:
        print('uh oh', e)
    return render_template("log_in.html")

@app.route('/make_new_bug', methods=('GET','POST'))
def make_new_bug():
    try:
        if request.method == 'POST':
            if request.form.get("Cancel"):
                return redirect(url_for('index', user=user))
            if request.form.get("Save"):
                try:
                    save_to_temp(request.form, user, False)
                    return redirect(url_for('my_bugs'))
                except Exception as e:
                    print(e)
                    return redirect(url_for('index'))
            # if request.form.get("Log In"):
            #     username = request.form['username']
            #     password = request.form['password']
            #     if not username:
            #         flash('username is required!')
            #     elif not password:
            #         flash('Password is not strong enough!')
            #     else:
            #         global user 
            #         user = get_user_login(username, u.User.get_password_hash(password))
            #         if(user != None):
            #             return redirect(url_for('index'))
            #         else:
            #             flash('Either Username or Password is Incorrect')
    except Exception as e:
        print('uh oh', e)
    return render_template("make_bug.html")

@app.route("/my_bugs")
def my_bugs():
    print(user)
    return render_template('my_bugs.html', unfinished_bugs=get_unfinished_bugs(user.user_id))

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
        
def get_unfinished_bugs(uID: int):
    conn = get_db()
    cur = conn.cursor()
    query = f"""SELECT * FROM temp_reports WHERE user_id == ?"""
    print(uID)
    res = cur.execute(query, (uID,)).fetchall()
    final = []
    for bug in res:
        print(bug)
        final.append(b.Bug(bug_id=bug[0],user_id=bug[1],date=bug[2],bug_title=bug[3],bug_summary=bug[4],priority=bug[5],notify=bug[6]))
    
    return final

def save_to_temp(rForm, user, is_in_db):
    conn = get_db()
    cur = conn.cursor()
    try:
        if(is_in_db):
            print(rForm)
        else:
            query = f"INSERT INTO temp_reports (user_id, date, bug_title, bug_summary, priority, notify) VALUES (?, ?, ?, ?, ?, ?)"
            bug = b.make_new_bugs(rForm, user.user_id)[1:]
            cur.execute(query, bug)
            conn.commit()
            
    except Exception as e:
        print(e)
    conn.close()