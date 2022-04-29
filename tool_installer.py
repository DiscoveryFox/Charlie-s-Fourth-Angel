import os
import json
import pip
import configparser
from pprint import pprint

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
    print(name)
    services = json.loads(requests.get(config['PATHS']['OnlineServices']).text)

    if name in services:
        return {'success': 1,
                'response': services[name]
                }
    else:
        return {'success': 0,
                'response': None
                }


def install(name):
    service = get_service(name)
    match service['success']:
        case 1:
            with open(config['PATHS']['ServicesPath'], "r") as file:
                print(file.read())
                if name in json.loads(file.read()):
                    print(file.read())
                    content = json.loads(file.read())
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
                    file.truncate()
                    file.write(json.dumps(content))
        case 0:
            print('Service not found in this database.')
        case _:
            raise Exception


