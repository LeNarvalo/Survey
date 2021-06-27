import os, time
from subprocess import *

while True:
    ct = time.time()
    try:
        if time.time()-ct>5:
            ct = time.time()
        file = open(os.path.expanduser(r'~\survey\survey\Stochastic Prevent WMI.exe'), "r+")
        file.close()
        Popen(r'start %userprofile%\survey\survey\"Stochastic Prevent WMI.exe"', stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
    except:
        pass
    time.sleep(0.1)
