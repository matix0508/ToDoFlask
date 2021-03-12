from flask import render_template, request, redirect, url_for, flash
from forms import TodoForm, LoginForm, NewUserForm
from models import Todo, User
from app import app, db, login_manager
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.urls import url_parse

items = []


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error.html',
                           blocked=True,
                           photo="static/NoCanDo.jpeg",
                           photo_text="No Can Do",
                           text="Daaaamn, Looks like you have wrong Address",
                           title="No Can Do"
                           ), 404


@login_manager.unauthorized_handler
def unauthorized():
    return render_template(
        'error.html',
        blocked=True,
        photo="static/ThereIsNoTry.jpg",
        photo_text="Try Not",
        text="Looks Like You have no power Here, Are you lost?",
        title="Try Not"
                           )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/nope")
@login_required
def nope():
    return render_template('error.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # return redirect(url_for('panel'))
            flash("Invalid username or password")
            return redirect(url_for('nope'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, blocked=True)


@app.route('/', methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        logged_in = True
        login_on = False
    else:
        return redirect(url_for('login'))
    if 'todo' in request.form:
        if request.form['todo']:
            item = Todo(todo_text=request.form['todo'])
            if logged_in:
                item.owner = current_user.id
            else:
                items.append(item)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))
    # todos = []
    if logged_in:
        todos = Todo.query.filter_by(owner=current_user.id).all()
    else:
        todos = items
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
@login_required
def remove_todo(todo_id):
    my_todo = Todo.query.get(todo_id)
    if not current_user.admin or current_user.id == my_todo.owner:
        redirect(url_for('nope'))
    db.session.delete(my_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/panel')
@login_required
def panel():
    if not current_user.admin:
        return redirect(url_for('nope'))
    models = [User, Todo]
    names = ["User", "Todo"]
    return render_template('panel.html', models=models, names=names, items=len(names), panel=True)


@app.route('/panel/add_user')
@login_required
def add_user():
    if not current_user.admin:
        return redirect(url_for('nope'))

    return render_template("new_user.html", form=NewUserForm())
