#!/usr/bin/env python
import os, sys


#----------------------------------------------------------------------

# assert False, "change this"
configTemplate = os.path.expandvars("$CMSSW_BASE/src/flashgg/Taggers/test/simple_Tag_test.py")

# assert False, "change this"
outputDir = "root://eoscms.cern.ch//store/user/gkole/Hgg/VH/TEST_23Sept/"

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------
from optparse import OptionParser
parser = OptionParser("""

  usage: %prog [options] jobNumber filename

"""
)

### parser.add_option("--mass",
###                   dest="mass",
###                   default = 125,
###                   type=float,
###                   help="Higgs mass to process",
###                   metavar="mh")
### 
### parser.add_option("--proc",
###                   default = "ggh",
###                   type="choice",
###                   choices = [ "ggh", "vbf" ],
###                   metavar="proc")

(options, ARGV) = parser.parse_args()

assert len(ARGV) == 2

jobNumber = int(ARGV.pop(0))
inputFile = ARGV.pop(0)

#----------------------------------------


# create a temporary file with the modified cmsRun configuration

import tempfile

fout = tempfile.NamedTemporaryFile(suffix = ".py", delete = False)

fout.write(open(configTemplate).read())

# print >> fout, "process.maxEvents.input = cms.untracked.int32(%d)" % numEvents

# input file
print >> fout, "process.source.fileNames = cms.untracked.vstring([ '%s' ])" % inputFile

# output file
intermediateOutputDir = tempfile.mkdtemp()

intermediateOutputFname = os.path.join(intermediateOutputDir, "output-%04d.root" % jobNumber) # defined in DEBUG gkole
intermediateLogFname    = os.path.join(intermediateOutputDir, "output-%04d.log" % jobNumber)

# DEBUG gkole


print "inputFile", inputFile
dspartstmp = inputFile.strip('/').split('/')
if len(dspartstmp) > 1:
    secondary = dspartstmp[1]
else:
    secondary = None

# primary = '/' + dspartstmp[0]

print "9th term", dspartstmp[8]

# print "primary", primary

intermediateOutputFname = os.path.join(intermediateOutputDir, "output-"+dspartstmp[8]+"-%04d.root" % jobNumber) 
# print "intermediateOutputFnameCheck", intermediateOutputFnameCheck
intermediateLogFname    = os.path.join(intermediateOutputDir, "output-"+dspartstmp[8]+"-%04d.log" % jobNumber)
print "intermediateOutputFname", intermediateOutputFname
print "intermediateLogFname", intermediateLogFname
# END DEBUG gkole

print >> fout, "process.out.fileName = '%s'" % intermediateOutputFname

# DEBUG
print >> fout, "process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )"


# DEBUG
# print >> fout, "process.AODSIMoutput.outputCommands = cms.untracked.vstring([ 'keep *'])"


fout.flush()

cmd = ' '.join([
        "cmsRun",
        fout.name,
        " > %s 2>&1" % intermediateLogFname,


        # this does not properly reflect the cmsRun exit status later on ?!
        # (on the other hand, we can monitor progress with bpeek -f)
        # 2>&1 | tee %s" % intermediateLogFname
        ])
                

print "running",cmd
res = os.system(cmd)
assert res == 0, "cmsRun failed"

# copy to final output directory

for fname in [ intermediateOutputFname, intermediateLogFname]:
    
    dest = os.path.join(outputDir, os.path.basename(fname))

    res = os.system("xrdcp -f " + fname + " " + dest)

    


