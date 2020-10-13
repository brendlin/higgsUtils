
ftest = {
    'M17_ggH_0J_Cen'        :['ExpPoly2','ExpPoly3'],
    'M17_ggH_0J_Fwd'        :['ExpPoly2','ExpPoly3'],
    'M17_ggH_1J_LOW'        :['ExpPoly2','ExpPoly3'],
    'M17_ggH_1J_MED'        :['ExpPoly2','ExpPoly3'],
    'M17_ggH_1J_HIGH'       :['Pow','Pow2'],
    'M17_ggH_1J_BSM'        :['Exponential','ExpPoly2'],
    'M17_ggH_2J_LOW'        :['ExpPoly2','ExpPoly3'],
    'M17_ggH_2J_MED'        :['ExpPoly2','ExpPoly3'],
    'M17_ggH_2J_HIGH'       :['Pow','Pow2'],
    'M17_ggH_2J_BSM'        :['Pow','Pow2'],
    'M17_VBF_HjjLOW_loose'  :['Exponential','ExpPoly2'],
    'M17_VBF_HjjLOW_tight'  :['Exponential','ExpPoly2'],
    'M17_VBF_HjjHIGH_loose' :['Exponential','ExpPoly2'],
    'M17_VBF_HjjHIGH_tight' :['Exponential','ExpPoly2'],
    'M17_VHhad_loose'       :['Exponential','ExpPoly2'],
    'M17_VHhad_tight'       :['Exponential','ExpPoly2'],
    'M17_qqH_BSM'           :['Exponential','ExpPoly2'],
    'M17_VHMET_LOW'         :['Exponential','ExpPoly2'],
    'M17_VHMET_HIGH'        :['Exponential','ExpPoly2'],
    'M17_VHMET_BSM'         :['Exponential','ExpPoly2'],
    'M17_VHlep_LOW'         :['Pow','Pow2'],
    'M17_VHlep_HIGH'        :['Exponential','ExpPoly2'],
    'M17_VHdilep_LOW'       :['Pow','Pow2'],
    'M17_VHdilep_HIGH'      :['None'],
    'M17_tH_Had_4j2b'       :['Pow','Pow2'],
    'M17_tH_Had_4j1b'       :['Pow','Pow2'],
    'M17_ttH_Had_BDT4'      :['Exponential','ExpPoly2'],
    'M17_ttH_Had_BDT3'      :['Exponential','ExpPoly2'],
    'M17_ttH_Had_BDT2'      :['Exponential','ExpPoly2'],
    'M17_ttH_Had_BDT1'      :['Exponential','ExpPoly2'],
    'M17_ttH_Lep'           :['Pow','Pow2'],
    'M17_tH_lep_1fwd'       :['Pow','Pow2'],
    'M17_tH_lep_0fwd'       :['Pow','Pow2'],
    'GGF_DIMUON'               :['ExpPoly2','ExpPoly3'],
    'GGF_RESOLVED_DIELECTRON'  :['Pow','Pow2'],
    'GGF_MERGED_DIELECTRON'    :['ExpPoly2','ExpPoly3'],
    'VBF_DIMUON'               :['Pow','Pow2'],
    'VBF_RESOLVED_DIELECTRON'  :['Exponential','ExpPoly2'],
    'VBF_MERGED_DIELECTRON'    :['Pow','Pow2'],
    'HIPTT_DIMUON'             :['Pow','Pow2'],
    'HIPTT_RESOLVED_DIELECTRON':['Pow','Pow2'],
    'HIPTT_MERGED_DIELECTRON'  :['Pow','Pow2'],
}

##################################################################################
def FitForChi2_DataSidebands(f,useMaxLikelihood=True) :
    import ROOT

    #ROOT.gROOT.ProcessLine('.L Extras.h')
    #ROOT.gROOT.LoadMacro("rootlogon.C+")
    #rootlogon()
    #print list(ROOT.gROOT.GetListOfFunctions())
    #ROOT.ListExtras()

