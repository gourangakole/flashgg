// By L D CORPE
// Adapted from the flashggCommissioning tree maker code  by C. Favaro et al.

#include <memory>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/MergeableDouble.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
//#include "DataFormats/Common/interface/PtrVector.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "flashgg/MicroAOD/interface/VertexSelectorBase.h"
#include "flashgg/DataFormats/interface/Photon.h"
#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"

#include "flashgg/MicroAOD/interface/PhotonIdUtils.h"

#include "flashgg/DataFormats/interface/VertexCandidateMap.h"
#include "flashgg/DataFormats/interface/Jet.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "flashgg/DataFormats/interface/VBFTag.h"
#include "flashgg/DataFormats/interface/UntaggedTag.h"
#include "flashgg/DataFormats/interface/DiPhotonTagBase.h"
#include "flashgg/DataFormats/interface/TTHHadronicTag.h"
#include "flashgg/DataFormats/interface/TTHLeptonicTag.h"

#include "FWCore/Common/interface/TriggerNames.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"

#include "TMath.h"
#include "TTree.h"
#include "TVector3.h"
#include "TLorentzVector.h"

using namespace std;
using namespace edm;
using namespace flashgg;

// **********************************************************************

class FlashggTreeMakerWithTagSorter : public edm::EDAnalyzer
{
public:
    explicit FlashggTreeMakerWithTagSorter( const edm::ParameterSet & );
    ~FlashggTreeMakerWithTagSorter();

    static void fillDescriptions( edm::ConfigurationDescriptions &descriptions );

private:

    edm::Service<TFileService> fs_;

    virtual void beginJob() override;
    virtual void analyze( const edm::Event &, const edm::EventSetup & ) override;
    virtual void endJob() override;

    virtual void endLuminosityBlock(edm::LuminosityBlock const& iLumi, edm::EventSetup const& iSetup) override;
    
    EDGetTokenT<View<reco::Vertex> > vertexToken_;
    EDGetTokenT<View<reco::GenParticle> > genParticleToken_;
    EDGetTokenT<GenEventInfoProduct> tok_GenEvInfo_;
    EDGetTokenT< VertexCandidateMap > vertexCandidateMapTokenDz_;
    EDGetTokenT< VertexCandidateMap > vertexCandidateMapTokenAOD_;
    //EDGetTokenT<View<flashgg::Jet> > jetTokenDz_;
    std::vector<edm::InputTag> inputTagJets_;
    EDGetTokenT<edm::View<flashgg::DiPhotonCandidate> >  diPhotonToken_;
    EDGetTokenT<edm::View<pat::MET> >  METToken_;
    EDGetTokenT<edm::View<PileupSummaryInfo> >  PileUpToken_;
    edm::InputTag rhoFixedGrid_;

    TTree *flashggTreeWithTagSorter;
    TTree *auxTree;
    edm::EDGetTokenT<edm::MergeableDouble> weightTokenDummy_;

