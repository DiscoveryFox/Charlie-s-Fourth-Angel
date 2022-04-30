import os
import json
import pip
import configparser
from pprint import pprint
import ast

import requests

config = configparser.ConfigParser()
config.read('app.cfg')


# noinspection PyUnresolvedReferences,PyProtectedMember
def prime_install(pipname: str = None, gitlink: str = None):
    if gitlink is not None:
        os.system(f'git clone {gitlink}')
    else:
        if hasattr(pip, 'main'):
            pip.main(['install', pipname])
        else:
            pip._internal.main(['install', pipname])


def get_service(name: str) -> dict:
    services = requests.get(config['PATHS']['OnlineServices']).text
    services = json.loads(services)
    if name in services:
        return {'success': 1,
                'response': services[name]
                }
    else:
        return {'success': 0,
                'response': None
                }


def add_blueprint(service_dir: str, name:str) -> str:
    # noinspection PyTypeChecker
    blueprint_content = requests.get(service_dir['path_to_blueprint']).text
    # create a new file with the name of the service + _blueprint.py and write the
    # blueprint_content in it

    with open(f'blueprints/{name}_blueprint_test.py', 'w') as file:
        file.write(blueprint_content)

    return "blueprint"


def install(name):
    service = get_service(name)
    match service['success']:
        case 1:
            with open(config['PATHS']['ServicesPath'], "r") as file:
                filecontent = json.loads(file.read())
                if name in filecontent:
                    content = filecontent
                    del content[name]
                    content_found = True
                else:
                    lines = file.readlines()
                    del lines[-1]
                    lines.append(service['response'] + "}")
                    content_found = False
            with open(config['PATHS']['ServicesPath'], "w") as file:
                if not content_found:
                    file.truncate()
                    file.writelines(lines)
                else:
                    content[name] = service['response']
                    add_blueprint(content[name], name)
                    file.truncate()
                    file.write(json.dumps(content, indent=2))
        case 0:
            print('Service not found in this database.')
        case _:
            raise Exception
