#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'Please specify a Project'
    exit 0
fi

parent=$(dirname $(dirname $(realpath "$0")))
mkdir -p $parent/results/$1/all/

for bug in "$parent"/results/$1/*; do
	number=$(basename $bug)
	if [ "$number" != "all" ]; then
		cp $bug/all.png $parent/results/$1/all/$number.png || echo "Graph not found: $1_$number"
		# count=`ls -1 $bug/cg/*.png | wc -l`
		# if [ $count == 1 ]; then
			# copy the file
		#	cp $bug/cg/*.png $parent/mfl/$1/all/$number.png
		#else
		#	echo "There were $count graphs in $bug"
		#fi
	fi
done
