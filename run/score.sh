#!/bin/bash

sum=0
count=0

top10=0
top5=0
difficult=0

parent=$(dirname $(dirname $(realpath "$0")))

# single graphs
for filename in "$parent"/results/$1/*/score_$2; do
	s=`cat $filename`
	id=`echo "$filename" | awk -F/ '{print $(NF-1)}'`
	echo -e "$id\t$s"
	sum=$(python -c "print $sum + $s")
        ((count++))
	if (( $(echo "$s <= 5.0" | bc -l) )); then ((top5++)); fi
	if (( $(echo "$s <= 10.0" | bc -l) )); then ((top10++)); fi
	if (( $(echo "$s >= 500.0" | bc -l) )); then ((difficult++)); fi
done

avg=`awk "BEGIN { print ($sum / $count) }"`

echo -e "avg\t$avg" 1>&2

echo -e "sum\t$sum" 1>&2
echo -e "count\t$count" 1>&2

echo "Top 10: $top10" 1>&2
echo "Top 5: $top5" 1>&2
echo "Very difficult (>=500): $difficult" 1>&2
