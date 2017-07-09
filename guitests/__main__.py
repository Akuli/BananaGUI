import os
import subprocess
import sys


here = os.path.dirname(os.path.abspath(__file__))
listing = os.listdir(here)
listing.sort()

for filename in listing:
    name, extension = os.path.splitext(filename)
    if extension != '.py' or name.startswith('_'):
        continue

    command = [sys.executable, '-m', 'guitests.%s' % name] + sys.argv[1:]
    print((" %s " % filename).center(70, '*'))

    gonna_break = False
    with subprocess.Popen(command, stderr=subprocess.PIPE) as process:
        for line in process.stderr:
            if line.startswith(b'KeyboardInterrupt'):
                gonna_break = True
            sys.stderr.buffer.write(line)
            sys.stderr.buffer.flush()

    if gonna_break:
        break
