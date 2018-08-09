#!/usr/bin/env cmsRun

import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import FWCore.ParameterSet.VarParsing as VarParsing
from flashgg.Systematics.SystematicDumperDefaultVariables import minimalVariables,minimalHistograms,minimalNonSignalVariables,systematicVariables
from flashgg.Systematics.SystematicDumperDefaultVariables import minimalVariablesHTXS,systematicVariablesHTXS
from flashgg.Systematics.SystematicDumperDefaultVariables import defaultVariables
import os

process = cms.Process("FLASHggTHQ")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
if os.environ["CMSSW_VERSION"].count("CMSSW_9_4_6"):
    process.GlobalTag.globaltag = '94X_mc2017_realistic_v12'
elif os.environ["CMSSW_VERSION"].count("CMSSW_7_4"):
    process.GlobalTag.globaltag = '74X_mcRun2_asymptotic_v4' 
elif os.environ["CMSSW_VERSION"].count("CMSSW_8_0"):
    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2'
else:
    raise Exception,"Could not find a sensible CMSSW_VERSION for default globaltag"

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 100 )



from flashgg.Systematics.SystematicsCustomize import *
jetSystematicsInputTags = createStandardSystematicsProducers(process)
process.load("flashgg.Taggers.flashggTagSequence_cfi")
modifyTagSequenceForSystematics(process,jetSystematicsInputTags)

systlabels = [""]
phosystlabels = []
metsystlabels = []
jetsystlabels = []
elesystlabels = []
musystlabels = []

from flashgg.MetaData.JobConfig import customize
customize.options.register('thqTagsOnly',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'thqTagsOnly'
                           )
customize.options.register('tthTagsOnly',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'tthTagsOnly'
                           )
customize.options.register('doHTXS',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doHTXS'
                           )
customize.options.register('doMuFilter',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doMuFilter'
                           )
customize.options.register('doFiducial',
                           False,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doFiducial'
                           )
customize.options.register('acceptance',
                           'NONE',
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.string,
                           'acceptance'
                           )
customize.options.register('doSystematics',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doSystematics'
                           )
customize.options.register('doPdfWeights',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'doPdfWeights'
                           )
customize.options.register('dumpTrees',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'dumpTrees'
                           )
customize.options.register('dumpWorkspace',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'dumpWorkspace'
                           )


print "Printing defaults"
print 'doFiducial '+str(customize.doFiducial)
print 'acceptance '+str(customize.acceptance)
print 'tthTagsOnly '+str(customize.tthTagsOnly)
# import flashgg customization to check if we have signal or background
from flashgg.MetaData.JobConfig import customize
customize.parse()
print "Printing options"
print 'doFiducial '+str(customize.doFiducial)
print 'acceptance '+str(customize.acceptance)
print 'tthTagsOnly '+str(customize.tthTagsOnly)
print 'doMuFilter '+str(customize.doMuFilter)

if customize.doFiducial:
    import flashgg.Systematics.fiducialCrossSectionsCustomize as fc
    fc.leadCut = 1./3.
    fc.subLeadCut = 1./4.
    fc.isoCut = 10.
    fc.etaCut = 2.5
    matchCut = "leadingPhoton.hasMatchedGenPhoton() && subLeadingPhoton.hasMatchedGenPhoton()"
    phoIDcut = '(leadingView().phoIdMvaWrtChosenVtx() >0.320 && subLeadingView().phoIdMvaWrtChosenVtx() >0.320)'
    accCut   = fc.getAccRecoCut()
    
    print process.flashggPreselectedDiPhotons.cut

    if customize.acceptance == 'IN':
        process.flashggPreselectedDiPhotons.cut = cms.string(str(process.flashggPreselectedDiPhotons.cut)[12:-2] +' && '+ str(matchCut)+ ' && '+ str(phoIDcut) +' && ' + str(accCut))

    if customize.acceptance == 'OUT':
        process.flashggPreselectedDiPhotons.cut = cms.string(str(process.flashggPreselectedDiPhotons.cut)[12:-2] +' && '+ str(matchCut)+ ' && '+ str(phoIDcut) +' && !' + str(accCut))
        
    if customize.acceptance == 'NONE':
        process.flashggPreselectedDiPhotons.cut = cms.string(str(process.flashggPreselectedDiPhotons.cut)[12:-2] +' && '+ str(phoIDcut))
    print "Here we print the preslection cut"
    print process.flashggPreselectedDiPhotons.cut



