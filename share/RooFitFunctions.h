#include "RooChi2Var.h"

double GetChiSquare(RooRealVar& obsVar,RooAbsReal& f,RooDataHist& data,int ndof_bins) {
  RooChi2Var* chi2_lowerSideBand = new RooChi2Var("chi2_low","chi2_low", f, data, RooFit::DataError(RooAbsData::Poisson), RooFit::Range("lower"));
  RooChi2Var* chi2_upperSideBand = new RooChi2Var("chi2_up","chi2_up", f, data, RooFit::DataError(RooAbsData::Poisson), RooFit::Range("upper"));
  double chi2 = chi2_lowerSideBand->getValV() + chi2_upperSideBand->getValV();

  delete chi2_lowerSideBand;
  delete chi2_upperSideBand;
  
  return chi2/float(ndof_bins);
}

std::map<std::string,double> NoMemoryLeakSnapshot(RooArgSet& set) {
  std::map<std::string,double> ret;
  
  TIterator *iterator= set.createIterator();
  RooRealVar *arg = 0;
  while((arg = (RooRealVar*)iterator->Next())) {
    //std::cout << "Saving: " << arg->GetName() << std::endl;
    ret[arg->GetName()] = arg->getVal();
  }
  delete iterator;
  return ret;
}

void ReturnToSnapshot(RooArgSet& set,std::map<std::string,double> snap) {
  TIterator *iterator= set.createIterator();
  RooRealVar *arg = 0;
  while((arg = (RooRealVar*)iterator->Next())) {
    //std::cout << "Resetting: " << arg->GetName() << std::endl;
    arg->setVal(snap[arg->GetName()]);
  }
  delete iterator;
  return;
}

std::vector<double> ExecuteToy(RooAbsPdf& f1,RooAbsPdf& f2,RooRealVar& obsVar,int ndof_bins_1,int ndof_bins_2){
  // generate binned
  RooDataHist* toy_data = f1.generateBinned(obsVar,RooFit::Extended());

  // Fit f1
  RooArgSet* initial = f1.getParameters(toy_data);
  std::map<std::string,double> initialState = NoMemoryLeakSnapshot(*initial);
  //RooArgSet* initialState = (RooArgSet*)f1.getParameters(toy_data)->snapshot(false); // snapshot
  RooFitResult* rfres = f1.fitTo(*toy_data,
                                 RooFit::Extended(),
                                 RooFit::Range("lower,upper"),
                                 RooFit::Minimizer("Minuit2","migrad"),
                                 RooFit::Strategy(2)
                                 );
  delete rfres;
  double chi2 = GetChiSquare(obsVar,f1,*toy_data,ndof_bins_1);
  ReturnToSnapshot(*initial,initialState);
  delete initial;

  // Fit f2
  RooArgSet* initial_2 = f2.getParameters(toy_data);
  std::map<std::string,double> initialState_2 = NoMemoryLeakSnapshot(*initial_2);
  RooFitResult* rfres2 = f2.fitTo(*toy_data,
                                  RooFit::Extended(),
                                  RooFit::Range("lower,upper"),
                                  RooFit::Minimizer("Minuit2","migrad"),
                                  RooFit::Strategy(2)
                                  );
  delete rfres2;
  double chi2_2 = GetChiSquare(obsVar,f2,*toy_data,ndof_bins_2);
  ReturnToSnapshot(*initial_2,initialState_2);
  delete initial_2;

  std::vector<double> res;
  res.push_back(chi2);
  res.push_back(chi2_2);

  delete toy_data;
  return res;
}
