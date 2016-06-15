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
cmsRun /afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/MetaData/work/030616/testMe/zeeValidationDumper.py maxEvents=-1 campaign=RunIISpring16DR80X-2_0_0-25ns targetLumi=708 processIdMap=/afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/MetaData/work/030616/testMe/config.json dataset=/DYToEE_NNPDF30_13TeV-powheg-pythia8/ferrif-RunIISpring16DR80X-2_0_0-25ns-2_0_0-v0-RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1-ab7f7a5fb9fbc4628a618ccc220a1e9e/USER outputFile=testMe/output_DYToEE_NNPDF30_13TeV-powheg-pythia8_ferrif-RunIISpring16DR80X-2_0_0-25ns-2_0_0-v0-RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1-ab7f7a5fb9fbc4628a618ccc220a1e9e_USER.root nJobs=200 jobId=98
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

