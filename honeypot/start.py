from subprocess import call
import os

PORT = 80

cmd = "python3.7 " + os.path.join(os.getcwd(), "http_server/myserver.py") + " " + str(PORT)

call(cmd, shell=True)