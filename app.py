from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Initialize database
if os.environ.get('DATABASE_URL'):
  # Set the database URL from the environment variable if it is set. 
  # The .replace() is a workaround because of a mismatch between Heroku's default set up and SQLAlchemy
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
else:
  # Use SQLite as a fallback and locally
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

# Models

# A basic model for Todos storing some text and the date of creation:
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id

# Routes

@app.route('/')
def index():
  # Users will always be redirected to the list of todos:
  return redirect(url_for('todos_index'))


@app.route('/todos', methods=['POST', 'GET'])
def todos_index():
  if request.method == 'POST':
    # The POST request is done by the form in the index.html file. It creates a new todo in the database
    task_content = request.form['content']
    new_task = Todo(content=task_content)

    try:
      # Try to write the new todo in the database:
      db.session.add(new_task)
      db.session.commit()
      return redirect('/todos')
    except:
      return '🤔 The task could not be added'
  else:
    # If the request is not POST return the list of ToDos from the database and render the index.html template
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", tasks=tasks)


@app.route('/todos/<int:id>/delete')
def todos_delete(id):
  # Get the todo by a given ID
  task_to_delete = Todo.query.get_or_404(id)

  try: 
    # Try to delete the todo from the database and redirect to index after
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/todos')
  except:
    return '🤔 Oh. The task could not be deleted.'



@app.route('/todos/<int:id>/update', methods=['GET', 'POST'])
def todos_update(id):
  # fint a todo by a given ID
  task = Todo.query.get_or_404(id)

  if request.method == 'POST':
    # The HTML form sends a POST request. In that case we want to update the todo with the given "conten" parameter:
    task.content = request.form['content']

    try:
      # Try to update the database:
      db.session.commit()
      return redirect('/todos')
    except:
      return '🤔 Well that did not work updating the task.'
  else:
    # Users just accessing the update page through the browser make a GET request. Display the page to them:
    return render_template('update.html', task=task)

# Run the server

if __name__ == "__main__":
  app.run(debug=True)