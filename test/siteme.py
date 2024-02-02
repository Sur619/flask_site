from flask import Flask, render_template, request, redirect, url_for, flash, session, redirect, send_from_directory, \
    abort

import sqlite3, os

DATABASE = 'D:\python_project\dop_study_flask\siteme.db'
DEBUG = True
SECRET_KEY = '2!@##$%^&*(_*(*&^%^$$#$&&&('

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(database=os.path.join(app.root_path, 'siteme.db')))

menu = [
    {'name': 'install', 'url': 'install-flask'},
    {'name': 'first app', 'url': 'first-app'},
    {'name': 'contact', 'url': 'contact'}
]


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


create_db()


@app.route('/')
def index():
    return render_template('index.html', title='Home', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='About this site', menu=menu)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('message send', category='success')
        else:
            flash('message failed', category='error')
    return render_template('contact.html', title='Contact', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='ops something went wrong', menu=menu), 404


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Sura' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Login', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)


'''with app.test_request_context():
    print(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)
'''
