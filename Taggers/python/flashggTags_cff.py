import FWCore.ParameterSet.Config as cms
from flashgg.MicroAOD.flashggJets_cfi import flashggBTag, maxJetCollections

bDiscriminator74X = cms.vdouble(0.605,0.890)
bDiscriminator76X = cms.vdouble(0.460,0.800)

flashggUnpackedJets = cms.EDProducer("FlashggVectorVectorJetUnpacker",
                                     JetsTag = cms.InputTag("flashggFinalJets"),
                                     NCollections = cms.uint32(maxJetCollections)
                                     )

UnpackedJetCollectionVInputTag = cms.VInputTag()
for i in range(0,maxJetCollections):
    UnpackedJetCollectionVInputTag.append(cms.InputTag('flashggUnpackedJets',str(i)))

flashggUntagged = cms.EDProducer("FlashggUntaggedTagProducer",
#                                 DiPhotonTag=cms.InputTag('flashggDiPhotons'),
                                 DiPhotonTag    = cms.InputTag('flashggPreselectedDiPhotons'),
                                 SystLabel      = cms.string(""),
                                 MVAResultTag   = cms.InputTag('flashggDiPhotonMVA'),
                                 GenParticleTag = cms.InputTag( "flashggPrunedGenParticles" ),
                                 Boundaries     = cms.vdouble(-0.398,0.308,0.624,0.907), #,1.000),
                                 RequireScaledPtCuts = cms.bool(True)
)

flashggSigmaMoMpToMTag = cms.EDProducer("FlashggSigmaMpTTagProducer",
#                                 DiPhotonTag=cms.InputTag('flashggDiPhotons'),
                                 DiPhotonTag    = cms.InputTag('flashggPreselectedDiPhotons'),
                                 SystLabel      = cms.string(""),
                                 MVAResultTag   = cms.InputTag('flashggDiPhotonMVA'),
                                 GenParticleTag = cms.InputTag( "flashggPrunedGenParticles" ),
                                 BoundariesSigmaMoM  = cms.vdouble(0.,0.00764,0.0109,0.0288), #boundaries have to be provided including lowest and highest
#                                 BoundariespToM      = cms.vdouble(0.,1.02,1.83,10.0), #,1.000), #boundaries have to be provided including lowest and highest
                                 RequireScaledPtCuts = cms.bool(True)
)



flashggTTHHadronicTag = cms.EDProducer("FlashggTTHHadronicTagProducer",
                                       DiPhotonTag=cms.InputTag('flashggPreselectedDiPhotons'),
                                       SystLabel=cms.string(""),
                                       MVAResultTag=cms.InputTag('flashggDiPhotonMVA'),
                                       ElectronTag=cms.InputTag('flashggSelectedElectrons'),
                                       MuonTag=cms.InputTag('flashggSelectedMuons'),
                                       VertexTag=cms.InputTag('offlineSlimmedPrimaryVertices'),
                                       GenParticleTag=cms.InputTag( 'flashggPrunedGenParticles' ),  
                                       leadPhoOverMassThreshold = cms.double(0.5),
                                       leadPhoPtThreshold = cms.double(20),  
                                       leadPhoUseVariableThreshold =  cms.bool(True),
                                       subleadPhoOverMassThreshold = cms.double(0.25),
                                       subleadPhoPtThreshold = cms.double(20),
                                       subleadPhoUseVariableThreshold =  cms.bool(True),
                                       MVAThreshold = cms.double(0.5),
                                       PhoMVAThreshold = cms.double(-0.9),
                                       inputTagJets= UnpackedJetCollectionVInputTag, 
                                       jetPtThreshold = cms.double(25.),
                                       jetEtaThreshold = cms.double(2.4),
                                       bDiscriminator = bDiscriminator76X, #For CMSSW74X use : bDiscriminator74X
                                       bTag = cms.string(flashggBTag),
                                       jetsNumberThreshold = cms.int32(5),
                                       bjetsNumberThreshold = cms.int32(1),  
                                       dRJetPhoLeadCut =  cms.double(0.4),
                                       dRJetPhoSubleadCut = cms.double(0.4),                          
                                       leptonPtThreshold = cms.double(20),
                                       muonEtaThreshold = cms.double(2.4), 
                                       muPFIsoSumRelThreshold = cms.double(0.25),
				       muMiniIsoSumRelThreshold = cms.double(0.05),	 
                                       electronEtaThresholds=cms.vdouble(1.4442,1.566,2.5),
                                       nonTrigMVAThresholds = cms.vdouble(0.913286,0.805013,0.358969),
                                       nonTrigMVAEtaCuts = cms.vdouble(0.8,1.479,2.5),
                                       electronIsoThreshold = cms.double(0.15),
				       elMiniIsoEBThreshold = cms.double(0.045),
                                       elMiniIsoEEThreshold = cms.double(0.08),
                                       electronNumOfHitsThreshold = cms.double(1),
                                       TransverseImpactParam = cms.double(0.02),
                                       LongitudinalImpactParam = cms.double(0.2),
                                       useStdLeptonID = cms.bool(True),
                                       useElectronMVARecipe = cms.bool(False),
                                       useElectronLooseID = cms.bool(True)                                     
                                       )

