#!/usr/bin/python
"""
@author: Discovery Fox
@contact: Flinn@Fuxxbau.de
@name: Charlie's Fourth Angel
@license: Open Source
@version: 1.0 Beta
@date: 3.2.2022
"""
from subprocess import Popen
import psutil
import atexit

import argparse
from rich.console import Console
from rich.panel import Panel

parser = argparse.ArgumentParser(
    description='Starts the Charlie web interface. After that, it can be reached under localhost:5000 by default.'
)

parser.add_argument(
    '-n',
    help='If given automatically starts the ngrok service with the Web Interface.',
    type=str,
    default="False"
)

args = parser.parse_args( )

if args.__dict__.get('n').lower() == 'true':
    from pyngrok import ngrok
    http_tunnel = ngrok.connect(addr=5000)
    console = Console()
    console.print((Panel(f'[cyan]NGROK URL: {http_tunnel.public_url} ', title='[cyan]Charlie\'s Fourth Angel')))
elif args.__dict__.get('n').lower() != "false" and args.__dict__.get('n').lower() != "true":
    parser.error(f'-n must be True or False. You set it to: {args.__dict__.get("n")}')
    parser.print_help( )
    exit(0)

Popen(['python', 'app.py'])


@atexit.register
def goodbye():
    for process in psutil.process_iter( ):
        if process.cmdline( ) == ['python', 'app.py']:
            print('Process found. Terminating it.')
            process.terminate( )
            break
    else:
        print('Process already done!')


while True:
    pass
# todo: ^^
# todo: Make it a try expression and a custom output when you exit the Program
