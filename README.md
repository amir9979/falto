# falto

FAult Localization TOols

A bunch of tools for fault localization. This is the main repo, it contains the scoring pipeline and scripts to run experiments on bugs from Defects4J.

https://github.com/dkarv/lang-26-data contains the files our tools computed for Lang-26.

## Setup

1. Clone this repository
2. Run `./init.sh` to check the dependencies and initalize everything. `./init.sh -install` installs all dependencies on a debian based linux system. Tested on Ubuntu 14.04.

## How-to

To run a test from Defects4J, generate the dependency graph and run a bunch of fault localization techniques, use the following commands. We support the four projects _Chart_, _Closure_, _Lang_ and _Time_.

`run/this.sh <project> <bug id>`: Run a single bug from a single project. Example: `run/this.sh Lang 1`

`run/these.sh <project> <bug id 1> <bug id 2> <bug id 3> ...`: Run a bunch of bugs from one project. Can be combined with shell expansion: `run/these.sh {10..20}`

`run/upto.sh <project> <bug id>`: Run all bugs, starting with 1 up to the given number.

`run/all.sh <project>`: Run all bugs from the given project. `run/all.sh Lang`

