from subprocess import call, PIPE
import os

PORT = 12345

cmd = "python3.7 " + os.path.join(os.getcwd(), "http_server/myserver.py") + " " + str(PORT)

call(cmd, shell=True)