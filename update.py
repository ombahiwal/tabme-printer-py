import os
from subprocess import (PIPE, Popen)
# update test
Popen('sudo cd /home/pi/tabme-printer-py/ && sudo git pull origin master && sudo cd -', stdout=PIPE, shell=True).stdout.read()