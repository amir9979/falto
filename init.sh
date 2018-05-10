#!/bin/bash

error=0
echoerr() { echo "$@" 1>&2; }

if ! [ -x "$(command -v javac)" ]; then
  echoerr "Please install a JDK"
  echo "apt install openjdk-8"
  error=1
fi

if ! [ -x "$(command -v mvn)" ]; then
  echoerr "Please install maven"
  echo "apt install maven"
  error=1
fi

if ! [ -x "$(command -v dot)" ]; then
  echoerr "Please install graphviz"
  echo "apt install graphviz"
  error=1
fi

if ! $(perl -e 'use DBI;'); then
  echoerr "Please install libdbi-perl"
  echo "apt install libdbi-perl"
  error=1
fi

if ! $(python -c 'import causality; import sklearn') ; then
  echoerr "Please install python, pip, gfortran, python-dev, liblapack-dev"
  echoerr "Also install the python modules numpy, causality, sklearn"
  echo "apt install python-pip gfortran python-dev liblapack-dev"
  echo "pip install numpy"
  echo "pip install causality"
  echo "pip install sklearn"
  error=1
fi


if [ "$error" -eq "1" ]; then
   echoerr "Please install all dependencies and run again"
   exit 1;
fi

git submodule update --init --recursive
mvn -f falo/falo/pom.xml package -DskipTests
mvn -f jdcallgraph/jdcallgraph/pom.xml package -DskipTests -Dcheckstyle.skip=true


git clone https://github.com/dkarv/defects4j data/defects4j
cd data/defects4j
./init.sh

echo ""
echo "Change the folder in data/defects4j/framework/projects/defects4j.build.xml now"
