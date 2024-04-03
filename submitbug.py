# An error occurred: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand. 
# keeps showing up and not sure how to fix lol 
# make_bug.html is the render template

from flask import Flask, render_template, request, g, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'bugs.db'

SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reportNum INTEGER,
    bugType TEXT,
    bugSummary TEXT,
    updateNotifs TEXT,
    updateProgress TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.cursor().executescript(SQL_SCHEMA)
        db.commit()

@app.route('/')
def report_form():
    return render_template('make_bug.html')

@app.route('/insert_report', methods=['POST'])
def insert_report():
    try:
        report_num = request.form['reportNum']
        bug_type = request.form['bugType']
        bug_summary = request.form['bugSummary']
        update_notifs = request.form['updateNotifs']
        update_progress = request.form['updateProgress']

        db = get_db()
        db.execute('INSERT INTO reports (reportNum, bugType, bugSummary, updateNotifs, updateProgress) VALUES (?, ?, ?, ?, ?)',
                   (report_num, bug_type, bug_summary, update_notifs, update_progress))
        db.commit()

        return 'Report submitted successfully!', 'success'
    except Exception as e:
        return f'An error occurred: {str(e)}', 'error'

    return redirect(url_for('report_form'))

if __name__ == "__main__":
    app.run(port=5007)