#     f.obsVar.setRange("lower",105,120) ;
#     f.obsVar.setRange("upper",130,160) ;

    # initial state
    f.workspace.var('nBkg_ext').setVal(f.datasb_rebinned.sumEntries())
    f.workspace.var('nBkg_ext').setMax(f.datasb_rebinned.sumEntries()*1.5)
    f.obsVar.setBins(f.datasb_rebinned.numEntries())

    if useMaxLikelihood :
        f.function_ext.fitTo(f.datasb_rebinned
                             ,ROOT.RooFit.Extended()
                             #,ROOT.RooFit.Warnings(False)
                             ,ROOT.RooFit.Range("lower,upper")
                             #,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson)
                             ,ROOT.RooFit.Minimizer('Minuit2','migrad')
                             ,ROOT.RooFit.Strategy(2)
                             ,ROOT.RooFit.NumCPU(4)
                             )
    else : # chi2
        if not getattr(ROOT,'chi2FitTo_KB',None) :
            ROOT.gROOT.LoadMacro("Extras.h+")
        ROOT.chi2FitTo_KB(f.function_ext,f.datasb_rebinned)

    return

##################################################################################
def NormalizeToSideband(f) :
    import ROOT

    tmp_data = f.function_ext.generateBinned(ROOT.RooArgSet(f.obsVar),ROOT.RooFit.ExpectedData(),ROOT.RooFit.Name("tmp_ftest_tmp_%s"%(f.name)))

    tmp_integral = float(tmp_data.sumEntries("120>m_yy || m_yy>130"))
    correction = 1.
    norm = f.datasb_rebinned.sumEntries()*correction/float(tmp_integral)

    # print 'correction:',correction
    # print 'tmp_integral:',tmp_integral
    # print 'Normalization is',norm

    f.workspace.var('nBkg_ext').setVal(f.workspace.var('nBkg_ext').getVal()*norm)

    # tmp_data_2 = f.function_ext.generateBinned(ROOT.RooArgSet(f.obsVar),ROOT.RooFit.ExpectedData(),ROOT.RooFit.Name("tmp_ftest_tmp_%s"%(f.name)))
    # c = ROOT.TCanvas()
    # ClearRooPlot(f.frame)
    # f.datasb_rebinned.plotOn(f.frame)
    # tmp_data_2.plotOn(f.frame)
    # f.function_ext.plotOn(f.frame,*(plotOptions_sb))
    # f.frame.Draw()
    # raw_input('asdf')

    return

##################################################################################
def GetChiSquare_ForSpuriousSignal(frame,af2,function,ndof) :
    import Tools
    Tools.ClearRooPlot(frame)
    af2.plotOn(frame)
    function.plotOn(frame)
    # Get the chi2 from the background-only fit
    chisquare = frame.chiSquare(1+ndof) # n-1 bins
    return chisquare

##################################################################################
def ChiSquareToys_ForSpuriousSignal(f,outdir) :
    import Tools
    Tools.ClearRooPlot(f.frame)
    f.obsVar.setBins(f.af2_rebinned.numEntries())
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
def GetChiSquare(frame,obsVar,f,data,ndof_bins,i=0) :
    import ROOT
    # data.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.Range("all"))
    # f.plotOn(frame,ROOT.RooFit.Range("lower"),ROOT.RooFit.NormRange("lower"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))

#     chi2_lower = frame.chiSquare(1+ndof)
#     f.plotOn(frame,ROOT.RooFit.Range("upper"),ROOT.RooFit.NormRange("upper"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))
#     chi2_upper = frame.chiSquare(1+ndof)
#     chi2 = (chi2_lower * (15-1-ndof) + chi2_upper * (30-1-ndof)) / float(45-1-ndof)

    # f.plotOn(frame,ROOT.RooFit.Range("all"),ROOT.RooFit.NormRange("all"),ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative))
    # chi2 = frame.chiSquare(ndof+1)

    chi2_lowerSideBand = ROOT.RooChi2Var("chi2_low_%s_%d"%(f.GetName(),i),"chi2_low", f, data, ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson), ROOT.RooFit.Range("lower"))
    chi2_upperSideBand = ROOT.RooChi2Var("chi2_up_%s_%d"%(f.GetName(),i),"chi2_up", f, data, ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson), ROOT.RooFit.Range("upper"))
    chi2 = chi2_lowerSideBand.getValV() + chi2_upperSideBand.getValV()

    return chi2/float(ndof_bins)

