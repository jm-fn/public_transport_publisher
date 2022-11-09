# My Public Transport Publisher

This is a personal project that builds a little dashboard with the earliest public transport connections using Raspberry Pi and a touch LCD. The connections are scraped from idos.cz website for public transport in Prague. We hardcoded three destinations that are nearest to the point of interest (Anděl). We use Kivy for GUI. The project served mostly as a learning experience for using Kivy and Beautiful Soup. 

## Hardware
We use [Raspberry Pi 4B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) and [Waveshare 3.2 inch Touch display](https://www.waveshare.com/3.2inch-rpi-lcd-c.htm) The project will probably work with other touch displays with minor modifications.

## Installation

### On Raspberry Pi
We use Ansible to install the project (PTP) on RPi. ([Here](https://docs.ansible.com/ansible/latest/getting_started/index.html) is some quick guide.) The configuration has been tested with Raspbian Bullseye. 

First create inventory directory with Ansible hosts file:
```yaml
# inventory/hosts file
all:
    hosts:
      host:
        ansible_host: <Your pi IP address here.>
        ansible_user: <Your pi user here.>
```

Then either install Waveshare LCD drivers manually following [this wiki](https://www.waveshare.com/wiki/3.2inch_RPi_LCD_(C) ) or run the install_drivers.yaml playlist from the root directory:
```bash
ansible-playbook -i path/to/inventory/hosts ansible/install_drivers.yaml
```
This downloads the display drivers on RPi, compiles them and runs them. (**Note** that you may need to add `--ask-become-pass` to enable priviledge escalation on RPi if you don't have NOPASSWD in your sudoers file.)


Then run init.yaml playbook to install the project on RPi:
```bash
ansible-playbook -i ansible/inventory/hosts ansible/init.yaml
```
This clones the project git repo and configures the system so that the pi user is automatically logged in after startup and the Public Transport Publisher (PTP) runs on startup. (Note that this is kinda dangerous and should not be used where there may be some malicious people with access to the RPi.)

After running the playbook, restart the RPi and a while after startup PTP should be running.

### On PC
Run:
```bash
git clone https://github.com/jm-fn/public_transport_publisher.git ptp
cd ptp/gui
python -m venv .venv
. .venv/bin/activate
pip3 install bs4 kivy
python3 main.py
```

