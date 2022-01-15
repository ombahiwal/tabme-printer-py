sudo apt-get -y update
sudo apt-get install -y git python3 vim cups
# sudo apt-get install -y cups ia32-libs gcc-multilib
pip3 install argparse tabulate requests textwrap3 python-dotenv
# mkdir tabme-print
# cd tabme-print
# git init
# git remote add origin https://github.com/ombahiwal/tabme-printer-py
# git pull origin master
git clone https://github.com/ombahiwal/tabme-printer-py
cd /home/pi/tabme-printer-py
git checkout master

# Run on Startup
echo 'sudo python /home/pi/tabme-printer-py/update.py &' >> /etc/rc.local
echo 'sudo python /home/pi/tabme-printer-py/tabme-auto-print.py &' >> /etc/rc.local
echo 'sudo python /home/pi/tabme-printer-py/tabme-queue-print.py &' >> /etc/rc.local
# cd ../
# git clone https://github.com/OkkarMin/HOP-H58-RaspberryPi-Driver
# cd HOP-H58-RaspberryPi-Driver
# chmod +x ./install_H58_driver.sh
# ./install_H58_driver.sh
# check update 1
cd ../
git clone https://github.com/LukePrior/Raspberry-Pi-Thermal-Printer
cd Raspberry-Pi-Thermal-Printer
sudo chmod +x ./installer.sh
sudo ./installer.sh