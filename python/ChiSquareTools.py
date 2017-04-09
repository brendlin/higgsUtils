
##################################################################################
def FitForChi2_DataSidebands(f) :
    #ROOT.gROOT.ProcessLine('.L Extras.h')
    #ROOT.gROOT.LoadMacro("rootlogon.C+")
    #rootlogon()
    #print list(ROOT.gROOT.GetListOfFunctions())
    ROOT.gROOT.LoadMacro("Extras.h+")
    ROOT.ListExtras()

    f.obsVar.setBins(f.datasb_rebinned.numEntries())
    print f.datasb_rebinned.numEntries()
    f.obsVar.setRange("lower",105,120) ; 
    f.obsVar.setRange("upper",130,160) ; 

#     args_datalimit_sideband = ROOT.RooLinkedList()
#     blah2 = ROOT.RooFit.Extended(True)               ; args_datalimit_sideband.Add(blah2)
    #blah3 = ROOT.RooFit.Minimizer('Minuit2','migrad'); args_datalimit_sideband.Add(blah3)
#     blah3 = ROOT.RooFit.Minimizer('Minuit2')         ; args_datalimit_sideband.Add(blah3)
#     blah3a= ROOT.RooFit.Strategy(2)                  ; args_datalimit_sideband.Add(blah3a)
    #blah4 = ROOT.RooFit.Offset()                     ; args_datalimit_sideband.Add(blah4)
    #blah5 = ROOT.RooFit.PrintEvalErrors(-1)          ; args_datalimit_sideband.Add(blah5)
#     blah1 = ROOT.RooFit.Range("lower,upper")         ; args_datalimit_sideband.Add(blah1)
#     blah6 = ROOT.RooFit.Save()                       ; args_datalimit_sideband.Add(blah6)
    #blah7 = ROOT.RooFit.SumW2Error(False)            ; args_datalimit_sideband.Add(blah7)
#     print 'just before this.',args_datalimit_sideband.Print("")
#     printArgs(f.BkgArgList)
    f.BkgNormalization.setVal(f.datahist.Integral())
    f.workspace.Print()
    #f.BkgNormalization.setConstant(False)
    #SetBkgToConstant(f,False)

    #f.function_ext.chi2FitTo(f.datasb_rebinned,args_datalimit_sideband)
    #f.function_ext.chi2FitTo(f.datasb_rebinned,ROOT.RooFit.Range("lower,upper"),ROOT.RooFit.Extended(True))
    ClearRooPlot(f.frame)

    printArgs(f.BkgArgList)
    ROOT.chi2FitTo_KB(f.function_ext,f.datasb_rebinned)
#                       ROOT.RooFit.Range("lower,upper"),
#                       ROOT.RooFit.Extended(True),
#                       ROOT.RooFit.Strategy(2),
#                       ROOT.RooFit.Minimizer('Minuit2'),
#                       ROOT.RooFit.Save()
#                       )
#     f.function_ext.fitTo(f.datasb_rebinned,ROOT.RooFit.Range("lower,upper"),*(args_datalimit))
    printArgs(f.BkgArgList)


    #f.function_ext.chi2FitTo(f.af2_rebinned,args_datalimit_sideband) # lower,upper
    f.function_ext.Print()
    print f.BkgNormalization.getVal(),f.datahist.Integral()

    f.datasb_rebinned.plotOn(f.frame)
    #f.af2_rebinned.plotOn(f.frame)
    f.function_ext.plotOn(f.frame,*plotOptions_sb)
    c = ROOT.TCanvas('asdf','asdf',600,500)
    f.frame.Draw()
    raw_input('pause')

    return

##################################################################################
def GetChiSquare_ForSpuriousSignal(frame,af2,function,ndof) :
    ClearRooPlot(frame)
    af2.plotOn(frame)
    function.plotOn(frame)
    # Get the chi2 from the background-only fit
    chisquare = frame.chiSquare(1+ndof) # n-1 bins
    return chisquare