##################################################################################
def GetF(chi2,chi2_2,ndof_bins,ndof_bins_2,prob_hist=0,prob_hist_2=0) :
    import ROOT

    pvalue_chi2_sb = ROOT.TMath.Prob(chi2*(ndof_bins),ndof_bins)
    pvalue_chi2_sb_2 = ROOT.TMath.Prob(chi2_2*(ndof_bins_2),ndof_bins_2)
    if prob_hist :
        prob_hist.Fill(pvalue_chi2_sb)
    if prob_hist_2 :
        prob_hist_2.Fill(pvalue_chi2_sb_2)
    if chi2_2 == 0 :
        return 0
    ftest = (chi2*(ndof_bins) - chi2_2*(ndof_bins_2))/ float( chi2_2 )
    if ftest < 0 :
        ftest = 0
    return ftest

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
            if f2.name == links.get(f1.name,'nothing') :
                print 'linking %s as F to %s'%(f2.name,f1.name)
                f1.ftest_function = f2

    return

##################################################################################
def ToyFtest(function,function2,the_ftest,directory,ntoys,useMaxLikelihood=True) :
    import ROOT
    import Tools
    import PlotFunctions as plotfunc

    tmp_data_2 = function.function_ext.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.ExpectedData(),ROOT.RooFit.Name("tmp_ftest_tmp_%s"%(function.name)))
    c = ROOT.TCanvas()
    Tools.ClearRooPlot(function.frame)
    function.datasb_rebinned.plotOn(function.frame)
    tmp_data_2.plotOn(function.frame)
    function.frame.Draw()
    #raw_input('asdf')

    #
    # Throw toys
    #
    chi2_hist   = ROOT.TH1F('%s_chi2hist'%(function.name),'%s #chi^{2}'%(function.name),50,0,2)
    chi2_hist_2 = ROOT.TH1F('%s_chi2hist_2'%(function2.name),'%s #chi^{2}'%(function2.name),50,0,2)
    prob_hist   = ROOT.TH1F('%s_probhist'%(function.name),'%s p(#chi^{2})'%(function.name),50,0,2)
    prob_hist_2 = ROOT.TH1F('%s_probhist_2'%(function2.name),'%s p(#chi^{2})'%(function2.name),50,0,2)
    ftest_hist  = ROOT.TH1F('%s_ftest_prob'%(function2.name),'1 - p(F)',50,0,2)
    fisher_dist = ROOT.TH1F('%s_fisher_dist'%(function.name),'toys',5000,0,20)
    fisher_func = ROOT.TH1F('%02d_%s_fisher_func'%(function.category,function.name),'F distribution',50000,0,20)
    #function.workspace.var('nBkg').setVal(function.workspace.var('nBkg').getVal()*100)

    nbins_blind = int(function.datasb_rebinned.numEntries()*9/11.)

    ndof_bins = nbins_blind-function.ndof-1
    ndof_bins_2 = nbins_blind-function2.ndof-1

    # print 'Summary:'
    # print 'function.ndof',function.ndof
    # print 'function2.ndof',function2.ndof
    # print 'ndof_bins',ndof_bins
    # print 'ndof_bins_2',ndof_bins_2

