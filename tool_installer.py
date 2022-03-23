import os


def install(gitlink: str) -> None:
    os.system(f'git clone {gitlink}')
