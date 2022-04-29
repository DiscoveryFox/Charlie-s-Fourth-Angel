#!/usr/bin/python
import os
from shlex import quote as shlex_quote

# get path of the current directory
cwd = os.getcwd()


# TODO: change '/home/kali/Documents/' to a variable which works atleast across linux

def customize_app():
    # open the app.cfg file and set ServicePath to cwd + /Services.json
    if os.getcwd().split("/")[-1] == "Charlie-s-Fourth-Angel":
        # In working directory
        with open(cwd + '/app.cfg', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if 'ServicesPath' in line:
                    lines[i] = 'ServicesPath = ' + shlex_quote(cwd + '/Services.json') + '\r\n'

        with open(cwd + '/app.cfg', 'w') as f:
            f.writelines(lines)

    else:
        with open('/home/kali/Documents/' + 'Charlie-s-Fourth-Angel' + '/app.cfg', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if 'ServicesPath' in line:
                    lines[i] = 'ServicesPath = ' + shlex_quote(
                        '/home/kali/Documents/' + "/Charlie-s-Fourth-Angel/" +
                        '/Services.json') + '\r\n'

        with open('/home/kali/Documents/'+ 'Charlie-s-Fourth-Angel' + '/app.cfg', 'w') as f:
            f.writelines(lines)




# clone a repository to the current directory from github
def clone_repo():
    # clone the repo
    os.system('git clone https://github.com/DiscoveryFox/Charlie-s-Fourth-Angel.git')
    # change to the cloned directory
    os.chdir(cwd + '/Charlie-s-Fourth-Angel')


def make_executables():
    to_make = ['app.py', 'get_ip.sh', 'startcam.sh', 'start.py', 'tool_installer.py']
    for file in to_make:
        os.system(f'chmod +x {cwd + "/Charlie-s-Fourth-Angel/" + file}')


# install the requirements through pip


if __name__ == '__main__':
    # clone the repo
    clone_repo()
    # customize the app.cfg file
    customize_app()
    # make the executables
    make_executables()
