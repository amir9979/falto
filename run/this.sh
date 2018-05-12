#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
args=`cat $SCRIPTPATH/.args`
ROOT="$(dirname $SCRIPTPATH)"

$ROOT/lib/d4j.py -p $1 -b $2 -w $ROOT $args ${@:3}
