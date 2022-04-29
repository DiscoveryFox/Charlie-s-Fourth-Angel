import os
import pip


# noinspection PyUnresolvedReferences
def install(pipname: str= None, gitlink: str=None):
    if gitlink is not None:
        os.system(f'git clone {gitlink}')
    else:
        if hasattr(pip, 'main'):
            pip.main(['install', pipname])
        else:
            pip._internal.main(['install', pipname])