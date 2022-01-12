import os
from subprocess import (PIPE, Popen)

Popen('cd /home/pi/tabme-printer-py/ && git pull origin master && cd -', stdout=PIPE, shell=True).stdout.read()