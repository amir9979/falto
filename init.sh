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
    sudo pip install "$@"
  else
    echoerr "Please do pip install $@"
  fi
}


apt=1

if ! [ -x "$(command -v javac)" ]; then
  echoerr "Missing a JDK"
  aptinstall "openjdk-8-jdk"
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
  aptinstall "python-dev"
  aptinstall "python-pip"
  aptinstall "gfortran"
  aptinstall "liblapack-dev"
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


# Prepare defects4j
# enable debug mode
sed -i "s@our $DEBUG = 0;@our $DEBUG = 1;@" defects4j/framework/core/Constants.pm

# add jdcallgraph as instrumentation
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
match='<junit printsummary="yes" haltonfailure="no" haltonerror="no" fork="no" showOutput="true">'
insert='<junit printsummary="yes" haltonfailure="no" haltonerror="no" fork="yes" forkmode="once" showOutput="true">\n            <jvmarg value="-javaagent:'$SCRIPTPATH'/jdcallgraph/jdcallgraph/target/jdcallgraph-0.1-agent.jar='$SCRIPTPATH'/jdcallgraph/examples/falo.ini" />'
file='defects4j/framework/projects/defects4j.build.xml'
sed -i "s@$match@$insert@" $file


cd defects4j
./init.sh
cd ..
