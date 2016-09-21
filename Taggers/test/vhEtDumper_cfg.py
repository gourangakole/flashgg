#!/usr/bin/env cmsRun

import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
from FWCore.ParameterSet.VarParsing import VarParsing

from flashgg.MetaData.samples_utils import SamplesManager

## CMD LINE OPTIONS ##
options = VarParsing('analysis')
print options

# maxEvents is the max number of events processed of each file, not globally
options.maxEvents = -1
#options.inputFiles = "file:/tmp/nancy/vhEtTagOutputFile_VHsignal.root" 
options.inputFiles = "file:myTagOutputFile.root" 

options.outputFile = "VHEtTagsDump_signal.root" 
options.parseArguments()

## I/O SETUP ##
#process = cms.Process("VHEtTagsDumper")
process = cms.Process("VHLooseTagsDumper")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1 )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring(options.inputFiles))

if options.maxEvents > 0:
    process.source.eventsToProcess = cms.untracked.VEventRange('1:1-1:'+str(options.maxEvents))

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputFile))

from flashgg.Taggers.tagsDumpers_cfi import createTagDumper
import flashgg.Taggers.dumperConfigTools as cfgTools

#process.vhEtTagDumper = createTagDumper("VHEtTag")
process.vhEtTagDumper = createTagDumper("VHLooseTag")
process.vhEtTagDumper.dumpTrees = True
process.vhEtTagDumper.dumpHistos = True

dipho_variables=["dipho_sumpt      := diPhoton.sumPt",
                 "dipho_cosphi     := abs(cos(diPhoton.leadingPhoton.phi - diPhoton.subLeadingPhoton.phi))",
                 "mass             := diPhoton.mass",
                 "leadPt           := diPhoton.leadingPhoton.pt",
                 "leadEt           := diPhoton.leadingPhoton.et",
                 "leadEta          := diPhoton.leadingPhoton.eta",
                 "leadPhi          := diPhoton.leadingPhoton.phi",
                 "lead_sieie       := diPhoton.leadingPhoton.sigmaIetaIeta",
                 "lead_hoe         := diPhoton.leadingPhoton.hadronicOverEm",
                 "lead_sigmaEoE    := diPhoton.leadingPhoton.sigEOverE",
                 "lead_ptoM        := diPhoton.leadingPhoton.pt/diPhoton.mass",
                 "leadR9           := diPhoton.leadingPhoton.r9",
                 "subleadPt        := diPhoton.subLeadingPhoton.pt",
                 "subleadEt        := diPhoton.subLeadingPhoton.et",
                 "subleadEta       := diPhoton.subLeadingPhoton.eta",
                 "subleadPhi       := diPhoton.subLeadingPhoton.phi",
                 "sublead_sieie    := diPhoton.subLeadingPhoton.sigmaIetaIeta",
                 "sublead_hoe      := diPhoton.subLeadingPhoton.hadronicOverEm",
                 "sublead_sigmaEoE := diPhoton.subLeadingPhoton.sigEOverE",
                 "sublead_ptoM     := diPhoton.subLeadingPhoton.pt/diPhoton.mass",
                 "subleadR9        := diPhoton.subLeadingPhoton.r9",
                 "leadIDMVA        := diPhoton.leadingView.phoIdMvaWrtChosenVtx",
                 "subleadIDMVA     := diPhoton.subLeadingView.phoIdMvaWrtChosenVtx",]

cfgTools.addCategories(process.vhEtTagDumper,
                       ## categories definition                                                                                                                                                                                  
                       [("all","1",0)
                    ],
                       ## variables to be dumped in trees/datasets. Same variables for all categories                                                                                                                            
                       variables=dipho_variables+
                       ["pfMET_rawPt        := met.uncorPt",
                        "pfMET_rawPhi       := met.uncorPhi",
                        "pfMET_rawSumEt     := met.uncorSumEt",
                        "pfMET_corPt        := met.corPt",
                        "pfMET_corPhi       := met.corPhi",
                        "pfMET_corSumEt     := met.corSumEt",
                        "caloMET_rawPt      := met.caloMETPt",
                        "caloMET_rawPhi     := met.caloMETPhi",
                        "caloMET_rawSumEt   := met.caloMETSumEt",
                        "genMET_pt          := met.genMET.pt",
                        "genMET_phi         := met.genMET.phi",
                        "genMET_sumEt       := met.genMET.sumEt",
                        "pfNeutralEMFraction := met.NeutralEMFraction",
                        "pfNeutralHadEtFraction := met.NeutralHadEtFraction",
                        "pfChargedEMEtFraction := met.ChargedEMEtFraction",
                        "pfChargedHadEtFraction := met.ChargedHadEtFraction"
                        ],
                       histograms=["mass>>mass(160,100,180)",
                                   "subleadPt:leadPt>>ptLeadvsSub(180,20,200:180,20,200)",
                                   "leadIDMVA>>leadIDMVA(50,0,1)",
                                   "subleadIDMVA>>subleadIDMVA(50,0,1)",
                                   "pfMET_rawPt>>pfMET_rawPt(250,0,500)",
                                   "pfMET_corPt>>pfMET_corPt(250,0,500)",
                                   "pfMET_rawSumEt>>pfMET_rawSumEt(400,200,2000)",
                                   "pfMET_corSumEt>>pfMET_corSumEt(400,200,2000)",
                                   "caloMET_rawPt>>caloMET_rawPt(250,0,500)",
                                   "caloMET_rawSumEt>>caloMET_rawSumEt(400,200,2000)",
                                   "pfMET_rawPhi>>pfMET_rawPhi(100,-3.14,3.14)",
                                   "pfMET_corPhi>>pfMET_corPhi(100,-3.14,3.14)",
                                   "caloMET_rawPhi>>caloMET_rawPhi(100,-3.14,3.14)",
                                   "genMET_pt>>genMET_pt(250,0,500)",
                                   "genMET_phi>>genMET_phi(100,-3.14,3.14)",
                                   "genMET_sumEt>>genMET_sumEt(400,200,2000)"
                                  ]
                       )



process.p1 = cms.Path(
    process.vhEtTagDumper
    )

print process.p1
