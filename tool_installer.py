import os
import pip

def install(pipname: str= None, gitlink: str=None):
    if gitlink != None:
        os.system(f'git clone {gitlink}')
    else:
        if hasattr(pip, 'main'):
            pip.main(['install', pipname])
        else:
            pip._internal.main(['install', pipname])