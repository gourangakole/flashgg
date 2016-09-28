#!/usr/bin/env python

import os, sys

queue = "1nh"

campaign = "RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2_Workspaces"


datasets = [
    '/VHToGG_M127_13TeV_amcatnloFXFX_madspin_pythia8/ferrif-RunIISpring16DR80X-2_2_0-25ns_ICHEP16_MiniAODv2-2_2_0-v0-RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1-9d6acec11aa5264fedffe5a321afb429/USER',

    ]

#----------------------------------------------------------------------

from pprint import pprint

def getFiles(campaign, dataset):
    from flashgg.MetaData.samples_utils import SamplesManager

    samplesManager = SamplesManager("$CMSSW_BASE/src/flashgg/MetaData/data/%s/datasets.json" % campaign
                                    )
    dsparts = dataset.strip('/').split('/')
    if len(dsparts) > 1:
        secondary = dsparts[1]
    else:
        secondary = None

    primary = '/' + dsparts[0]


    x = samplesManager.getDatasetMetaData(-1,
                                             primary,
                                             secondary
                                             )

    fullDsName, xsect, numEvents, files, maxEvents = samplesManager.getDatasetMetaData(-1,
                                             primary,
                                             secondary
                                             )



    return files

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------

# get the list of files for each dataset

ARGV = sys.argv[1:]

if ARGV:
    selectedJobs = [ int(x) for x in ARGV ]
else:
    selectedJobs = None

allFiles = []

for dataset in datasets:
    allFiles.extend(getFiles(campaign, dataset))


uid = os.getuid()
for jobNumber, inputFile in enumerate(allFiles):

    if selectedJobs == None or jobNumber in selectedJobs:


        fout = os.popen(" ".join([
                    "bsub",
                    "-q " + queue,
                    " -J " + "%05d" % jobNumber,

                    # we may have to copy the 'grid proxy file' to the remote host
                    # "-f '/tmp/x509up_u%d > /tmp/x509up_u%d'" % (uid, uid) # the 'grid proxy file'
                    ]),
                 "w")

        print >> fout,"#!/bin/sh"

        # avoid home directory be flooded with cores
        print >> fout,"ulimit -c 0"

        print >> fout,"source /afs/cern.ch/group/zh/group_env.sh"
        print >> fout,"cd " + os.environ['CMSSW_BASE']
        print >> fout,"eval `scram runtime -sh`"
        print >> fout,"cd " + os.getcwd()

        print >> fout,"./runJob.py %d %s" % (jobNumber, inputFile)

        print >> fout,"echo ----------"
        print >> fout,"pwd"

        # start submission
        fout.close()

    # DEBUG
    # break
    


