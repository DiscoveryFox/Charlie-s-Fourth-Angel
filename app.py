#!/usr/bin/python
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit( )
            return redirect('/')
        except:
            return 'There was an Issue adding your task to the database'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all( )
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit( )
        return redirect('/')
    except:
        return "There was a Problem deleting that Task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit( )
            return redirect('/')
        except:
            return 'There was an issue updating your Task'
    else:
        return render_template('update.html', task=task)



@app.route('/CamPhish/')
def camphish_create() -> str:
    print(request.method)
    service = request.args.get('port_forwarding')
    template = request.args.get('template')
    ngrok_url = "test"
    return render_template('Camphish.html', ngrok_url=ngrok_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
