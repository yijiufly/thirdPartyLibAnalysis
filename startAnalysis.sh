#!/bin/sh
CLASS_DIR_NEW=$1
CLASS_DIR_OLD=$2
CLASS_PATH=$3

BIN_DIR="$PWD/bin"
GRAPH_DIR="$PWD/graphs"
CURR_DIR=$PWD

SOOT="$PWD/soot/soot-trunk.jar"
#SOOTCLASS="$PWD/soot/sootclasses-trunk.jar"
#POLYGLOT="$PWD/soot/polyglotclasses-1.3.5.jar"
#JASMIN="$PWD/soot/jasminclasses-2.5.0.jar"
JPYTHON="$PWD/soot/jython-standalone-2.7.0.jar"
ANDROID="$PWD/sdk/platforms/default/android-23.jar"
GSON="$PWD/sdk/platforms/default/pdg/gson-2.3.1.jar"
OUTPUT="$PWD/output/$CLASS_DIR_NEW.output"

CLASS_PATH=${CLASS_PATH%/}
CLASS_FULLPATH_NEW="$CLASS_PATH/$CLASS_DIR_NEW"
CLASS_FULLPATH_OLD="$CLASS_PATH/$CLASS_DIR_OLD"

#call this script with 
# ./api-graph.sh $class_dir $CLASS_PATH 
# For example
#./startAnalysis.sh new_lib_dir old_lib_dir ~/yueduan/thirdPartyLibAnalysis/input

#rm -rf $GRAPH_DIR/*
#./sync_bin.sh

cd $BIN_DIR
echo "Generating graphs for $CLASS_DIR_NEW and $CLASS_DIR_OLD  hopefully it's working"
java -Xss8192m -Xmx16384m -cp $SOOT:$ANDROID:$GSON:$JPYTHON:. mySoot.AnalyzerMain $CLASS_DIR_NEW $CLASS_DIR_OLD $CLASS_FULLPATH_NEW $CLASS_FULLPATH_OLD true $BIN_DIR > $OUTPUT #2> error

echo "Start analysis.."
java -Xss8192m -Xmx16384m -cp $SOOT:$ANDROID:$GSON:$JPYTHON:. mySoot.AnalyzerMain $CLASS_DIR_NEW $CLASS_DIR_OLD $CLASS_FULLPATH_NEW $CLASS_FULLPATH_OLD false $BIN_DIR > $OUTPUT #2>error


# use graphviz to convert dot file to pdf figures
idx=0
DOT=.dot
DOT_FILES=$CURR_DIR/output/*$DOT
for filename in $DOT_FILES
do
	dot -Tpdf $filename -o $CURR_DIR/output/$idx.pdf
	idx=$((idx + 1))
done
