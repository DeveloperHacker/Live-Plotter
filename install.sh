#!/usr/bin/env bash
python3 setup.py build
sudo python3 setup.py install
sudo rm -r build/
