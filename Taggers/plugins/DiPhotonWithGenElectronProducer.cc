#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
// #include "flashgg/MicroAOD/interface/PhotonIdUtils.h"
#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"
// #include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
// #include "RecoEgamma/EgammaTools/plugins/EGExtraInfoModifierFromDB.cc"
// #include "CommonTools/CandAlgos/interface/ModifyObjectValueBase.h"
// #include "flashgg/Taggers/src/IsolationCorrection.C"

#include <iostream>

#include "TFile.h"
#include "TGraph.h"

using namespace std;
using namespace edm;
using namespace reco;

namespace flashgg {

    class DiPhotonWithGenElectronProducer : public edm::EDProducer
    {
    public:
        DiPhotonWithGenElectronProducer( const edm::ParameterSet & );
        void produce( edm::Event &, const edm::EventSetup & ) override;

        void addGenMatchElectron(edm::Handle<edm::View<reco::GenParticle> > genParticlesHandle, flashgg::Photon &photon);

    private:
        edm::EDGetTokenT<edm::View<flashgg::DiPhotonCandidate> > token_;
        edm::EDGetTokenT<edm::View<reco::GenParticle> > genParticleToken_;

        const double maxGenDeltaR_;
    };

    DiPhotonWithGenElectronProducer::DiPhotonWithGenElectronProducer( const edm::ParameterSet &ps ) :
        token_(consumes<edm::View<flashgg::DiPhotonCandidate> >(ps.getParameter<edm::InputTag>("src"))),
        genParticleToken_(consumes<edm::View<reco::GenParticle> >(ps.getParameter<edm::InputTag>("genParticles"))),
        maxGenDeltaR_(ps.getParameter<double>( "maxGenDeltaR" ))

    {
        produces<std::vector<flashgg::DiPhotonCandidate> >();
    }

    //----------------------------------------

    void DiPhotonWithGenElectronProducer::addGenMatchElectron(edm::Handle<edm::View<reco::GenParticle> > genParticlesHandle,
                                                              flashgg::Photon &photon) {
        unsigned int best = INT_MAX;
        float bestptdiff = 99e15;

        const auto &genParticles = *genParticlesHandle;

        // code adapted from flashgg/MicroAOD/plugins/PhotonProducer.cc
        for( unsigned int j = 0 ; j < genParticles.size() ; j++ ) {
            auto gen = genParticles[j];
            if( abs(gen.pdgId()) != 11 ) { continue; }

            // similar to ./MicroAOD/python/flashggGenPhotons_cfi.py
            // if( gen.pt() <= 5 ) { continue; }


            if( gen.status() != 1 ) { continue; }

            // std::cout << "found electron with status " << gen.status() << std::endl;

            float dR = reco::deltaR( photon, gen );

            if( dR > maxGenDeltaR_ ) { continue; }

            float ptdiff = fabs( photon.pt() - gen.pt() );
            if( ptdiff < bestptdiff ) {
                bestptdiff = ptdiff;
                best = j;
            }
        }

        if( best < INT_MAX ) {
            // auto &extra = genParticles[best];
            edm::Ptr<reco::GenParticle> extraPtr(genParticlesHandle, best);

            photon.setMatchedGenElectron( extraPtr );
        }

    }

    //----------------------------------------

    void DiPhotonWithGenElectronProducer::produce( edm::Event &evt, const edm::EventSetup & es)
    {
        edm::Handle<edm::View<flashgg::DiPhotonCandidate> > objects;
        evt.getByToken( token_, objects );

        edm::Handle<edm::View<reco::GenParticle> > genParticlesHandle;
        evt.getByToken( genParticleToken_, genParticlesHandle );
        auto_ptr<std::vector<flashgg::DiPhotonCandidate> > out_obj( new std::vector<flashgg::DiPhotonCandidate>() );

        // loop over existing diphotons
        for (const auto & obj : *objects) {
            flashgg::DiPhotonCandidate *new_obj = obj.clone();
            new_obj->makePhotonsPersistent();

            if( ! evt.isRealData() ) {
                // Gen matching
                addGenMatchElectron(genParticlesHandle, new_obj->getLeadingPhoton());
                addGenMatchElectron(genParticlesHandle, new_obj->getSubLeadingPhoton());
            }

            out_obj->push_back(*new_obj);
            delete new_obj;
        }
        evt.put(out_obj);
    }
}

typedef flashgg::DiPhotonWithGenElectronProducer FlashggDiPhotonWithGenElectronProducer;
DEFINE_FWK_MODULE( FlashggDiPhotonWithGenElectronProducer );

// Local Variables:
// mode:c++
// indent-tabs-mode:nil
// tab-width:4
// c-basic-offset:4
// End:
// vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
