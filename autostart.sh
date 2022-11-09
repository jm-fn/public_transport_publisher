#!/bin/bash

cd ~/ptp/gui
python3 -m venv venv
. venv/bin/activate
pip3 install kivy bs4
python main.py
