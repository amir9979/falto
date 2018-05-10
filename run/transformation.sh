#!/bin/bash

parent=$(dirname $(dirname $(realpath "$0")))
MAX=20
n=0

function process {
	if [ "$n" -ge "$MAX" ]; then
		echo "Skip $1"
		return;
	fi

	echo "Processing $1"
	dot -Tpng "$1.dot" -o "$1.png" > /dev/null
	((n++))
}

# single graphs
for filename in "$parent"/results/*/*/*/*.dot; do
	file=${filename%.*}
	if [ ! -f "$file.png" ]; then
		process $file
	fi
done

# combined graphs
for filename in "$parent"/results/*/*/*.dot; do
	file=${filename%.*}
	if [ ! -f "$file.png" ]; then
		process $file
	fi
done
