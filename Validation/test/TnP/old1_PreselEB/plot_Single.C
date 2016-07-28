#include "TFile.h"
#include "TH1.h"
#include "TH1F.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include <string>
#include <functional>
#include <istream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <TROOT.h>
#include <vector>
#include <sstream>
#include <TH1F.h>
#include <TFile.h>
#include <TCanvas.h>


void plot_Single() {

  TFile *f = new TFile("try.root","RECREATE");
  
  TFile* _fileMC = TFile::Open("efficiency-data-passingPresel-EB.root");
  
  TDirectory* dir = _fileMC->GetDirectory("PhotonToRECO/passingPresel/probe_Pho_r9_bin0__probe_sc_abseta_bin0__passingPresel_0p0To0p85_0p0To1p479/");
  TString fitname = "fit_canvas";
  
  TCanvas *canvas = (TCanvas*)dir->Get("fit_canvas");
  RooHist *rh = (RooHist*)canvas->GetPrimitive("fit_canvas_1");
  TH1F *h = (TH1F*)rh->GetHistogram();
  
  h->GetXaxis()->SetTitle("pt_muon");
  h->GetXaxis()->SetTitleSize(0.06);
  h->GetXaxis()->SetTitleOffset(0.56);
  h->GetYaxis()->SetTitle("Muon ID efficiency");
  h->GetYaxis()->SetTitleSize(0.05);
  h->SetMaximum(1.05);
  h->SetMinimum(0.6);
  
  h->SetFillColor(4);
  h->SetFillStyle(0);
  h->SetLineColor(4);
  h->SetLineWidth(2);
  //canvas->Clear();
  canvas->Draw();
  //h->Draw("AP");
  return ;

}
