#!/bin/bash

cp -R /home/creds/* /home/blt &
python job_runner.py &
python webui.py
