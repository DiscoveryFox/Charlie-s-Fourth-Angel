#!/usr/bin/python
"""
@author: Discovery Fox
@contact: Flinn@Fuxxbau.de
@name: Charlie's Fourth Angel
@license: Open Source
@version: 1.0 Beta
@date: 3.2.2022
"""
import os
import time
from subprocess import Popen
import psutil
import atexit

import argparse
from rich.console import Console
from rich.panel import Panel

import setup

parser = argparse.ArgumentParser(
    description='Starts the Charlie web interface. After that, it can be reached under localhost:5000 by default.'
)

parser.add_argument(
    '-n',
    help='If given automatically starts the ngrok service with the Web Interface.',
    type=str,
    default="False"
)

parser.add_argument(
    '-c',
    help='If given the script will cleanup the settings and the folder structure at start. '
         'Default is False.',
    type=str,
    default="False"
)

parser.add_argument(
    '-wd',
    help='Here you can specify a special working directory. Default is the current directory.',
    type=str,
    default="."
)

args = parser.parse_args( )

if args.__dict__.get('n').lower() == 'true':
    from pyngrok import ngrok
    http_tunnel = ngrok.connect(addr=5000)
    console = Console()
    console.print((Panel(f'[cyan]NGROK URL: [bold]{http_tunnel.public_url} ', title='[cyan]Charlie\'s Fourth Angel')))
elif args.__dict__.get('n').lower() != "false" and args.__dict__.get('n').lower() != "true":
    parser.error(f'-n must be True or False. You set it to: {args.__dict__.get("n")}')
    parser.print_help( )
    exit(-1)

if args.__dict__.get('c').lower() == 'true':
    setup.customize_app()
elif args.__dict__.get('c').lower() != "false" and args.__dict__.get('c').lower() != "true":
    parser.error(f'-c must be True or False. You set it to: {args.__dict__.get("c")}')
    parser.print_help( )
    exit(-1)

if args.__dict__.get('wd') != ".":
    wd = args.__dict__.get('wd')
    if not args.__dict__.get('wd').endswith('/'): wd += '/'
    os.chdir(wd)
elif args.__dict__.get('wd') == ".":
    os.chdir(os.getcwd())

Popen(['python3.10', 'app.py'])


@atexit.register
def goodbye():
    for process in psutil.process_iter( ):
        if process.cmdline( ) == ['python3.10', 'app.py']:
            print('Process found. Terminating it.')
            process.terminate( )
            break
    else:
        print('Process already done!')


while True:
    time.sleep(0.00001)
    pass
# todo: ^^
# todo: Make it a try expression and a custom output when you exit the Program