flashggVBFTag = cms.EDProducer("FlashggVBFTagProducer",
                               DiPhotonTag=cms.InputTag('flashggPreselectedDiPhotons'),
                               SystLabel=cms.string(""),
                               MVAResultTag=cms.InputTag('flashggDiPhotonMVA'),
                               VBFDiPhoDiJetMVAResultTag=cms.InputTag('flashggVBFDiPhoDiJetMVA'),
                               VBFMVAResultTag=cms.InputTag('flashggVBFMVA'),
                               GenParticleTag=cms.InputTag( "flashggPrunedGenParticles" ),
                               GenJetTag = cms.InputTag("slimmedGenJets"),
                               #Boundaries=cms.vdouble(0.21,0.6,0.81)
                               #  for the moment we have two categories VBF-0 and VBF-1: to be changed when the diphoton MVA is ready 
                               #Boundaries=cms.vdouble(0.5819, 0.9449)
                               #Boundaries=cms.vdouble(0.62, 0.94),
                               Boundaries=cms.vdouble(0.634, 0.919),
                               SetArbitraryNonGoldMC = cms.bool(False),
                               DropNonGoldData = cms.bool(False),
                               RequireVBFPreselection = cms.bool(True),
                               GetQCDWeights = cms.bool(False)
                               )


flashggVHEtTag = cms.EDProducer("FlashggVHEtTagProducer",
                                DiPhotonTag=cms.InputTag('flashggPreselectedDiPhotons'),
                                SystLabel=cms.string(""),
                                GenParticleTag=cms.InputTag( "flashggPrunedGenParticles" ),
                                MVAResultTag=cms.InputTag('flashggDiPhotonMVA'),
                                METTag=cms.InputTag('slimmedMETs'),   
                                leadPhoOverMassThreshold = cms.double(0.375),
                                subleadPhoOverMassThreshold = cms.double(0.25),
                                metPtThreshold = cms.double(70),
                                diphoMVAThreshold= cms.double(-1.0),
                                phoIdMVAThreshold= cms.double(-0.9)
                                #Boundaries=cms.vdouble(0.21,0.6,0.81)
)

