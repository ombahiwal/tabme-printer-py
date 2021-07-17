sudo apt-get -y update
sudo apt-get install -y git python3 pip3
git clone https://github.com/OkkarMin/HOP-H58-RaspberryPi-Driver
cd HOP-H58-RaspberryPi-Driver
chmod +x ./install_H58_driver.sh
./install_H58_driver.sh
cd ../
git clone https://github.com/LukePrior/Raspberry-Pi-Thermal-Printer
cd Raspberry-Pi-Thermal-Printer
sudo chmod +x ./installer.sh
sudo ./installer.sh
cd ../
sudo apt-get install paps
pip3 install pyowm tweepy requests
mkdir tabme-print
cd tabme-print
git init
git remote add origin https://github.com/ombahiwal/tabme-printer-py
git pull origin master
pip3 install textwrap argparse tabulate json requests
python3 tabme-queue-print.py
