import flask
import configparser
import json

config = configparser.ConfigParser()
config.read('../app.cfg')

app = flask.Flask(__name__)


@app.route('/')
def index():
    # services_path = config['PATHS']['ServicesPath']
    # print(services_path)
    with open('Services.json', 'r') as f:
        return json.loads(f.read())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
