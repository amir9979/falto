#!/bin/bash

if (( $# < 2 )); then
	echo "Usage: these.sh <Proj> <Bug1> [<BugN>...]"
	exit 1
fi

parent=$(realpath "$0" | xargs dirname | xargs dirname)
for i in ${@:2}; do
	folder="$parent/results/$1/$i"
#	if [ -f "$folder/all.dot" ]; then
#		printf "\nSkip $i because $folder/all.dot already exists.\n"
#		continue
#	fi
        rm -r $parent/result/* || true
        mkdir -p $parent/result/
        cp $folder/result_* $parent/result/
        cp $folder/score_* $parent/result/

	$(dirname "$0")/this.sh $1 $i || { echo "Skip saving results"; continue; }

	# save the results
	mkdir -p "$folder/"
        cp -r $parent/result/* $folder/
	$(dirname "$0")/transformation.sh || true
done

$(dirname "$0")/collector.sh $1
