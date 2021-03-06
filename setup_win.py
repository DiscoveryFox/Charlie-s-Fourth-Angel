import os

# get path of the current directory
import sys

cwd = os.getcwd( )


def customize_app():
    # open the app.cfg file and set ServicePath to cwd + /Services.json
    with open(cwd + '/app.cfg', 'r') as f:
        lines = f.readlines( )
        for i, line in enumerate(lines):
            if 'ServicesPath' in line:
                lines[i] = 'ServicesPath = ' + cwd + '/Services.json' + '\r\n'

    # write the new app.cfg file
    with open(cwd + '/app.cfg', 'w') as f:
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
        os.system(f'chmod +x {file}')


# install the requirements through pip
def install_requirements():
    os.system('pip install -r requirements.txt')


if __name__ == '__main__':
    # clone the repo
    clone_repo( )
    # customize the app.cfg file
    customize_app( )
    # make the executables
    # make_executables( )
    # install the requirements
    install_requirements( )
    sys.exit(0)