##################################################################################
def ChiSquareToys_ForSpuriousSignal(f,outdir) :
    ClearRooPlot(f.frame)
    f.obsVar.setBins(55)
    h = ROOT.TH1F('p_chi2_hist','p_chi2_hist',10000,0,1)
    c2 = ROOT.TH1F('chi2_hist','chi2_hist',10000,0,5)
    #h_tmp = f.af2hist_not_rebinned.Clone()
    #h_tmp.SetName('h_tmp')
    rand = ROOT.TRandom3()

    # Make a smooth version of the AF2 based on the fitted function
    f.BkgNormalization.setVal(f.af2_rebinned.sumEntries())
    asimov = f.function_ext.generateBinned(ROOT.RooArgSet(f.obsVar),ROOT.RooFit.ExpectedData(),ROOT.RooFit.Name('asimov'))
    print type(asimov)
    h_asimov = asimov.createHistogram("m_yy")
    for j in range(f.af2hist_not_rebinned.GetNbinsX()) :
        h_asimov.SetBinError(j+1,f.af2hist_not_rebinned.GetBinError(j+1))
    h_tmp = h_asimov.Clone(h_asimov.GetName()+'_tmp')
    for j in range(f.af2hist_not_rebinned.GetNbinsX()) :
        h_tmp.SetBinContent(j+1,rand.Gaus(h_asimov.GetBinContent(j+1),h_asimov.GetBinError(j+1)))

#     c = ROOT.TCanvas()
#     f.af2hist_not_rebinned.Draw()
#     h_asimov.Draw('sames')
#     h_asimov.SetLineColor(ROOT.kBlue); h_asimov.SetMarkerColor(ROOT.kBlue);
#     h_tmp.SetLineColor(ROOT.kRed); h_tmp.SetMarkerColor(ROOT.kRed);
#     h_tmp.Draw('sames')

    #f.data.plotOn(f.frame)
    #asimov.plotOn(f.frame)
    #f.frame.Draw()
#     raw_input('pause')

    for i in range(100) :
        if not i%1000 : print i
        for j in range(h_tmp.GetNbinsX()) :
            new_bin_content = rand.Gaus(h_asimov.GetBinContent(j+1),h_asimov.GetBinError(j+1))
            #if j == 0 : print new_bin_content
            h_tmp.SetBinContent(j+1,new_bin_content)
            h_tmp.SetBinError(j+1,h_asimov.GetBinError(j+1))
            
        toy_data = ROOT.RooDataHist('h_tmp_%d'%(i),'',ROOT.RooArgList(f.obsVar),h_tmp,1.)
        #bins = toy_data.numEntries()
        f.function.fitTo(toy_data,ROOT.RooFit.Minimizer("Minuit2", "migrad"),ROOT.RooFit.Offset(),ROOT.RooFit.SumW2Error(True))
        h_tmp_rebinned = h_tmp.Clone()
        h_tmp_rebinned.SetName('h_tmp_rebinned_%d'%(i))
        h_tmp_rebinned.Rebin(5)
        toy_data_rebinned = ROOT.RooDataHist('h_tmp_rebinned_%d'%(i),'',ROOT.RooArgList(f.obsVar),h_tmp_rebinned,1.)
        bins = toy_data_rebinned.numEntries()
        chi2 = GetChiSquare_ForSpuriousSignal(f.frame,toy_data_rebinned,f.function,f.ndof)
        #ROOT.gROOT.ProcessLine('delete h_tmp_rebinned')
        pvalue_chi2 = ROOT.TMath.Prob(chi2*(bins-1-f.ndof),bins-1-f.ndof)
        h.Fill(pvalue_chi2)
        c2.Fill(chi2)
        #print 'chi2: %2.6f p-value: %2.6f'%(chi2,pvalue_chi2)

#         c = ROOT.TCanvas()
#         f.af2hist_not_rebinned.Draw()
#         h_tmp.Draw('sames')
#         raw_input('pause')

    print 'f.chisquare: %2.6f f.pvalue_chi2: %2.6f'%(f.chisquare,f.pvalue_chi2)

    print 'h.FindBin(f.pvalue_chi2)',h.FindBin(f.pvalue_chi2)
    #pchi2_toys = h.Integral(h.FindBin(f.pvalue_chi2),10000000)/float(h.Integral(-1,100000000))
    pchi2_toys = h.Integral(h.FindBin(0.008),10000000)/float(h.Integral(-1,100000000))
    print 'chi toys: %2.6f'%(pchi2_toys)
    
    c = ROOT.TCanvas()
    #h_tmp.Draw()
    #f.af2hist_not_rebinned.Draw('sames')
    h.Rebin(100)
    h.Draw()
    c.Print('%s/ChiSquareToys.pdf'%(outdir))
    
    #raw_input('pause')
    return 

