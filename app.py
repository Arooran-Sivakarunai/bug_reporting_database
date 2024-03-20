from flask import Flask, render_template, request, url_for, flash, redirect
from flask import g
import sqlite3

DATABASE = './databases/main.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

app = Flask(__name__)
#test
@app.route("/")
def index():
    return render_template("index.html", logged_in = False)

@app.route('/create', methods=('GET','POST'))
def create():
    if request.method == 'POST':
        userID = int(request.form['userID'])
        username = request.form['username']
        password = request.form['password']
        if not userID:
            flash('UserID is required!')
        elif not username:
            flash('Content is required!')
        elif not password:
            flash('Password is required!')
        else:
            make_new_user(userID, username, password)
            return redirect(url_for('index'))
    return render_template("create_user.html")

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

def auth_new_user(info: tuple, conn: any) -> bool:
    query = f"""SELECT * FROM users"""
    cur = conn.cursor()
    
    try:
        cur.execute(query)
        results = cur.fetchall()
        print(results)
        return info not in results
    except:
        return False
    
    