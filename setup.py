import os
from shlex import quote as shlex_quote
import gitpi

# get path of the current directory
cwd = os.getcwd( )
print(cwd)


def customize_app():
    # open the app.cfg file and set ServicePath to cwd + /Services.json
    with open(cwd + '/app.cfg', 'r') as f:
        lines = f.readlines( )
        for i, line in enumerate(lines):
            if 'ServicesPath' in line:
                lines[i] = 'ServicePath = ' + shlex_quote(cwd + '/Services.json') + '\r\n'

    # write the new app.cfg file
    with open(cwd + '/app.cfg', 'w') as f:
        f.writelines(lines)


# clone a repository to the current directory from github
def clone_repo():
    # clone the repo
    os.system('git clone https://github.com/DiscoveryFox/Charlie-s-Fourth-Angel.git')
    # change to the cloned directory
    os.chdir(cwd + '/Charlie-s-Fourth-Angel')
