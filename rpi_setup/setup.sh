#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip -=y
python3 -m venv env
source env/bin/activate