#     return fisher_dist

    if not getattr(ROOT,'ExecuteToy',None) :
        ROOT.gROOT.LoadMacro('RooFitFunctions.h')

    for i in range(ntoys) :
        if not i%100 : print 'Ftest %d toys in progress: %d'%(ntoys,i)
        #if not i%1 : print 'Ftest %d toys in progress: %d'%(ntoys,i)

        res = list(ROOT.ExecuteToy(function.function_ext,function2.function_ext,function.obsVar,ndof_bins,ndof_bins_2))
        #print res; import sys; sys.exit();
        chi2 = res[0]
        chi2_2 = res[1]

        ftest = GetF(chi2,chi2_2,ndof_bins,ndof_bins_2,prob_hist,prob_hist_2)

        chi2_hist.Fill(chi2)
        chi2_hist_2.Fill(chi2_2)
        fisher_dist.Fill(ftest)
        p_ftest = 1.0 - ROOT.TMath.FDistI(ftest,ndof_bins-ndof_bins_2,ndof_bins_2)
        ftest_hist.Fill(p_ftest)


    c = ROOT.TCanvas('c%02d_ftest_toy_%s'%(function.category,function.name),"toy study results, %s"%(function.name),600,500)
    chi2_hist.DrawNormalized("E1")
    chi2_hist_2.SetLineColor(ROOT.kRed+1);    chi2_hist_2.SetMarkerColor(ROOT.kRed+1)
    chi2_hist_2.DrawNormalized("sames pE1")

    prob_hist  .SetLineColor(ROOT.kGreen+1);    prob_hist  .SetMarkerColor(ROOT.kGreen+1)
    prob_hist  .DrawNormalized("sames pE1")
    prob_hist_2.SetLineColor(ROOT.kOrange+1);    prob_hist_2.SetMarkerColor(ROOT.kOrange+1)
    prob_hist_2.DrawNormalized("sames pE1")
    ftest_hist.SetLineColor(ROOT.kAzure+2);    ftest_hist.SetMarkerColor(ROOT.kAzure+2)
    ftest_hist.DrawNormalized("sames pE1")
    plotfunc.MakeLegend(c,0.71,0.72,0.81,0.93)
    plotfunc.AutoFixAxes(c)
    plotfunc.AutoFixYaxis(c,minzero=True)

    c.Print('%s/ChiSquares_%s.pdf'%(directory,c.GetName()))
    c.Print('%s/ChiSquares_%s.eps'%(directory,c.GetName()))
    c.Print('%s/ChiSquares_%s.C'%(directory,c.GetName()))


    d = ROOT.TCanvas('c%02d_fisherdist_%s'%(function.category,function.name),"toy study results, %s"%(function.name),600,500)
    d.SetLogy()
    fdist2 = ROOT.TF1('1+npar',"TMath::FDist(x,%d,%d)*[0]"%(ndof_bins-ndof_bins_2,ndof_bins_2),0.00001,20)
    fdist2.SetTitle(fdist2.GetName())
    fdist2.SetParameter(0,0.4)

    for i in range(fisher_func.GetNbinsX()) :
        fisher_func.SetBinContent(i+1,fdist2.Eval(fisher_func.GetBinCenter(i+1)))
        fisher_func.SetBinError(i+1,0)
    fisher_func.Rebin(500)


    fisher_dist_clone = fisher_dist.Clone()
    fisher_dist_clone.SetName(fisher_dist.GetName()+'_clone')
    fisher_dist_clone.Rebin(50)
    fisher_dist_clone.DrawNormalized("E1")
    fisher_func.SetMarkerColor(ROOT.kOrange+1)
    fisher_func.SetLineColor(ROOT.kOrange+1)
    fisher_func.DrawNormalized("E1sames")


    # fdist2.SetLineColor(ROOT.kRed+1)
    # fdist2.Draw("lsames")
    from array import array
    y = array('d',[fisher_func.GetBinContent(fisher_func.GetNbinsX())/fisher_func.Integral(),
                   fisher_func.GetBinContent(fisher_func.FindBin(the_ftest))/fisher_func.Integral()])

    a = ROOT.TGraph(2,array('d',[the_ftest,the_ftest]),y)
    a.SetName('Data sideband')
    a.SetTitle('F for data SB')
    a.SetLineWidth(2); a.SetMarkerColor(ROOT.kRed+1); a.SetLineColor(ROOT.kRed+1); a.SetFillColor(0)
    plotfunc.AddHistogram(d,a,drawopt='l')

    plotfunc.SetAxisLabels(d,'F-test statistic','nToys')
    plotfunc.MakeLegend(d,0.69,0.75,0.83,0.90,option=['p','l','l'])
    plotfunc.AutoFixAxes(d)
    plotfunc.SetXaxisRanges(d,0,12)

    d.Print('%s/FtestToys_%s.pdf'%(directory,d.GetName()))
    d.Print('%s/FtestToys_%s.eps'%(directory,d.GetName()))
    d.Print('%s/FtestToys_%s.C'%(directory,d.GetName()))

    return fisher_dist
