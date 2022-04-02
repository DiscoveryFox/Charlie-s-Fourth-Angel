# freeze setup.py to a .exe using pyinstaller
# I only want one .exe file

import os

os.system('pyinstaller --onefile setup_win.py')