#!/bin/sh

read LINE

SCRIPT_DIR=$(cd $(dirname $0); pwd)

echo $LINE | python3 "${SCRIPT_DIR}/swallow.py"
