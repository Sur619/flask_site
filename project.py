import os, flask, sqlite3
from flask import render_template, request, g, url_for, render_template, flash, abort
from FDataBase import FDataBase

DATABASE = 'D:/python_project/dop_study_flask/project.db'
DEBUG = True
secret_key = '!@@#$%^&%^&^*((*()()__)_+*(&*&^%%$##@#@#'

app = flask.Flask(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'project.db')))
app.config.from_object(__name__)
app.secret_key = '!@@#$%^&%^&^*((*()()__)_+*(&*&^%%$##@#@#'

def db_connect():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def db_create():
    db = db_connect()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()



@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link.db'):
        g.link.db.close()

@app.route('/')
def index():
    db = db_connect()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())

@app.route("/addpost", methods=["POST", "GET"])
def addpost():
    db = db_connect()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addpost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")

@app.route('/post/<alias>')
def showPost(alias):
    db = db_connect()
    dbase = FDataBase(db)

    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.route('/rating')
def rating():
    db = db_connect()
    dbase = FDataBase(db)

    return render_template('rating.html', menu=dbase.getMenu(), title='Rating', post='smth very importent')

if __name__ == '__main__':
    app.run(debug=True)