flashggTTHLeptonicTag = cms.EDProducer("FlashggTTHLeptonicTagProducer",
                                       DiPhotonTag=cms.InputTag('flashggPreselectedDiPhotons'),
                                       SystLabel=cms.string(""),
                                       MVAResultTag=cms.InputTag('flashggDiPhotonMVA'),
                                       inputTagJets= UnpackedJetCollectionVInputTag,
                                       ElectronTag=cms.InputTag('flashggSelectedElectrons'),
                                       MuonTag=cms.InputTag('flashggSelectedMuons'),
                                       VertexTag=cms.InputTag('offlineSlimmedPrimaryVertices'),
                                       GenParticleTag=cms.InputTag( "flashggPrunedGenParticles" ),
                                       leptonPtThreshold = cms.double(20),
                                       muonEtaThreshold = cms.double(2.4),
                                       leadPhoOverMassThreshold = cms.double(0.5),
                                       subleadPhoOverMassThreshold = cms.double(0.25),
                                       MVAThreshold = cms.double(-0.4),
                                       PhoMVAThreshold = cms.double(-0.9), 
                                       deltaRMuonPhoThreshold = cms.double(0.4),
                                       deltaRJetLepThreshold = cms.double(0.4),
                                       jetsNumberThreshold = cms.double(2.),
                                       bjetsNumberThreshold = cms.double(1.),
                                       jetPtThreshold = cms.double(25.), 
                                       jetEtaThreshold= cms.double(2.4),
                                       deltaRJetLeadPhoThreshold = cms.double(0.4),
                                       deltaRJetSubLeadPhoThreshold = cms.double(0.4),
                                       bDiscriminator = bDiscriminator76X, #For CMSSW74X use : bDiscriminator74X
                                       bTag = cms.string(flashggBTag),
                                       muPFIsoSumRelThreshold = cms.double(0.25), 
				       muMiniIsoSumRelThreshold = cms.double(0.05),
                                       PuIDCutoffThreshold = cms.double(0.8),
                                       DeltaRTrkElec = cms.double(0.4),
                                       TransverseImpactParam = cms.double(0.02),
                                       LongitudinalImpactParam = cms.double(0.2),
                                       deltaRPhoElectronThreshold = cms.double(0.4),
                                       deltaMassElectronZThreshold = cms.double(10.),
                                       electronEtaThresholds=cms.vdouble(1.4442,1.566,2.5),
                                       nonTrigMVAThresholds = cms.vdouble(0.913286,0.805013,0.358969),
                                       nonTrigMVAEtaCuts = cms.vdouble(0.8,1.479,2.5),
                                       electronIsoThreshold = cms.double(0.15),
				       elMiniIsoEBThreshold = cms.double(0.045),
				       elMiniIsoEEThreshold = cms.double(0.08),
                                       electronNumOfHitsThreshold = cms.double(1),
                                       useStdLeptonID = cms.bool(True),
                                       useElectronMVARecipe = cms.bool(False),
                                       useElectronLooseID = cms.bool(True)
)
flashggVHLooseTag = cms.EDProducer("FlashggVHLooseTagProducer",
                                   DiPhotonTag=cms.InputTag('flashggPreselectedDiPhotons'),
                                   SystLabel=cms.string(""),
                                   #JetTag=cms.InputTag('flashggSelectedJets'),
                                   inputTagJets= UnpackedJetCollectionVInputTag,
                                   ElectronTag=cms.InputTag('flashggSelectedElectrons'),
                                   MuonTag=cms.InputTag('flashggSelectedMuons'),
                                   VertexTag=cms.InputTag('offlineSlimmedPrimaryVertices'),
                                   MVAResultTag=cms.InputTag('flashggDiPhotonMVA'),
                                   METTag=cms.InputTag('slimmedMETs'),
                                   GenParticleTag=cms.InputTag( "flashggPrunedGenParticles" ),
                                   leptonPtThreshold = cms.double(20),
                                   muonEtaThreshold = cms.double(2.4),
                                   leadPhoOverMassThreshold = cms.double(0.375),
                                   subleadPhoOverMassThreshold = cms.double(0.25),
                                   MVAThreshold = cms.double(-1.0),
                                   deltaRMuonPhoThreshold = cms.double(1),
                                   jetsNumberThreshold = cms.double(3.),
                                   jetPtThreshold = cms.double(20.),
                                   jetEtaThreshold= cms.double(2.4),
                                   deltaRPhoLeadJet = cms.double(0.5),
                                   deltaRPhoSubLeadJet = cms.double(0.5),
                                   muPFIsoSumRelThreshold = cms.double(0.25), 
                                   deltaRJetMuonThreshold = cms.double(0.5),
                                   PuIDCutoffThreshold = cms.double(0.8),
                                   PhoMVAThreshold = cms.double(-0.9),
                                   METThreshold = cms.double(45.),
                                   ElectronPtThreshold = cms.double(20.),
                                   DeltaRTrkElec = cms.double(1.),
                                   TransverseImpactParam = cms.double(0.02),
                                   LongitudinalImpactParam = cms.double(0.2),
                                   deltaRPhoElectronThreshold = cms.double(1.),
                                   deltaMassElectronZThreshold = cms.double(10.),
                                   electronEtaThresholds=cms.vdouble(1.4442,1.566,2.5),
                                   nonTrigMVAThresholds = cms.vdouble(0.913286,0.805013,0.358969),
                                   nonTrigMVAEtaCuts = cms.vdouble(0.8,1.479,2.5),
                                   electronIsoThreshold = cms.double(0.15),
                                   electronNumOfHitsThreshold = cms.double(1)

				    )
