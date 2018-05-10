#!/bin/bash

nums=$(seq -s ' ' 1 $2)
dir=$(dirname "$0")
$dir/these.sh $1 $nums
