from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Initialize database
if os.environ.get('DATABASE_URL'):
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# Models

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id

# Routes

@app.route('/')
def index():
  return redirect(url_for('todos_index'))


@app.route('/todos', methods=['POST', 'GET'])
def todos_index():
  if request.method == 'POST':
    task_content = request.form['content']
    new_task = Todo(content=task_content)

    try:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/')
    except:
      return '🤔 The task could not be added'
  else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", tasks=tasks)


@app.route('/todos/<int:id>/delete')
def todos_delete(id):
  task_to_delete = Todo.query.get_or_404(id)

  try: 
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return '🤔 Oh. The task could not be deleted.'



@app.route('/todos/<int:id>/update', methods=['GET', 'POST'])
def todos_update(id):
  task = Todo.query.get_or_404(id)

  if request.method == 'POST':
    task.content = request.form['content']

    try:
      db.session.commit()
      return redirect('/')
    except:
      return '🤔 Well that did not work updating the task.'
  else:
    return render_template('update.html', task=task)

# Run the server

if __name__ == "__main__":
  app.run(debug=True)