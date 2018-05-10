#!/bin/bash

if (( $# < 1 )); then
	echo "Usage: all.sh <Proj>"
	exit 1
fi

max=0

case $1 in
Lang)
  max=65
  ;;
Math)
  max=106
  ;;
Closure)
  max=133
  ;;
Mockito)
  max=33
  ;;
Time)
  max=27
  ;;
Chart)
  max=26
  ;;
*)
  echo "Unknown project: $1"
  exit 1
  ;;
esac

$(dirname "$0")/upto.sh $1 $max
