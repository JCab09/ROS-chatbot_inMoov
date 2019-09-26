#! /bin/sh

clear

export PYTHONPATH=../../src:$PYTHONPATH
#export PYTHONPATH=../../../program-y/src:$PYTHONPATH

python3 -m henry.clients.events.rosnode.client --config ../../config/xnix/config.ros.yaml --cformat yaml --logging ../../config/xnix/logging.yaml
