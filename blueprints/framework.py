# noinspection PyUnusedLocal,PyPep8Naming
import flask
from flask_login import login_required


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
                x['view_function'] = app.route(x['endpoint'], methods=x['method'])(
                    login_required(x['view_function']))
            else:
                x['view_function'] = app.route(x['endpoint'], methods=x['method'])(
                    x['view_function'])
    except AssertionError:
        pass