print process.flashggTagSequence
if customize.doFiducial:
    from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet,massSearchReplaceAnyInputTag
    process.flashggTagSequence.remove(process.flashggVBFTag)
    process.flashggTagSequence.remove(process.flashggTTHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggTTHHadronicTag)
    #haven't tested VH tags with fiducial cross-section measurement yet
    process.flashggTagSequence.remove(process.flashggVHEtTag)
    process.flashggTagSequence.remove(process.flashggVHLooseTag)
    process.flashggTagSequence.remove(process.flashggVHTightTag)
    process.flashggTagSequence.remove(process.flashggVHMetTag)
    process.flashggTagSequence.remove(process.flashggWHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggZHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggVHLeptonicLooseTag)
    process.flashggTagSequence.remove(process.flashggVHHadronicTag)
    process.flashggTagSequence.replace(process.flashggUntagged, process.flashggSigmaMoMpToMTag)

if customize.tthTagsOnly:
    process.flashggTagSequence.remove(process.flashggVBFTag)
    process.flashggTagSequence.remove(process.flashggVHMetTag)
    process.flashggTagSequence.remove(process.flashggWHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggZHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggVHLeptonicLooseTag)
    process.flashggTagSequence.remove(process.flashggVHHadronicTag)
    process.flashggTagSequence.remove(process.flashggUntagged)
    process.flashggTagSequence.remove(process.flashggVBFMVA)
    process.flashggTagSequence.remove(process.flashggVBFDiPhoDiJetMVA)

if customize.thqTagsOnly:
    process.flashggTagSequence.remove(process.flashggTTHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggTTHHadronicTag)
    process.flashggTagSequence.remove(process.flashggVBFTag)
    process.flashggTagSequence.remove(process.flashggVHMetTag)
    process.flashggTagSequence.remove(process.flashggWHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggZHLeptonicTag)
    process.flashggTagSequence.remove(process.flashggVHLeptonicLooseTag)
    process.flashggTagSequence.remove(process.flashggVHHadronicTag)
    process.flashggTagSequence.remove(process.flashggUntagged)
    process.flashggTagSequence.remove(process.flashggVBFMVA)
    process.flashggTagSequence.remove(process.flashggVBFDiPhoDiJetMVA)

    #if customize.processId.count("thq") or customize.processId.count("thw"):
    process.flashggTHQLeptonicTag.processId = cms.string(str(customize.processId))

print " processId = " , customize.processId
#print " process.flashggTHQLeptonicTag.IsTH = " ,  process.flashggTHQLeptonicTag.IsTH 

print 'here we print the tag sequence after'
print process.flashggTagSequence

if customize.doFiducial:
    print 'we do fiducial and we change tagsorter'
    process.flashggTagSorter.TagPriorityRanges = cms.VPSet(     cms.PSet(TagName = cms.InputTag('flashggSigmaMoMpToMTag')) )

if customize.tthTagsOnly:
    process.flashggTagSorter.TagPriorityRanges = cms.VPSet(     cms.PSet(TagName = cms.InputTag('flashggTTHLeptonicTag')),
        cms.PSet(TagName = cms.InputTag('flashggTTHHadronicTag')) )

if customize.thqTagsOnly:
    process.flashggTagSorter.TagPriorityRanges = cms.VPSet(     cms.PSet(TagName = cms.InputTag('flashggTHQLeptonicTag')) )

print "customize.processId:",customize.processId
# load appropriate scale and smearing bins here
# systematics customization scripts will take care of adjusting flashggDiPhotonSystematics
#process.load("flashgg.Systematics.escales.escale76X_16DecRereco_2015")

