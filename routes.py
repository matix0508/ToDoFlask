from flask import render_template, request, redirect, url_for, flash
from forms import TodoForm, LoginForm
from models import Todo, User
from app import app, db, login_manager
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.urls import url_parse


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized():
    return "You have no power here"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=LoginForm())


@app.route('/', methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        logged_in = True
        login_on = False
    else:
        logged_in = False
        login_on = True
    if 'todo' in request.form:
        if request.form['todo']:
            item = Todo(todo_text=request.form['todo'])
            if logged_in:
                item.owner = current_user.id
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))
    todos = []
    if logged_in:
        todos = Todo.query.filter_by(owner=current_user.id).all()
    return render_template(
        "index.html",
        todos=todos,
        template_form=TodoForm(),
        login_on=login_on,
        notes=True,
        logged_in=logged_in
    )


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


@app.route('/panel')
@login_required
def panel():
    if not current_user.admin:
        return redirect(url_for('unauthorized'))
    models = [User, Todo]
    names = ["User", "Todo"]
    return "panel"