    // Variables to fill
    Int_t run;
    Int_t lumis;
    ULong64_t event;
    Float_t dRphojet1;
    Float_t dRphojet2;
    Float_t njets10;
    Float_t njets15;
    Float_t njets20;
    Int_t isconv1;
    Int_t isconv2;
    Int_t haspixelseed1;
    Int_t haspixelseed2;
    Int_t itype;
    Float_t nvtx;
    Float_t rho;
    Double_t gen_weight;
    Double_t xsec_weight;
    Double_t full_weight;
    Double_t pu_weight;
    Float_t pu_n;
    Float_t mass;
    Float_t dipho_pt;
    Float_t dipho_phi;
    Float_t dipho_eta;
    Float_t full_cat;
    Float_t et1;
    Float_t et2;
    Float_t eta1;
    Float_t eta2;
    Float_t phi1;
    Float_t phi2;
    Float_t r91;
    Float_t r92;
    Float_t sieie1;
    Float_t sieie2;
    Float_t hoe1;
    Float_t hoe2;
    Float_t sigmaEoE1;
    Float_t sigmaEoE2;
    Float_t ptoM1;
    Float_t ptoM2;
    Float_t isEB1;
    Float_t isEB2;
    Float_t chiso1;
    Float_t chiso2;
    Float_t chisow1;
    Float_t chisow2;
    Float_t phoiso1;
    Float_t phoiso2;
    Float_t phoiso041;
    Float_t phoiso042;
    Float_t ecaliso03_1;
    Float_t ecaliso03_2;
    Float_t hcaliso03_1;
    Float_t hcaliso03_2;
    Float_t pfcluecal03_1;
    Float_t pfcluecal03_2;
    Float_t pfcluhcal03_1;
    Float_t pfcluhcal03_2;
    Float_t trkiso03_1;
    Float_t trkiso03_2;
    Float_t pfchiso2_1;
    Float_t pfchiso2_2;
    Float_t sieip1;
    Float_t sieip2;
    Float_t etawidth1;
    Float_t phiwidth1;
    Float_t etawidth2;
    Float_t phiwidth2;
    Float_t regrerr1;
    Float_t regrerr2;
    Float_t cosphi;
    Float_t genmatch1;
    Float_t genmatch2;
    Float_t cicpf4cutlevel1;
    Float_t cicpf4cutlevel2;
    Float_t idmva1;
    Float_t idmva2;
    Float_t vbfcat;
    Float_t MET;
    Float_t MET_phi;
    Float_t isorv1;
    Float_t isowv1;
    Float_t isorv2;
    Float_t isowv2;
    Float_t s4ratio1;
    Float_t s4ratio2;
    Float_t effSigma1;
    Float_t effSigma2;
    Float_t scraw1;
    Float_t scraw2;
    Float_t ese1;
    Float_t ese2;
    Float_t vtx_x;
    Float_t vtx_y;
    Float_t vtx_z;
    Float_t gv_x;
    Float_t gv_y;
    Float_t gv_z;
    Float_t dijet_leadEta;
    Float_t dijet_subleadEta;
    Float_t dijet_LeadJPt;
    Float_t dijet_SubJPt;
    Float_t dijet_dEta;
    Float_t dijet_Zep;
    Float_t dijet_dPhi;
    Float_t dijet_Mjj;
    Float_t dijet_MVA;
    Float_t bdt_combined;
    Float_t issyst;
    Float_t name1;
    Float_t sigmaMrvoM;
    Float_t sigmaMwvoM;
    Float_t vtxprob;
    Float_t ptbal;
    Float_t ptasym;
    Float_t logspt2;
    Float_t p2conv;
    Float_t nconv;
    Float_t vtxmva;
    Float_t vtxdz;
    Float_t dipho_mva;
    Float_t dipho_mva_cat;
    Float_t dipho_PToM;
    //Tag Categories
    Int_t flash_Untagged_Category;
    Int_t flash_VBFTag_Category;
    Int_t leadjet_genmatch;
    Int_t subljet_genmatch;
    Float_t e1x31;
    Float_t e2x51;
    Float_t e3x31;
    Float_t e5x51;
    Float_t e1x32;
    Float_t e2x52;
    Float_t e3x32;
    Float_t e5x52;
    int passSel[15];

    edm::EDGetTokenT<edm::View<flashgg::Photon> >            photonToken_; // SCZ work-in-progress adding this!
    edm::EDGetTokenT<edm::OwnVector<flashgg::DiPhotonTagBase> > TagSorterToken_;
    edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
    edm::Handle<edm::TriggerResults> triggerResultsHandle_;
    std::vector<std::string> pathNames_;

    Double_t totalGenWeight_;

    std::string processID_;
    bool puReweight_;
    std::vector<double> puData_;
    std::vector<double> puMC_;
    int npu_;
    double minpu_, maxpu_;
};
