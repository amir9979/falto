#!/bin/bash

error=0
inst=0
if [[ $1 == -install ]]; then
  inst=1
fi

echoerr() { echo "$@" 1>&2; }
aptinstall() {
  if [[ $inst -eq "1" ]]; then
    sudo apt-get install "$@"
  else
    echoerr "Please install $@"
  fi
}

pipinstall() {
  if [[ $inst -eq "1" ]]; then
    pip install "$@"
  else
    echoerr "Please do pip install $@"
  fi
}


apt=1

if ! [ -x "$(command -v javac)" ]; then
  echoerr "Missing a JDK"
  aptinstall "openjdk-8"
  error=1
fi

if ! [ -x "$(command -v mvn)" ]; then
  echoerr "Maven missing"
  aptinstall "maven"
  error=1
fi

if ! [ -x "$(command -v dot)" ]; then
  echoerr "Please install graphviz"
  aptinstall "graphviz"
  error=1
fi

if ! $(perl -e 'use DBI;'); then
  echoerr "Please install libdbi-perl"
  aptinstall "libdbi-perl"
  error=1
fi

if ! $(python -c 'import causality; import sklearn') ; then
  echoerr "Please install python, pip, gfortran, python-dev, liblapack-dev"
  echoerr "Also install the python modules numpy, causality, sklearn"
  aptinstall "python-pip gfortran python-dev liblapack-dev"
  pipinstall "numpy"
  pipinstall "causality"
  pipinstall "sklearn"
  error=1
fi


if [ "$error" -eq "1" ] && [ "$inst" -eq "0" ]; then
   echoerr "Please install all dependencies and run again. Calling this script with -install flag will install everything on systems with apt-get."
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
