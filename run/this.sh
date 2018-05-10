#!/bin/bash

args=`cat $(dirname $0)/.args`
$(dirname $(dirname "$0"))/lib/d4j.py -p $1 -b $2 -w $(dirname $(dirname $(realpath "$0"))) $args ${@:3}
