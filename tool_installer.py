import os
import json
import time
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


def add_blueprint(service_dir: str, name: str) -> str:
    # noinspection PyTypeChecker
    blueprint_content = requests.get(service_dir['path_to_blueprint']).text
    # create a new file with the name of the service + _blueprint.py and write the
    # blueprint_content in it

    with open(f'blueprints/{name}_blueprint.py', 'w') as file:
        file.write(blueprint_content)

    # insert the blueprint in the app.py file
    with open('app.py', 'r') as file:
        lines = file.readlines()
    for x in range(3):
        del lines[-1]
    ###lines.append(f'from blueprints.{name}_blueprint import {name}_blueprint\n')
    ###lines.append(f'app.register_blueprint({name}_blueprint, url_prefix="/{name}")\n')
    ###lines.append(f'if __name__ == "__main__":\n')
    ###lines.append(f'    app.run(host="0.0.0.0", debug=True)\n')
    ###with open('app.py', 'w') as file:
    ###    file.writelines(lines)

    return "blueprint"


# todo: add support to get git project name from ssh connection

def git_project_name(link: str) -> str:
    return link.split('/')[-1].split('.')[0].split('_')[-1]


def download(path, binary=False) -> None:
    if binary:
        with open(f'{git_project_name(path)}_installer.py', "wb") as file:
            file.write(requests.get(path).content)
    else:
        with open(f'{git_project_name(path)}_installer.py', "w") as file:
            file.write(requests.get(path).text)


# todo: add support for multiple os in the installation file maybe with a check locally or maybe
#  the installer just recognize it. Also add python path to app.cfg or atleast prefix or smth
def install(name):
    service = get_service(name)
    match service['success']:
        case 1:
            with open(config['PATHS']['ServicesPath'], "r") as file:
                filecontent = json.loads(file.read())
                if name in filecontent:
                    content = filecontent
                    # pprint(content)
                    download(content[name]['path_to_installer'])
                    # check if file is downloaded
                    while not os.path.isfile(f"{git_project_name(content[name]['path_to_installer'])}_installer.py"):
                        time.sleep(0.3)
                        print('waiting for file to be downloaded')
                    os.system(f'python3.10 {name}_installer.py')
                    content[name]['installed'] = True
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
                    # add_blueprint(content[name], name)
                    file.truncate()
                    file.write(json.dumps(content, indent=2))

        case 0:
            print('Service not found in this database.')
        case _:
            raise Exception


def check_if_service_installed(project_to_open):
    with open(config['PATHS']['ServicesPath'], "r") as file:
        filecontent = json.loads(file.read())
        try:
            if filecontent[project_to_open]['installed'] is not False:
                return True
            else:
                return False
        except KeyError:
            print('Service not found in this database.')
            return False


