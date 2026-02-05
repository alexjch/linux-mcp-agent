#!/bin/bash
set -e

dnf install git python3 python3-pip make -y
python -m venv .venv
echo 'source /workspace/.venv/bin/activate' >> ~/.bashrc
.venv/bin/pip3 install --upgrade pip
.venv/bin/pip3 install -r requirements.txt
.venv/bin/pip3 install linux-mcp-server