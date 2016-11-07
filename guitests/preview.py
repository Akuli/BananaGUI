import subprocess
import sys


args = [sys.executable, '-m', 'bananagui.iniloader', 'guitests/preview.ini']
sys.exit(subprocess.call(args))
