#!/bin/bash

export X509_USER_PROXY=/afs/cern.ch/user/g/gkole/.globus/x509up_u11906
WD=$PWD
echo
echo
echo
cd /afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8
eval $(scram runtime -sh)
cd $WD
mkdir flatTree_no_corr
echo "ls $X509_USER_PROXY"
ls $X509_USER_PROXY
cmsRun /afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/Validation/test/ZeeValidation_wocorr/flatTree_no_corr/zeeValidationDumper.py maxEvents=-1 campaign=RunIISpring16DR80X-2_0_0-25ns targetLumi=708 processIdMap=/afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/Validation/test/ZeeValidation_wocorr/flatTree_no_corr/config.json dataset=/DoubleEG/ferrif-RunIISpring16DR80X-2_0_0-25ns-2_0_0-v0-Run2016B-PromptReco-v2-634d2b8230861d3e22d915e30c562c87/USER outputFile=flatTree_no_corr/output_DoubleEG_ferrif-RunIISpring16DR80X-2_0_0-25ns-2_0_0-v0-Run2016B-PromptReco-v2-634d2b8230861d3e22d915e30c562c87_USER.root nJobs=100 jobId=1
retval=$?
if [[ $retval == 0 ]]; then
    errors=""
    for file in $(find -name '*.root' -or -name '*.xml'); do
        cp -pv $file /afs/cern.ch/work/g/gkole/Hgg/CMSSW_8_0_8/src/flashgg/Validation/test/ZeeValidation_wocorr/flatTree_no_corr
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

