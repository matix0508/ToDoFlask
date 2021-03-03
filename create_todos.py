from app import db, Todo

todos = ["Learn Flask", 'Setup venv', 'Build a cool app']

for todo in todos:
    t = Todo(todo_text=todo)
    db.session.add(t)
db.session.commit()