##################################################################################
def GetChiSquare(frame,obsVar,f,data,ndof) :
    data.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.Range("all"))
    f.plotOn(frame,ROOT.RooFit.Range("lower"),ROOT.RooFit.NormRange("lower"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))

#     chi2_lower = frame.chiSquare(1+ndof)
#     f.plotOn(frame,ROOT.RooFit.Range("upper"),ROOT.RooFit.NormRange("upper"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))
#     chi2_upper = frame.chiSquare(1+ndof)
#     chi2 = (chi2_lower * (15-1-ndof) + chi2_upper * (30-1-ndof)) / float(45-1-ndof)

    f.plotOn(frame,ROOT.RooFit.Range("all"),ROOT.RooFit.NormRange("all"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))
    chi2 = frame.chiSquare(ndof+1)

    return chi2

##################################################################################
def LinkFunctionsForFtest(functions) :
    links = {
        'Exponential':'ExpPoly2',
        'ExpPoly2':'ExpPoly3',
        'ExpPoly3':'ExpPoly4',
        'Pow':'Pow2',
        'Bernstein_3':'Bernstein_4',
        'Bernstein_4':'Bernstein_5',
        }
    for f1 in functions :
        for f2 in functions :
            if f2.name == links[f1.name] :
                print 'linking %s as F to %s'%(f2.name,f1.name)
                f1.ftest_function = f2

    return

##################################################################################
def ToyFtest(function,function2) :
    #
    # Throw toys
    #
    chi2_hist = ROOT.TH1F('%s_chi2hist'%(function.name),'%s #chi^{2}'%(function.name),50,0,2)
    chi2_hist_2 = ROOT.TH1F('%s_chi2hist_2'%(function2.name),'%s #chi^{2}'%(function2.name),50,0,2)
    prob_hist = ROOT.TH1F('%s_probhist'%(function.name),'%s prob'%(function.name),50,0,2)
    prob_hist_2 = ROOT.TH1F('%s_probhist_2'%(function2.name),'%s prob'%(function2.name),50,0,2)
    ftest_hist = ROOT.TH1F('%s_ftest_prob'%(function2.name),'ftest_prob',50,0,2)
    fisher_dist = ROOT.TH1F('%s_fisher_dist'%(function.name),'fisher_dist',50,0,20)
    fisher_func = ROOT.TH1F('%s_fisher_func'%(function.name),'fisher_func',5000,0,20)
    #function.workspace.var('nBkg').setVal(function.workspace.var('nBkg').getVal()*100)

    for i in range(2000) :
        if not i%100 : print 'Ftest:',i
        function.obsVar.setBins(function.datasb_rebinned.numEntries())
        #print function.datasb_rebinned.numEntries()
        toy_data = function.function_ext.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.Extended(),ROOT.RooFit.Name("tmp_ftest_toy_%d_%s"%(i,function.name)))
        #toy_data = function2.function_ext.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.Extended(),ROOT.RooFit.Name("tmp_ftest_toy_%d_%s"%(i,function.name)))
        initial_state = snapshot(function)
        #function.function_ext.fitTo(toy_data,ROOT.RooFit.Warnings(False),ROOT.RooFit.PrintLevel(-1),ROOT.RooFit.Range("lower,upper"),*args_datalimit)
        ROOT.chi2FitTo_KB(function.function_ext,toy_data)
        reset_to_snapshot(function,initial_state)
        chi2 = GetChiSquare(function.frame,function.obsVar,function.function_ext,toy_data,function.ndof)
        #function2.function_ext.fitTo(toy_data,ROOT.RooFit.Warnings(False),ROOT.RooFit.PrintLevel(-1),ROOT.RooFit.Range("lower,upper"),*args_datalimit)
        ROOT.chi2FitTo_KB(function2.function_ext,toy_data)
        chi2_2 = GetChiSquare(function.frame,function2.obsVar,function2.function_ext,toy_data,function2.ndof)

        ndof_bins = 55-1-function.ndof
        ndof_bins_2 = 55-1-function2.ndof
        pvalue_chi2_sb = ROOT.TMath.Prob(chi2*(ndof_bins),ndof_bins)
        pvalue_chi2_sb_2 = ROOT.TMath.Prob(chi2_2*(ndof_bins_2),ndof_bins_2)
        #chi2_hist.Fill(chi2)
        chi2_hist.Fill(chi2)
        chi2_hist_2.Fill(chi2_2)
        prob_hist.Fill(pvalue_chi2_sb)
        prob_hist_2.Fill(pvalue_chi2_sb_2)
        ftest = (chi2*(ndof_bins) - chi2_2*(ndof_bins_2))/ float( chi2_2 )
        fisher_dist.Fill(ftest)
        #p_ftest = 1.0 - ROOT.TMath.FDistI(ftest,1,ndof_bins_2)

        # This one looked ok...
        #p_ftest = 1.0 - ROOT.TMath.FDistI(ftest,ndof_bins,ndof_bins_2)

        #p_ftest = 1.0 - ROOT.TMath.FDistI(ftest,1+function.ndof,1+function2.ndof) # closer
        #p_ftest = 1.0 - ROOT.TMath.FDistI(ftest,function.ndof,function2.ndof) # closer
        ftest_hist.Fill(p_ftest)

