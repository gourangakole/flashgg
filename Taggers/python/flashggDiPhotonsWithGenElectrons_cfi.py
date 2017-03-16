import FWCore.ParameterSet.Config as cms

flashggDiPhotonsWithGenElectrons = cms.EDProducer("FlashggDiPhotonWithGenElectronProducer",
                                                          # note that these come AFTER updated flashggUpdatedIdMVADiPhotons
                                                          src          = cms.InputTag("flashggPreselectedDiPhotons"),

                                                          genParticles = cms.InputTag("flashggPrunedGenParticles"),
                                                          maxGenDeltaR = cms.double(0.1),
                                                          ) 

