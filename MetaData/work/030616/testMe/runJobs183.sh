#!/bin/bash

scp -p lxplus014:/afs/cern.ch/user/g/gkole/.globus/x509up_u11906 .
export X509_USER_PROXY=$PWD/x509up_u11906
WD=$PWD
echo
echo
echo
cd /afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8
eval $(scram runtime -sh)
cd $WD
mkdir testMe
echo "ls $X509_USER_PROXY"
ls $X509_USER_PROXY
cmsRun /afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/MetaData/work/030616/testMe/zeeValidationDumper.py maxEvents=-1 campaign=RunIISpring16DR80X-2_0_0-25ns targetLumi=708 processIdMap=/afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/MetaData/work/030616/testMe/config.json dataset=/DoubleEG/ferrif-RunIISpring16DR80X-2_0_0-25ns-2_0_0-v0-Run2016B-PromptReco-v1-634d2b8230861d3e22d915e30c562c87/USER outputFile=testMe/output_DoubleEG_ferrif-RunIISpring16DR80X-2_0_0-25ns-2_0_0-v0-Run2016B-PromptReco-v1-634d2b8230861d3e22d915e30c562c87_USER.root nJobs=200 jobId=183
retval=$?
if [[ $retval == 0 ]]; then
    errors=""
    for file in $(find -name '*.root' -or -name '*.xml'); do
        cp -pv $file /afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/MetaData/work/030616/testMe
        if [[ $? != 0 ]]; then
            errors="$errors $file($?)"
        fi
    done
    if [[ -n "$errors" ]]; then
       echo "Errors while staging files"
       echo "$errors"
       exit -2
    fi
fi

exit $retval

