#!/usr/bin/env python

import ROOT
import math
import PlotFunctions as plotfunc
import PyAnalysisPlotting as anaplot
import TAxisFunctions as taxisfunc
plotfunc.SetupStyle()
import Tools
import ChiSquareTools
import FunctionsModule
import os

ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
ROOT.RooMsgService.instance().setSilentMode(True)

def main_singleCategory(options,args) :

    if options.category in [30,31,19] :
        print 'Error! Too few AF2 stats. Not going to do it.'
        return

    cans = []

    options.outdir = ''

    if options.functions :
        flist = options.functions.split(',')
        options.outdir += '_'.join(flist)

    elif options.family == 'official' :
        #flist = ['Exponential','ExpPoly2','ExpPoly3','Bern4','Bern5','Pow','Pow2','Laurent0','Laurent1','Laurent2']
        flist = ['Exponential','ExpPoly2','Bern4','Bern5','Pow','Pow2','Laurent1','Laurent2']
        options.outdir += 'official_functions'

    elif options.family == 'selected' :
        flist = [Tools.selected[Tools.categories[options.category]]]
        options.outdir += 'selected_functions'

    elif options.family == 'ftest' :
        flist = ChiSquareTools.ftest[Tools.categories[options.category]]
        options.outdir += 'ftest_functions'

    elif options.family == 'ExpPoly' :
        flist = ['Exponential'] + list('ExpPoly%d'%(d) for d in range(2,4))
        options.outdir += 'exppoly_family'

    elif options.family == 'Laurent' :
        flist = list('Laurent%d'%(d) for d in range(0,3))
        options.outdir += 'Laurent_family'

    elif options.family == 'PolyOverX4' :
        flist = ['1/x^4'] + list('poly%d/x^4'%(d) for d in range(1,6))
        options.outdir += 'PolyOverX4_family'

    elif options.family == 'Bernstein' :
        flist = list('Bern%d'%(d) for d in range(4,6))
        options.outdir += 'Bern_family'

    elif options.family == 'PowerSum' :
        flist = ['Pow','Pow2']
        options.outdir += 'PowerSum_family'

    else :
        flist = [
            'Exponential', # bad
            'ExpPoly2',
            'ExpPoly3',
            ]
        options.outdir += '_'.join(flist)

    options.outdir += '_c%02d_%s'%(options.category,Tools.categories[options.category])

    functions = []
    FunctionsModule.PopulateFunctionList(functions,flist)
    ChiSquareTools.LinkFunctionsForFtest(functions)
    if len(functions) == 0 :
        print 'Error! no functions loaded!'
        import sys; sys.exit()

    for f in functions :
        f.SetCategory(options.category)
        f.SetFileName(options.file)
        f.Initialize()

