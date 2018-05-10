#!/bin/bash

echo "$@"
$(dirname "$0")/score.sh "$@" | sort -n