#         if i == 1 :
#             c_toy = ROOT.TCanvas('%s'%(i),'asdf',600,500)
#             function.frame = function.obsVar.frame()
#             function.datasb_rebinned.plotOn(function.frame)
#             toy_data.plotOn(function.frame,ROOT.RooFit.MarkerColor(ROOT.kRed))
#             function.function_ext.plotOn(function.frame,ROOT.RooFit.Range("lower"),ROOT.RooFit.NormRange("lower"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))
#             function2.function_ext.plotOn(function.frame,ROOT.RooFit.Range("lower"),ROOT.RooFit.NormRange("lower"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))
#             function.frame.Draw()


    c = ROOT.TCanvas('c%02d_ftest_toy_%s'%(function.category,function.name),"toy study results, %s"%(function.name),600,500)
    chi2_hist.Draw("E1")
    chi2_hist_2.SetLineColor(ROOT.kRed+1);    chi2_hist_2.SetMarkerColor(ROOT.kRed+1)
    chi2_hist_2.Draw("sames pE1")

    prob_hist  .SetLineColor(ROOT.kGreen+1);    prob_hist  .SetMarkerColor(ROOT.kGreen+1)
    prob_hist  .Draw("sames pE1")
    prob_hist_2.SetLineColor(ROOT.kOrange+1);    prob_hist_2.SetMarkerColor(ROOT.kOrange+1)
    prob_hist_2.Draw("sames pE1")
    ftest_hist.SetLineColor(ROOT.kAzure+2);    ftest_hist.SetMarkerColor(ROOT.kAzure+2)
    ftest_hist.Draw("sames pE1")
    plotfunc.AutoFixAxes(c)
    plotfunc.MakeLegend(c)

    d = ROOT.TCanvas('c%02d_fisherdist_%s'%(function.category,function.name),"toy study results, %s"%(function.name),600,500)
    fdist2 = ROOT.TF1('1+npar',"TMath::FDist(x,1,%d)*[0]"%(ndof_bins_2),0.1,20)
    fdist2.SetTitle(fdist2.GetName())
    fdist2.SetParameter(0,0.4)

    for i in range(fisher_func.GetNbinsX()) :
        fisher_func.SetBinContent(i+1,fdist2.Eval(fisher_func.GetBinCenter(i+1)))
        fisher_func.SetBinError(i+1,0)
    fisher_func.Rebin(100)
    

    fisher_dist.DrawNormalized("E1")
    fisher_func.SetMarkerColor(ROOT.kOrange+1)
    fisher_func.SetLineColor(ROOT.kOrange+1)
    fisher_func.DrawNormalized("E1sames")

    fdist2.SetLineColor(ROOT.kRed+1)
    fdist2.Draw("lsames")
    plotfunc.MakeLegend(d)
    plotfunc.AutoFixAxes(d)
    
    raw_input('pause')
    return