# Or use the official tool instead
useEGMTools(process)

# Only run systematics for signal events
if customize.processId.count("h_") or customize.processId.count("vbf_") or customize.processId.count("thq") or customize.processId.count("thw") or customize.processId.count("Acceptance"): # convention: ggh vbf wzh (wh zh) tth thq thw
    print "Signal MC, so adding systematics and dZ"
    if customize.doHTXS:
        variablesToUse = minimalVariablesHTXS
    else:
        variablesToUse = minimalVariables
    if customize.doFiducial:
        variablesToUse.extend(fc.getGenVariables(True))
        variablesToUse.extend(fc.getRecoVariables(True))
        variablesToUse.append("genLeadGenIso := ? diPhoton().leadingPhoton().hasMatchedGenPhoton() ? diPhoton().leadingPhoton().userFloat(\"genIso\") : -99")
        variablesToUse.append("decorrSigmarv := diPhotonMVA().decorrSigmarv")
        variablesToUse.append("leadmva := diPhotonMVA().leadmva")
        variablesToUse.append("subleadmva := diPhotonMVA().subleadmva")

    if customize.doSystematics:
        for direction in ["Up","Down"]:
            phosystlabels.append("MvaShift%s01sigma" % direction)
#            phosystlabels.append("MvaLinearSyst%s01sigma" % direction)
            phosystlabels.append("SigmaEOverEShift%s01sigma" % direction)
            phosystlabels.append("MaterialCentralBarrel%s01sigma" % direction)
            phosystlabels.append("MaterialOuterBarrel%s01sigma" % direction)
            phosystlabels.append("MaterialForward%s01sigma" % direction)
            phosystlabels.append("FNUFEB%s01sigma" % direction)
            phosystlabels.append("FNUFEE%s01sigma" % direction)
            phosystlabels.append("MCScaleGain6EB%s01sigma" % direction)
            phosystlabels.append("MCScaleGain1EB%s01sigma" % direction)
            jetsystlabels.append("JEC%s01sigma" % direction)
            jetsystlabels.append("JER%s01sigma" % direction)
            jetsystlabels.append("PUJIDShift%s01sigma" % direction)
            metsystlabels.append("metJecUncertainty%s01sigma" % direction)
            metsystlabels.append("metJerUncertainty%s01sigma" % direction)
            metsystlabels.append("metPhoUncertainty%s01sigma" % direction)
            metsystlabels.append("metUncUncertainty%s01sigma" % direction)
            variablesToUse.append("UnmatchedPUWeight%s01sigma[1,-999999.,999999.] := weight(\"UnmatchedPUWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("MvaLinearSyst%s01sigma[1,-999999.,999999.] := weight(\"MvaLinearSyst%s01sigma\")" % (direction,direction))
            variablesToUse.append("LooseMvaSF%s01sigma[1,-999999.,999999.] := weight(\"LooseMvaSF%s01sigma\")" % (direction,direction))
            variablesToUse.append("PreselSF%s01sigma[1,-999999.,999999.] := weight(\"PreselSF%s01sigma\")" % (direction,direction))
            variablesToUse.append("electronVetoSF%s01sigma[1,-999999.,999999.] := weight(\"electronVetoSF%s01sigma\")" % (direction,direction))
            variablesToUse.append("TriggerWeight%s01sigma[1,-999999.,999999.] := weight(\"TriggerWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("FracRVWeight%s01sigma[1,-999999.,999999.] := weight(\"FracRVWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("FracRVNvtxWeight%s01sigma[1,-999999.,999999.] := weight(\"FracRVNvtxWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("ElectronWeight%s01sigma[1,-999999.,999999.] := weight(\"ElectronWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("MuonWeight%s01sigma[1,-999999.,999999.] := weight(\"MuonWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("MuonMiniIsoWeight%s01sigma[1,-999999.,999999.] := weight(\"MuonMiniIsoWeight%s01sigma\")" % (direction,direction))
	    variablesToUse.append("JetBTagCutWeight%s01sigma[1,-999999.,999999.] := weight(\"JetBTagCutWeight%s01sigma\")" % (direction,direction))
            variablesToUse.append("JetBTagReshapeWeight%s01sigma[1,-999999.,999999.] := weight(\"JetBTagReshapeWeight%s01sigma\")" % (direction,direction))
            for r9 in ["HighR9","LowR9"]:
                for region in ["EB","EE"]:
                    phosystlabels.append("ShowerShape%s%s%s01sigma"%(r9,region,direction))
#                    phosystlabels.append("MCSmear%s%s%s01sigma" % (r9,region,direction))
                    phosystlabels.append("MCScale%s%s%s01sigma" % (r9,region,direction))
                    for var in ["Rho","Phi"]:
                        phosystlabels.append("MCSmear%s%s%s%s01sigma" % (r9,region,var,direction))
        systlabels += phosystlabels
        systlabels += jetsystlabels
        systlabels += metsystlabels
    customizeSystematicsForSignal(process)
elif customize.processId == "Data":
    print "Data, so turn off all shifts and systematics, with some exceptions"
    variablesToUse = minimalNonSignalVariables
    if customize.doFiducial:
        variablesToUse.extend(fc.getRecoVariables(True))
    customizeSystematicsForData(process)
else:
    print "Background MC, so store mgg and central only"
    variablesToUse = minimalNonSignalVariables
    customizeSystematicsForBackground(process)

print "--- Systematics  with independent collections ---"
print systlabels
print "-------------------------------------------------"
print "--- Variables to be dumped, including systematic weights ---"
print variablesToUse
print "------------------------------------------------------------"




#from flashgg.Taggers.globalVariables_cff import globalVariables
#globalVariables.extraFloats.rho = cms.InputTag("rhoFixedGridAll")

#cloneTagSequenceForEachSystematic(process,systlabels,phosystlabels,jetsystlabels,jetSystematicsInputTags)
cloneTagSequenceForEachSystematic(process,systlabels,phosystlabels,metsystlabels,jetsystlabels,jetSystematicsInputTags)

# Dump an object called NoTag for untagged events in order to track QCD weights
# Will be broken if it's done for non-central values, so turn this on only for the non-syst tag sorter
process.flashggTagSorter.CreateNoTag = True # MUST be after tag sequence cloning

###### Dumper section

from flashgg.MetaData.samples_utils import SamplesManager

process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring(
        #"root://eoscms.cern.ch//eos/cms/store/group/phys_top/gkrintir/flashgg/RunIISummer16-2_4_2-25ns_Moriond17/2_4_2/THQ_ctcvcp_HToGG_M120_13TeV-madgraph-pythia8_TuneCUETP8M1_v2/RunIISummer16-2_4_2-25ns_Moriond17-2_4_2-v0-RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/170504_223935/0000/myMicroAODOutputFile_1.root"
        #"root://eoscms.cern.ch//eos/cms/store/group/phys_top/gkrintir/flashgg/RunIISummer16-2_4_2-25ns_Moriond17/2_4_2/THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16-2_4_2-25ns_Moriond17-2_4_2-v0-RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/170413_104447/0000/myMicroAODOutputFile_1.root"
        #"root://eoscms.cern.ch//eos/cms/store/group/phys_top/gkrintir/flashgg/RunIISummer16-2_4_2-25ns_Moriond17/2_4_2/THW_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16-2_4_2-25ns_Moriond17-2_4_2-v0-RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/170413_155336/0000/myMicroAODOutputFile_10.root"
        #"root://eoscms.cern.ch//eos/cms/store/group/phys_top/gkrintir/flashgg/RunIISummer16-2_4_2-25ns_Moriond17/2_4_2/THQ_HToGG_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16-2_4_2-25ns_Moriond17-2_4_2-v0-RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/170413_104447/0000/myMicroAODOutputFile_1.root"
        #"root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/cmshgg/sethzenz/flashgg/ReMiniAOD-03Feb2017-2_5_4/2_5_1/DoubleEG/ReMiniAOD-03Feb2017-2_5_4-2_5_1-v0-Run2016E-03Feb2017-v1/170310_111722/0000/myMicroAODOutputFile_911.root"
        "root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIIFall17-3_1_0/3_1_0/THQ_ctcvcp_HToGG_M125_13TeV-madgraph-pythia8_TuneCP5/RunIIFall17-3_1_0-3_1_0-v0-RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/180605_204436/0000/myMicroAODOutputFile_35.root"
        #"root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/cmshgg/sethzenz/flashgg/RunIISummer16-2_4_1-25ns_Moriond17/2_4_1/VBFHToGG_M-125_13TeV_powheg_pythia8/RunIISummer16-2_4_1-25ns_Moriond17-2_4_1-v0-RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/170114_092754/0000/myMicroAODOutputFile_10.root"
        
        )
                             )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("test.root"))

process.extraDumpers = cms.Sequence()

import flashgg.Taggers.dumperConfigTools as cfgTools

import flashgg.Taggers.THQLeptonicTagVariables as var
if customize.processId.count("Data"):
    variablesToUse = minimalNonSignalVariables + var.vtx_variables + var.dipho_variables + var.photon_variables + var.lepton_variables + var.jet_variables + var.thqmva_variables + defaultVariables
elif customize.processId.count("thq") or customize.processId.count("thw"):
    variablesToUse = minimalVariables + var.vtx_variables + var.vtx_truth_variables + var.dipho_variables + var.photon_variables + var.lepton_variables + var.jet_variables + var.thqmva_variables + var.truth_variables + var.theoweight_variables + var.theoctcvweight_variables + defaultVariables
elif customize.processId.count("h_") or customize.processId.count("vbf"):
    variablesToUse = minimalVariables + var.vtx_variables + var.vtx_truth_variables + var.dipho_variables + var.photon_variables + var.lepton_variables + var.jet_variables + var.thqmva_variables + var.truth_variables + var.theoweight_variables + defaultVariables
else:
    variablesToUse = minimalVariables + var.vtx_variables + var.vtx_truth_variables + var.dipho_variables + var.photon_variables + var.lepton_variables + var.jet_variables + var.thqmva_variables + var.truth_variables  + defaultVariables

print "-------------------------------------------------"
print "--- Variables to be dumped, including systematic weights ---"
print variablesToUse
print "------------------------------------------------------------"


from flashgg.Taggers.tagsDumpers_cfi import *

# process.thqLeptonicTagDumper = createTagDumper("THQLeptonicTag")
# process.thqLeptonicTagDumper.dumpTrees = customize.dumpTrees
# process.thqLeptonicTagDumper.dumpWorkspace = customize.dumpWorkspace
# process.thqLeptonicTagDumper.nameTemplate ="$PROCESS_$SQRTS_$LABEL_$SUBCAT"

# cfgTools.addCategories(process.thqLeptonicTagDumper,
#                        ## categories definition
#                        [("all","1",0)
#                         ],                       
#                        ## variables to be dumped in trees/datasets. Same variables for all categories
#                        variables=variablesToUse,
#                        histograms=[]
#                        )


##### TAGDUMPER
process.load("flashgg.Taggers.diphotonTagDumper_cfi") ##  import diphotonTagDumper 
process.tagsDumper.className = "DiPhotonTagDumper"
process.tagsDumper.src = "flashggSystTagMerger"
#process.tagsDumper.src = "flashggTagSystematics"
process.tagsDumper.processId = "test"
process.tagsDumper.dumpTrees = customize.dumpTrees
process.tagsDumper.dumpWorkspace = customize.dumpWorkspace
process.tagsDumper.dumpHistos = False
process.tagsDumper.quietRooFit = True
process.tagsDumper.nameTemplate = cms.untracked.string("$PROCESS_$SQRTS_$CLASSNAME_$SUBCAT_$LABEL")
process.tagsDumper.splitPdfByStage0Cat = cms.untracked.bool(customize.doHTXS)

if(customize.doFiducial):
#    if customize.processId == "Data":
#        fc.addRecoGlobalVariables(process, process.tagsDumper)
#    else:
    fc.addObservables(process, process.tagsDumper, customize.processId )

#tagList=[
#["UntaggedTag",4],
#["VBFTag",2],
#["VHTightTag",0],
#["VHLooseTag",0],
#["VHEtTag",0],
#["VHHadronicTag",0],
#["TTHHadronicTag",0],
##["TTHLeptonicTag",0]
#]


if customize.doFiducial:
    tagList=[["SigmaMpTTag",3]]
elif customize.tthTagsOnly:
    tagList=[
        ["TTHHadronicTag",0],
        ["TTHLeptonicTag",0]
        ]
elif customize.thqTagsOnly:
    tagList=[
        ["THQLeptonicTag",0]
        ]
else:
    tagList=[
        ["NoTag",0],
        ["UntaggedTag",4],
        ["VBFTag",3],
        ["ZHLeptonicTag",0],
        ["WHLeptonicTag",0],
        ["VHLeptonicLooseTag",0],
        ["VHMetTag",0],
        ["VHHadronicTag",0],
        ["TTHHadronicTag",0],
        ["TTHLeptonicTag",0]
        ]

definedSysts=set()
process.tagsDumper.classifierCfg.remap=cms.untracked.VPSet()
for tag in tagList: 
  tagName=tag[0]
  tagCats=tag[1]
  # remap return value of class-based classifier
  process.tagsDumper.classifierCfg.remap.append( cms.untracked.PSet( src=cms.untracked.string("flashgg%s"%tagName), dst=cms.untracked.string(tagName) ) )
  for systlabel in systlabels:
      if not systlabel in definedSysts:
          # the cut corresponding to the systematics can be defined just once
          cutstring = "hasSyst(\"%s\") "%(systlabel)
          definedSysts.add(systlabel)
      else:
          cutstring = None
      if systlabel == "":
          currentVariables = variablesToUse
      else:
          if customize.doHTXS:
              currentVariables = systematicVariablesHTXS
          else:    
              currentVariables = systematicVariables + var.thqSystematicVariables
      if tagName == "NoTag":
          if customize.doHTXS:
              currentVariables = ["stage0cat[72,9.5,81.5] := tagTruth().HTXSstage0cat"]
          else:
              currentVariables = []
      isBinnedOnly = False #(systlabel !=  "")
      if ( customize.doPdfWeights  ) and ( (customize.datasetName() and customize.datasetName().count("HToGG")) or customize.processId.count("h_") or customize.processId.count("thq")  or customize.processId.count("thw") or customize.processId.count("vbf_") ) and (systlabel ==  "") and not (customize.processId == "th_125" or customize.processId == "bbh_125"):
          print "Signal MC central value, so dumping PDF weights"
          dumpPdfWeights = not ( customize.processId.count("thq")  or customize.processId.count("thw") ) #False ## was false before
          nPdfWeights = 60
          nAlphaSWeights = 2
          nScaleWeights = 9
      else:
          print "Data, background MC, or non-central value, or no systematics: no PDF weights"
          dumpPdfWeights = False
          nPdfWeights = -1
          nAlphaSWeights = -1
          nScaleWeights = -1
      
      cfgTools.addCategory(process.tagsDumper,
                           systlabel,
                           classname=tagName,
                           cutbased=cutstring,
                           subcats=tagCats, 
                           variables=currentVariables,
                           histograms=minimalHistograms,
                           binnedOnly=isBinnedOnly,
                           dumpPdfWeights=dumpPdfWeights,
                           nPdfWeights=nPdfWeights,
                           nAlphaSWeights=nAlphaSWeights,
                           nScaleWeights=nScaleWeights,
                           splitPdfByStage0Cat=customize.doHTXS
                           )

# Require standard diphoton trigger
from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltHighLevel= hltHighLevel.clone(HLTPaths = cms.vstring("HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v*",
#                                                                "HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v1",
#                                                                "HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v1"
                                                                ))

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# ee bad supercluster filter on data
process.load('RecoMET.METFilters.eeBadScFilter_cfi')
process.eeBadScFilter.EERecHitSource = cms.InputTag("reducedEgamma","reducedEERecHits") # Saved MicroAOD Collection (data only)
# Bad Muon filter
process.load('RecoMET.METFilters.badGlobalMuonTaggersMiniAOD_cff')
process.badGlobalMuonTaggerMAOD.muons = cms.InputTag("flashggSelectedMuons")
process.cloneGlobalMuonTaggerMAOD.muons = cms.InputTag("flashggSelectedMuons")

process.dataRequirements = cms.Sequence()
if customize.processId == "Data":
        process.dataRequirements += process.hltHighLevel
        process.dataRequirements += process.eeBadScFilter
        if customize.doMuFilter:
            process.dataRequirements += process.noBadGlobalMuonsMAOD

# Split WH and ZH
process.genFilter = cms.Sequence()
if (customize.processId.count("wh") or customize.processId.count("zh")) and not customize.processId.count("wzh"):
    process.load("flashgg/Systematics/VHFilter_cfi")
    process.genFilter += process.VHFilter
    process.VHFilter.chooseW = bool(customize.processId.count("wh"))
    process.VHFilter.chooseZ = bool(customize.processId.count("zh"))

if customize.processId.count("thq") or customize.processId.count("thw") or customize.processId == "bbh_125":
    process.load("flashgg/Systematics/CentralHiggsFilter_cfi")
    process.genFilter += process.CentralHiggsFilter

#pythia8 has an unanticipated EM showering feature, check have two photons from hard scatter
process.penultimateFilter= cms.Sequence()
if customize.processId.count("thq") or customize.processId.count("thw"): # for this sample the filter removes also H -> ZG
    process.load("flashgg/Systematics/HardProcessFinalStateFilter_cfi")
#    process.HardProcessFinalStateFilter.debug = True
    process.penultimateFilter += process.HardProcessFinalStateFilter

# Split out prompt-fake or fake-fake
process.finalFilter = cms.Sequence()
if (customize.processId.count("qcd") or customize.processId.count("gjet")) and customize.processId.count("fake"):
    process.load("flashgg/Systematics/PromptFakeFilter_cfi")
    process.finalFilter += process.PromptFakeFilter
    if (customize.processId.count("promptfake")):
        process.PromptFakeFilter.doPromptFake = cms.bool(True)
        process.PromptFakeFilter.doFakeFake =cms.bool(False)
    elif (customize.processId.count("fakefake")):
        process.PromptFakeFilter.doPromptFake =cms.bool(False)
        process.PromptFakeFilter.doFakeFake =cms.bool(True)
    else:
        raise Exception,"Mis-configuration of python for prompt-fake filter"


process.p = cms.Path(process.dataRequirements*
                     process.genFilter*
                     process.flashggUpdatedIdMVADiPhotons*
                     process.flashggDiPhotonSystematics*
                     process.flashggMetSystematics*
                     process.flashggMuonSystematics*process.flashggElectronSystematics*
                     (process.flashggUnpackedJets*process.jetSystematicsSequence)*
                     (process.flashggTagSequence*process.systematicsTagSequences)*
                     #process.flashggTagSorter*
                     process.flashggSystTagMerger*
                     process.penultimateFilter*
                     process.finalFilter*
                     process.tagsDumper)


#if( not hasattr(process,"options") ): process.options = cms.untracked.PSet()
#process.options.allowUnscheduled = cms.untracked.bool(True)

print "--- Dumping modules that take diphotons as input: ---"
mns = process.p.moduleNames()
for mn in mns:
    module = getattr(process,mn)
    if hasattr(module,"src") and type(module.src) == type(cms.InputTag("")) and module.src.value().count("DiPhoton"):
        print str(module),module.src
    elif hasattr(module,"DiPhotonTag"):
        print str(module),module.DiPhotonTag
print
printSystematicInfo(process)

customize.setDefault("maxEvents",1000)
customize.setDefault("targetLumi",1.00e+3)
# call the customization
customize(process)