#     print functions[0].smsignalyield.getVal()
#     return


    rebin = 5
    if options.category > 16 :
        rebin = 1
    functions[0].datahist.Rebin(rebin)
    for i,f in enumerate(functions) :
        if i :
            f.datahist.Rebin(rebin)
        f.datasb_rebinned = ROOT.RooDataHist('data_real_rebinned','',ROOT.RooArgList(f.obsVar),f.datahist,1.)
        
    if not os.path.exists(options.outdir) :
        os.makedirs(options.outdir)

    ftest_text = ''

    cans.append(plotfunc.RatioCanvas("Ftests_%02d_%s"%(options.category,Tools.categories[options.category]),"main plot",600,500))
    functions[0].datahist.SetBinErrorOption(ROOT.TH1.kPoisson)
    plotfunc.AddHistogram(cans[-1],functions[0].datahist)
    ##
    ## Ftests to sideband
    ##
    for f in functions :
        if not hasattr(f,'ftest_function') :
            continue

        nbins_blind = int(f.datasb_rebinned.numEntries()*9/11.)
        print 'nbins:',nbins_blind
        # ndof_bins = nbins_blind-f.ndof-1
        # ndof_bins_2 = nbins_blind-f.ftest_function.ndof-1
        ndof_bins = nbins_blind-f.ndof
        ndof_bins_2 = nbins_blind-f.ftest_function.ndof

        #
        # Fitting data sidebands - first function
        #
        print 'Fitting data sidebands'
        print f.PrintParameters()
        ChiSquareTools.FitForChi2_DataSidebands(f)
        print f.PrintParameters()
        print 'Fitting data sidebands done'
        ftest_text += f.PrintParameters()+'\n'
        chi2 = ChiSquareTools.GetChiSquare(f.frame,f.obsVar,f.function_ext,f.datasb_rebinned,ndof_bins)
        pvalue_chi2 = ROOT.TMath.Prob(chi2*(ndof_bins),ndof_bins)

        #
        # Plotting stuff - first function
        #
        Tools.ClearRooPlot(f.frame)
        ChiSquareTools.NormalizeToSideband(f)
        f.datasb_rebinned.plotOn(f.frame,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
        print 'about to plot'
        #f.workspace.var('a1').setVal(-1.6)
        print f.PrintParameters()
        f.function_ext.plotOn(f.frame,*(Tools.plotOptions_sb_all))
        print f.PrintParameters()
        print 'about to plot done'
        curve = f.frame.getCurve(); curve.SetMarkerSize(0); curve.SetLineWidth(2)
        curve.SetTitle('%s, p(#chi^{2}) = %2.1f%%'%(f.name,pvalue_chi2*100.))
        curve.SetLineColor(ROOT.kRed+1); curve.SetFillColor(0)
        pull = f.frame.pullHist(); pull.SetMarkerSize(0.7); pull.SetLineColor(ROOT.kRed+1);
        pull.SetMarkerColor(ROOT.kRed+1)
        plotfunc.AddRatioManual(cans[-1],curve,pull,drawopt1='l',drawopt2='p')


        #
        # Fitting data sidebands - first function
        #
        print 'Fitting data sidebands (other function)'
        print f.ftest_function.PrintParameters()        
        ChiSquareTools.FitForChi2_DataSidebands(f.ftest_function)
        print f.ftest_function.PrintParameters()        
        print 'Fitting data sidebands (other function) done'
        ftest_text += f.ftest_function.PrintParameters()+'\n'
        chi2_2 = ChiSquareTools.GetChiSquare(f.frame,f.obsVar,f.ftest_function.function_ext,f.datasb_rebinned,ndof_bins_2)
        pvalue_chi2_2 = ROOT.TMath.Prob(chi2_2*(ndof_bins_2),ndof_bins_2)

        #
        # Plotting stuff - other function
        #
        Tools.ClearRooPlot(f.frame)
        ChiSquareTools.NormalizeToSideband(f.ftest_function)
        f.datasb_rebinned.plotOn(f.frame)
        f.ftest_function.function_ext.plotOn(f.frame,*(Tools.plotOptions_sb_all))
        curve = f.frame.getCurve(); curve.SetMarkerSize(0); curve.SetLineWidth(2)
        curve.SetTitle('%s, p(#chi^{2}) = %2.1f%%'%(f.ftest_function.name,pvalue_chi2_2*100.))
        curve.SetLineColor(ROOT.kAzure-2); curve.SetFillColor(0)
        pull = f.frame.pullHist(); pull.SetMarkerSize(0.7); pull.SetLineColor(ROOT.kAzure-2);
        pull.SetMarkerColor(ROOT.kAzure-2)
        plotfunc.AddRatioManual(cans[-1],curve,pull,drawopt1='l',drawopt2='p')

        ftest = ChiSquareTools.GetF(chi2,chi2_2,ndof_bins,ndof_bins_2)

        ftest_text += 'chi2/ndf: %2.5f\n'%(chi2)
        ftest_text += 'chi2_2/ndf: %2.5f\n'%(chi2_2)
        ftest_text += 'chi2: %2.5f\n'%(chi2*ndof_bins)
        ftest_text += 'chi2_2: %2.5f\n'%(chi2_2*ndof_bins_2)
        ftest_text += 'ftest: %2.5f\n'%(ftest)
        #p_ftest = 1.0 - ROOT.TMath.FDistI(ftest,1,ndof_bins_2)
        p_ftest = 1.0 - ROOT.TMath.FDistI(ftest,ndof_bins-ndof_bins_2,ndof_bins_2)
        ftest_text += 'p_ftest: %2.5f\n'%(p_ftest)
        
        #
        # Throw Toys
        #
        fisher_dist = ChiSquareTools.ToyFtest(f,f.ftest_function,ftest,options.outdir,options.ntoys)

        if fisher_dist.Integral(0,100000) :
            ftest_text += 'p_ftest_toys: %2.5f\n'%(fisher_dist.Integral(fisher_dist.FindBin(ftest),100000)/float(fisher_dist.Integral(0,100000)))

#         chi2_lowerSideBand = ROOT.RooChi2Var("chi2_low","chi2_low",f.function_ext,f.data_realdata,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.Range("lower"));
#         chi2_upperSideBand = ROOT.RooChi2Var("chi2_upp","chi2_upp",f.function_ext,f.data_realdata,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.Range("upper"));
        # chi2_all           = ROOT.RooChi2Var("chi2_all","chi2_all",f.function_ext,f.data_realdata,ROOT.RooFit.Range("lower,upper"));
        # chi2_lowerSideBand = ROOT.RooChi2Var("chi2_low","chi2_low",f.function_ext,f.data_realdata,ROOT.RooFit.Range("lower"));
        # chi2_upperSideBand = ROOT.RooChi2Var("chi2_upp","chi2_upp",f.function_ext,f.data_realdata,ROOT.RooFit.Range("upper"));
        # print 'chi2_all          .getValV()',chi2_all.getValV()
        # print 'chi2_lowerSideBand.getValV()',chi2_lowerSideBand.getValV()
        # print 'chi2_upperSideBand.getValV()',chi2_upperSideBand.getValV()
        # print 'total:',(chi2_lowerSideBand.getValV()+chi2_upperSideBand.getValV()) / float(f.bins-1-f.ndof)

        # Get the chi2 from the background-only fit
        # print 'f.frame.chiSquare(1+f.ndof-10)',f.frame.chiSquare(1+f.ndof)*(f.bins-1-f.ndof)
        # f.chisquare_sb = f.frame.chiSquare(1+f.ndof-10) # n-1 bins MINUS 10 BINS
        # f.pvalue_chi2_sb = ROOT.TMath.Prob(f.chisquare_sb*(f.bins-1-f.ndof-10),f.bins-1-f.ndof-10)
        # print 'chisquare:',f.chisquare_sb,f.pvalue_chi2_sb

        continue

        curve = f.frame.getCurve(); curve.SetMarkerSize(0); curve.SetLineWidth(1)
        curve.SetTitle(f.name)
        curve.SetLineWidth(2)
#         resid = f.frame.residHist(); resid.SetMarkerSize(0)
#         plotfunc.AddRatioManual(cans[-1],curve,resid,drawopt1='l',drawopt2='l')
        pull = f.frame.pullHist(); pull.SetMarkerSize(0.7)

        # for special
        if options.family == 'selected' :
            color = {
                'Pow'         : ROOT.kBlack+0,
                'Exponential' : ROOT.kRed+1,
                'ExpPoly2'    : ROOT.kBlue+1,
                'Bern3'       : ROOT.kGreen+1,
                'Bern4'       : ROOT.kMagenta+1,
                'Bern5'       : ROOT.kOrange+1,
                }.get(f.name)
            pull.SetMarkerColor(color); pull.SetLineColor(color);
            curve.SetLineColor(color); curve.SetFillColor(0)
        
        plotfunc.AddRatioManual(cans[-1],curve,pull,drawopt1='l',drawopt2='p')
    
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','entries','pull')
    the_text = [plotfunc.GetAtlasInternalText()
                ,plotfunc.GetSqrtsText(13)+', '+plotfunc.GetLuminosityText(36.1)
                ,Tools.CategoryNames[Tools.categories[options.category]]
                ,'1-p(F_{%d%d}) = %2.1f%%'%(functions[0].ndof,functions[0].ftest_function.ndof,p_ftest*100)
                ]
    plotfunc.DrawText(cans[-1],the_text,0.19,0.63,0.59,0.91,totalentries=4)
    plotfunc.MakeLegend(cans[-1]       ,0.57,0.63,0.90,0.91,totalentries=4)
    plotfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),-4,4)
    plotfunc.SetXaxisRanges(cans[-1],functions[0].lower_range,functions[0].upper_range)
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(cans[-1]),forcemin=0.001)
    
    print ftest_text
    a = open('%s/ftests.txt'%(options.outdir),'w')
    a.write(options.file+'\n')
    a.write(ftest_text+'\n')
    a.close()

    for can in cans :
        plotfunc.FormatCanvasAxes(can)

    anaplot.UpdateCanvases(cans,options)
    if not options.batch :
        raw_input('Press enter to exit')
    anaplot.doSaving(options,cans)

    return

if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--category','--c',type='string',default='',dest='category',help='category (0-30something)')
    p.add_option('--family',type='string',default='ftest',dest='family',help='families: official,selected,ExpPoly,Laurent,PolyOverX4,Bernstein,PowerSum')
    p.add_option('--functions','--f',type='string',default='',dest='functions',help='functions Exponential,ExpPoly2,blah')
    p.add_option('--batch',action='store_true',default=False,dest='batch',help='run in batch mode')
    p.add_option('--save',action='store_true',default=False,dest='save',help='save cans to pdf')

    p.add_option('--file',type='string',default='',dest='file',help='file (in which the histogram is contained)')
    p.add_option('--ntoys',type='int',default=0,dest='ntoys',help='Number of f-test toys')

    options,args = p.parse_args()

    ROOT.gROOT.SetBatch(options.batch)

    if not options.file :
        print 'Error! Specify file with histograms. Exiting.'; import sys; sys.exit()

    if options.category == 'all' :
        for i in range(0,17) :
            options.category = int(i)
            main_singleCategory(options,args)
    else :
        options.category = int(options.category)
        main_singleCategory(options,args)