flashggVHTightTag = cms.EDProducer("FlashggVHTightTagProducer",
                                   DiPhotonTag=cms.InputTag('flashggPreselectedDiPhotons'),
                                   SystLabel=cms.string(""),
                                   #JetTag=cms.InputTag('flashggSelectedJets'),
                                   inputTagJets= UnpackedJetCollectionVInputTag,
                                   ElectronTag=cms.InputTag('flashggSelectedElectrons'),
                                   MuonTag=cms.InputTag('flashggSelectedMuons'),
                                   VertexTag=cms.InputTag('offlineSlimmedPrimaryVertices'),
                                   MVAResultTag=cms.InputTag('flashggDiPhotonMVA'),
                                   METTag=cms.InputTag('slimmedMETs'),
                                   GenParticleTag=cms.InputTag( "flashggPrunedGenParticles" ),
                                   leptonPtThreshold = cms.double(20),
                                   muonEtaThreshold = cms.double(2.4),
                                   leadPhoOverMassThreshold = cms.double(0.375),
                                   subleadPhoOverMassThreshold = cms.double(0.25),
                                   MVAThreshold = cms.double(-1.0),
                                   deltaRMuonPhoThreshold = cms.double(1),
                                   jetsNumberThreshold = cms.double(3.),
                                   jetPtThreshold = cms.double(20.),
                                   jetEtaThreshold= cms.double(2.4),
                                   muPFIsoSumRelThreshold = cms.double(0.25), 
                                   PuIDCutoffThreshold = cms.double(0.8),
                                   PhoMVAThreshold = cms.double(-0.9),
                                   METThreshold = cms.double(45.),
                                   deltaRJetMuonThreshold = cms.double(0.5),
                                   invMassLepLowThreshold = cms.double(70.),
                                   invMassLepHighThreshold = cms.double(110.),
                                   numberOfLowPtMuonsThreshold = cms.double(2.),
                                   numberOfHighPtMuonsThreshold = cms.double(1.),
                                   leptonLowPtThreshold = cms.double(10.),
                                   deltaRLowPtMuonPhoThreshold = cms.double(0.5),
                                   deltaRPhoLeadJet = cms.double(0.5),
                                   deltaRPhoSubLeadJet = cms.double(0.5),
                                   ElectronPtThreshold = cms.double(20.),
                                   DeltaRTrkElec = cms.double(1.),
                                   TransverseImpactParam = cms.double(0.02),
                                   LongitudinalImpactParam = cms.double(0.2),
                                   deltaRPhoElectronThreshold = cms.double(1.),
                                   deltaMassElectronZThreshold = cms.double(10.),
                                   electronEtaThresholds=cms.vdouble(1.4442,1.566,2.5),
                                   nonTrigMVAThresholds = cms.vdouble(0.913286,0.805013,0.358969),
                                   nonTrigMVAEtaCuts = cms.vdouble(0.8,1.479,2.5),
                                   electronIsoThreshold = cms.double(0.15),
                                   electronNumOfHitsThreshold = cms.double(1)
)


flashggVHHadronicTag = cms.EDProducer("FlashggVHHadronicTagProducer",
                                      DiPhotonTag = cms.InputTag('flashggPreselectedDiPhotons'),
                                      SystLabel=cms.string(""),
                                      MVAResultTag=cms.InputTag('flashggDiPhotonMVA'),
                                      #JetTag = cms.InputTag('flashggSelectedJets'),
                                      inputTagJets= UnpackedJetCollectionVInputTag,
                                      GenParticleTag=cms.InputTag( "flashggPrunedGenParticles" ),
                                      leadPhoOverMassThreshold = cms.double(0.375),
                                      subleadPhoOverMassThreshold = cms.double(0.25),
                                      diphoMVAThreshold = cms.double(-1.0),
                                      jetsNumberThreshold = cms.double(2.),
                                      jetPtThreshold = cms.double(40.),
                                      jetEtaThreshold= cms.double(2.4),
                                      dRJetToPhoLThreshold = cms.double(0.5),
                                      dRJetToPhoSThreshold = cms.double(0.5),
                                      dijetMassLowThreshold = cms.double(60.),
                                      dijetMassHighThreshold = cms.double(120.),
                                      cosThetaStarThreshold = cms.double(0.5),
                                      phoIdMVAThreshold = cms.double(-0.9)
)

# Tag is for jet studies only, not in default sequence
flashggZPlusJetTag = cms.EDProducer("FlashggZPlusJetTagProducer",
                                    DiPhotonTag    = cms.InputTag('flashggPreselectedDiPhotons'),
                                    SystLabel      = cms.string(""),
                                    MVAResultTag   = cms.InputTag('flashggDiPhotonMVA'),
                                    inputTagJets= UnpackedJetCollectionVInputTag,
                                    GenParticleTag=cms.InputTag( "flashggPrunedGenParticles" ),
                                    GenJetTag = cms.InputTag("slimmedGenJets")
                                    )

