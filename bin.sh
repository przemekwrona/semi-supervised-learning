#!/bin/bash

RESUTLS=""

red=`tput setaf 1`
reset=`tput sgr0`

DATASOURCE_ARFF="./resources/covertype/covettype.arff"
RESULTS_FILE_NAME="resources/covertype/covertype.CL_p.csv"

# TASK_CL="EvaluateInterleavedTestThenTrainSemi -b trees.HoeffdingTree -l (semisupervised.ClusterAndLabelClassifier -c (semisupervised.ClustreamSSL -a Euclidean)) -s (SemiSupervisedStream -s (ArffFileStream -f ${DATASOURCE_ARFF}) -t 0.9) -e WindowClassificationPerformanceEvaluator -i -1 -f 1000 -q 1000 -d /Users/wronap/dump2.csv"
TASK_CL_P="EvaluateInterleavedTestThenTrainSemi -b trees.HoeffdingTree -l (semisupervised.ClusterAndLabelClassifier -c (semisupervised.ClustreamSSL -a Euclidean) -p) -s (SemiSupervisedStream -s (ArffFileStream -f ${DATASOURCE_ARFF}) -t 0.9) -e WindowClassificationPerformanceEvaluator -i -1 -f 1000 -q 1000 -d ${RESULTS_FILE_NAME}"

java -cp moa/lib/moa.jar -javaagent:moa/lib/sizeofag-1.0.4.jar moa.DoTask $TASK_CL_P
