from flask import render_template, request, redirect, url_for
from forms import TodoForm, LoginForm
from models import Todo, User
from app import app, db, login_manager
from flask_login import login_required


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized():
    return "You have no power here"


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', template_form=LoginForm)


@app.route('/', methods=["GET", "POST"])
def index():
    if 'todo' in request.form:
        if request.form['todo']:
            db.session.add(Todo(todo_text=request.form['todo']))
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("index.html", todos=Todo.query.all(), template_form=TodoForm())


@app.route('/check/<int:todo_id>', methods=["GET", "POST"])
def check_todo(todo_id):
    my_todo = Todo.query.get(todo_id)
    my_todo.done = True
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/uncheck/<int:todo_id>', methods=["GET", "POST"])
def uncheck_todo(todo_id):
    my_todo = Todo.query.get(todo_id)
    my_todo.done = False
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/remove/<int:todo_id>', methods=["GET", "POST"])
def remove_todo(todo_id):
    my_todo = Todo.query.get(todo_id)
    db.session.delete(my_todo)
    db.session.commit()
    return redirect(url_for('index'))