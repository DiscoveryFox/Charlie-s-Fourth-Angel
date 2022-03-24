import os
import pip


def install(pipname=None, gitlink=None):
    if pipname is None:
        os.system(f'git clone {gitlink}')
    else:
        if hasattr(pip, 'main'):
            pip.main(['install', pipname])
        else:
            pip._internal.main(['install', pipname])
