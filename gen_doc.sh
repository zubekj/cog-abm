#!/bin/bash
PROJECT='src'

export PYTHONPATH=`pwd`
export PYTHONPATH=$PYTHONPATH:$PYTHONPATH/$PROJECT
echo $PYTHONPATH

cd docs

# generate apidoc (automatically for each module)
SPHINX_APIDOC="sphinx-apidoc"

rm -rf source/api_auto
for prog in 'cog_abm' 'presenter' 'steels'; do
    export SOURCE_PATH=`pwd`/../$PROJECT/$prog
    $SPHINX_APIDOC -o source/api_auto_$prog $SOURCE_PATH
done;
make html

