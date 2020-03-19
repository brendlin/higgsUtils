#!/usr/bin/env python

import ROOT
import math
import PlotFunctions as plotfunc
import PyAnalysisPlotting as anaplot
import TAxisFunctions as taxisfunc
plotfunc.SetupStyle()
import Tools
import FunctionsModule
import ChiSquareTools
import os

ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
ROOT.RooMsgService.instance().setSilentMode(True)

def main_singleCategory(options,args) :

    if options.category in [30,31] :
        print 'Error! Too few AF2 stats. Not going to do it.'
        return

    cans = []

    options.outdir = ''

    category_name = None
    category_title = None
    selected = None

    if options.analysis == 'couplings2017' :
        category_name = Tools.categories_couplings2017[options.category]
        category_title = Tools.CategoryNames_couplings2017[category_name]
        selected = Tools.selected_couplings2017[category_name]
    elif options.analysis == 'ysy' :
        category_name = Tools.categories_ysy[options.category]
        category_title = Tools.CategoryNames_ysy[category_name]
        selected = Tools.selected_ysy[category_name]
    else :
        print('Error - do not understand analysis name %s'%(options.analysis))
        import sys; sys.exit()

    if options.functions :
        flist = options.functions.split(',')
        options.outdir += '_'.join(flist)

    elif options.family == 'official' :
        #flist = ['Exponential','ExpPoly2','ExpPoly3','Bern4','Bern5','Pow','Pow2','Laurent0','Laurent1','Laurent2']
        flist = ['Exponential','ExpPoly2','Bern4','Bern5','Pow','Pow2','Laurent1','Laurent2']
        options.outdir += 'official_functions'

    elif options.family == 'selected' :
        flist = [selected]
        options.outdir += 'selected_functions'
        print flist

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

    options.outdir += '_c%02d_%s'%(options.category,category_name)

    functions = []
    FunctionsModule.PopulateFunctionList(functions,flist)
    ChiSquareTools.LinkFunctionsForFtest(functions)
    if len(functions) == 0 :
        print 'Error! no functions loaded!'
        import sys; sys.exit()

    for f in functions :
        f.SetAnalysis(options.analysis)
        f.SetCategory(options.category)
        f.SetFileName(options.file)
        f.SetSignalWS(options.signalws)
        f.Initialize()


    cans.append(ROOT.TCanvas("c%02d_error_summary"%(options.category),"error_summary",600,500))
    ##
    ## Spurious signal Z, Mu
    ##
    syst_hist = ROOT.TH1F('syst_hist','syst (0-bkg)',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        syst_hist.SetBinContent(i+1,Tools.GetSpuriousSignalMu(f,index=i))
        syst_hist.GetXaxis().SetBinLabel(i+1,f.name)
        Tools.GetSpuriousSignalZ(f,index=i)
    plotfunc.AddHistogram(cans[-1],syst_hist,drawopt='hist')

    ## Error on the signal
    error_hist = ROOT.TH1F('error_hist','stat (0-bkg)',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        error_hist.SetBinContent(i+1,Tools.GetDeltaS_Relative(f))
    cans[-1].cd()
    plotfunc.AddHistogram(cans[-1],error_hist,drawopt='hist')

    ## syst + stat
    total_hist = ROOT.TH1F('total_hist','Stat + syst',len(flist),0,len(flist))
    for i in range(total_hist.GetNbinsX()) :
        total_hist.SetBinContent(i+1,math.sqrt(syst_hist.GetBinContent(i+1)**2 + error_hist.GetBinContent(i+1)**2))
    plotfunc.AddHistogram(cans[-1],total_hist,drawopt='hist')

    ## Systematic with injection
    injected_hist = ROOT.TH1F('injected_hist','syst (inject SM)',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        injected_hist.SetBinContent(i+1,Tools.GetSignalBiasMuScan(f,index=i))
    injected_hist.SetLineStyle(2)
    #plotfunc.AddHistogram(cans[-1],injected_hist,drawopt='hist')

    ## Systematic with injection - 125 GeV
#     injected_hist_125 = ROOT.TH1F('injected_hist_125','injection syst 125',len(flist),0,len(flist))
#     for i,f in enumerate(functions) :
#         injected_hist_125.SetBinContent(i+1,Tools.GetInjectedSignalBias(f,125))
#     injected_hist_125.SetLineStyle(2)
#     plotfunc.AddHistogram(cans[-1],injected_hist_125,drawopt='hist')

    ## Error on the signal (in the injection case) - only 125
    error_hist_inj = ROOT.TH1F('error_hist_inj','stat (inject SM)',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        error_hist_inj.SetBinContent(i+1,f.injectionerror_rel) # only 125
    cans[-1].cd()
    error_hist_inj.SetLineStyle(2)
    #plotfunc.AddHistogram(cans[-1],error_hist_inj,drawopt='hist')

    plotfunc.SetColors(cans[-1])
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    #plotfunc.AutoFixAxes(cans[-1],ignorelegend=True)
    taxisfunc.AutoFixYaxis(cans[-1],ignorelegend=True,minzero=True)





    ##
    ## Spurious signal mu canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_spurious_signal_mu"%(options.category),"spurious signal mu",600,500))
    
    functions[0].spurioussignalmucv.Draw('al')
    functions[0].spurioussignalmuup.Draw('l')
    functions[0].spurioussignalmudn.Draw('l')
    for i,f in enumerate(functions[1:]) :
        f.spurioussignalmucv.Draw('l')
        f.spurioussignalmuup.Draw('l')
        f.spurioussignalmudn.Draw('l')
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','S_{spur}/S_{SM}')
    taxisfunc.SetYaxisRanges(cans[-1],-0.5,0.5)
    taxisfunc.SetXaxisRanges(cans[-1],110,160)
    Tools.DrawBox(121,129,-0.1,0.1)




    ##
    ## Stats-limited spurious signal mu canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_spurious_signal_mu_statlim"%(options.category),"spurious signal mu (stat-limited)",600,500))
    functions[0].spurioussignalmucomp.Draw('al')
    for i,f in enumerate(functions[1:]) :
        f.spurioussignalmucomp.Draw('l')
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','S_{spur}/S_{SM}')
    taxisfunc.SetYaxisRanges(cans[-1],-0.5,0.5)
    taxisfunc.SetXaxisRanges(cans[-1],110,160)
    Tools.DrawBox(121,129,-0.1,0.1)





    ##
    ## Spurious signal Z canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_spurious_signal_z"%(options.category),"spurious signal z",600,500))
    functions[0].spurioussignalzcv.Draw('al')
    functions[0].spurioussignalzup.Draw('l')
    functions[0].spurioussignalzdn.Draw('l')
    for i,f in enumerate(functions[1:]) :
        f.spurioussignalzcv.Draw('l')
        f.spurioussignalzup.Draw('l')
        f.spurioussignalzdn.Draw('l')
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','S_{spur}/#Delta S')
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    taxisfunc.SetYaxisRanges(cans[-1],-1.0,1.0)
    taxisfunc.SetXaxisRanges(cans[-1],110,160)
    Tools.DrawBox(121,129,-0.2,0.2)




    ##
    ## Stats-limited spurious signal z canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_spurious_signal_z_statlim"%(options.category),"spurious signal Z (stat-limited)",600,500))
    functions[0].spurioussignalzcomp.Draw('al')
    for i,f in enumerate(functions[1:]) :
        f.spurioussignalzcomp.Draw('l')
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','S_{spur}/S_{SM}')
    taxisfunc.SetYaxisRanges(cans[-1],-0.5,0.5)
    taxisfunc.SetXaxisRanges(cans[-1],110,160)
    Tools.DrawBox(121,129,-0.2,0.2)





    ##
    ## Injected signal bias canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_signal_bias_mu"%(options.category),"signal bias mu",600,500))
    functions[0].signalbiasmucv.Draw('al')
    #functions[0].signalbiasmuup.Draw('l')
    #functions[0].signalbiasmudn.Draw('l')
    for i,f in enumerate(functions[1:]) :
        f.signalbiasmucv.Draw('l')
        #f.signalbiasmuup.Draw('l')
        #f.signalbiasmudn.Draw('l')
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','S_{bias}/#Delta S')
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    taxisfunc.SetYaxisRanges(cans[-1],-0.5,0.5)
    taxisfunc.SetXaxisRanges(cans[-1],110,160)
    Tools.DrawBox(121,129,-0.1,0.1)






    ##
    ## Toy study canvases
    ##
#     for f in functions :
#         cans.append(Tools.ToyInjectedSignalBias(f,functions[0].deltas_relative,inject_signal=True))
#         plotfunc.SetAxisLabels(cans[-1],'S/S_{ref} (signal)','n toys')
#         cans.append(Tools.ToyInjectedSignalBias(f,functions[0].deltas_relative,inject_signal=False))
#         plotfunc.SetAxisLabels(cans[-1],'S/S_{ref} (no signal)','n toys')






    ##
    ## Plot the data and af2 (fit bkg-only just before this.) SpuriousSignal_05_M17_ggH_1J_BSM
    ##
    for f in functions :
        f.function.fitTo(f.data,*(Tools.args_bkgonly))
    cans.append(plotfunc.RatioCanvas("TemplateFit_%02d_%s"%(options.category,category_name),"main plot",600,500))
    functions[0].af2hist.SetMarkerSize(0)

    rebin = 1
    if options.rebin == 'dynamic' :
        print('Dynamically rebinning')
        rebin = Tools.RebinUntilSmallErrors(functions[0].af2hist,0,Tools.lower_range,Tools.upper_range,errormax=0.3)
    else :
        rebin = int(options.rebin)

    functions[0].af2hist.Rebin(rebin)
    binwidth = functions[0].af2hist.GetBinWidth(1)
    bins = int((functions[0].upper_range-functions[0].lower_range)/float(binwidth))
    functions[0].af2hist.SetTitle('#gamma#gamma MC')
    functions[0].af2hist.SetLineWidth(2)
    if options.family == 'selected' :
        functions[0].af2hist.SetLineColor(ROOT.kGray+2)
        functions[0].af2hist.SetFillColor(0)
    plotfunc.AddHistogram(cans[-1],functions[0].af2hist,drawopt='')
    for i,f in enumerate(functions) :
        f.obsVar.setBins(int(bins))
        f.bins = bins
        f.frame = f.obsVar.frame()
        if i :
            f.af2hist.Rebin(rebin)
        f.af2_rebinned = ROOT.RooDataHist('af2_rebinned','',ROOT.RooArgList(f.obsVar),f.af2hist,1.)
        #f.af2_rebinned.plotOn(f.frame,ROOT.RooFit.Range("lower,upper"))
        #f.function.plotOn(f.frame,ROOT.RooFit.NormRange("lower,upper"),ROOT.RooFit.Range("all"))
        f.chisquare = ChiSquareTools.GetChiSquare_ForSpuriousSignal(f.frame,f.af2_rebinned,f.function,f.ndof)
        print 'Original chi2:',f.chisquare
        #f.chisquare_toy = Tools.ChiSquareToys_ForSpuriousSignal(f)
        f.minNll = 0
        f.pvalue_chi2 = ROOT.TMath.Prob(f.chisquare*(f.bins-1-f.ndof),f.bins-1-f.ndof)
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

    if not options.family == 'selected' :
        plotfunc.SetColors(cans[-1])
    plotfunc.FormatCanvasAxes(cans[-1])
    plotfunc.SetXaxisRanges(cans[-1],functions[0].lower_range,functions[0].upper_range)
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','entries','pull')
    the_text = [plotfunc.GetAtlasInternalText()
                ,plotfunc.GetSqrtsText(13)+', '+plotfunc.GetLuminosityText(36.1)
                ,category_title]
    plotfunc.DrawText(cans[-1],the_text,0.19,0.70,0.59,0.91,totalentries=3)
    plotfunc.MakeLegend(cans[-1]       ,0.60,0.70,0.90,0.91,totalentries=3)
    #plotfunc.GetTopPad(cans[-1]).GetPrimitive('legend').AddEntry(0,'^{ }background-only fit','')
    #list(plotfunc.GetTopPad(cans[-1]).GetPrimitive('legend').GetListOfPrimitives())[-1].SetLabel('^{ }background-only fit')
    plotfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),-4,4)
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(cans[-1]),ignorelegend=False,minzero=True)














    ##
    ## Print out the nominal parameters
    ##
    if not os.path.exists(options.outdir) :
        os.makedirs(options.outdir)
    a = open('%s/parameters.txt'%(options.outdir),'w')
    a.write(options.file+'\n')
    a.write(options.signalws+'\n')
    for f in functions :
        a.write(f.PrintParameters())
        a.write('\n')
    chi = u"\u03C7"
    header = '{:<15} {:>10} {:>10} {:>12} {:>12} {:>10} {:>6} {:>10} {:>10} {:>10} {:>10} {:>10} {:>6}'
    header = header.format('c%d Function'%(options.category),'Sspur/Ssmh','inj bias','Toy bias','ToyNoSig','Sspur/DS','Result','Relax spur','Relax DS','chi2','p(chi2)','tot err','Newult')
    a.write(header+'\n')
    print header
    for f in functions :
        a.write(f.PrintSpuriousSignalStudy()+'\n')
    print

    header = '{:<15} {:>10} {:>10} {:>12} {:>10} {:>10} {:>12} {:>6} {:>6} {:>10} {:>10}'
    header = header.format('c%d Function'%(options.category),'stat err','Toy stat0','Toy sigma0','inj stat','Toy stat','Toy sigma','nfail','nfnsig','chi2sb','p(sb)')
    a.write(header+'\n')
    print header
    for f in functions :
        a.write(f.PrintAdditionalStatInfo()+'\n')


    #
    # Choose the right function
    #
    # sorted by old criteria
    result = ''
    functions = sorted(functions,key = lambda x: (not x.passes,x.ndof,math.fabs(x.max_spur_signalmu)))
    old_function = 'NONE'
    if functions[0].passes :
        old_function = functions[0].name
        result += 'Old test picked %s with total uncertainty %2.2f %%\n'%(functions[0].name,functions[0].total_error*100)
    else :
        result += 'NO OLD FUNCTION\n'

    # sorted by new criteria
    new_function = 'NONE'
    functions = sorted(functions,key = lambda x: (not x.passes_new,x.total_error))
    if functions[0].passes_new :
        result_new = 'New test picked %s with total uncertainty %2.2f %%\n'%(functions[0].name,functions[0].total_error*100)
    else :
        result_new = 'NO NEW FUNCTION\n'

    summary = '{:<15} & {:<15} & {:<15} & {:9.2f}\% & {:9.2f}\% & {:9.2f}\% & {:9.2f}\% \\\\\n'
    f = functions[0]
    if functions[0].passes_new :
        summary = summary.format(category_name.replace('_','\_'),
                                 old_function,
                                 f.name,
                                 f.max_spur_signalz*100.,
                                 f.max_spur_signalz_compatible*100,
                                 f.max_spur_signalmu*100.,
                                 f.max_spur_signalmu_compatible*100.,
                                 )
    else :
        summary = summary.format(category_name.replace('_','\_'),old_function,'NONE',0,0,0,0)

    a.write(result)
    a.write(result_new)
    a.write(summary)
    print result
    print result_new
    print summary

    a.close()


    for can in cans[:-1] :
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
    p.add_option('--family',type='string',default='',dest='family',help='families: official,selected,ExpPoly,Laurent,PolyOverX4,Bernstein,PowerSum')
    p.add_option('--functions','--f',type='string',default='',dest='functions',help='functions Exponential,ExpPoly2,blah')
    p.add_option('--batch',action='store_true',default=False,dest='batch',help='run in batch mode')
    p.add_option('--save',action='store_true',default=False,dest='save',help='save cans to pdf')

    p.add_option('--signalws',type='string',default='',dest='signalws',help='e.g. res_SM_DoubleCB_workspace_me.root')
    p.add_option('--file',type='string',default='',dest='file',help='file (in which the histogram is contained)')
    p.add_option('--analysis',type='string',default='couplings2017',dest='analysis',help='Which analysis (for steering category names, etc)')

    # Expert options
    p.add_option('--rebin',type='string',default='1',dest='rebin',help='Rebinning strategy (Default: 1, ... any compatible rebin number... or "dynamic")')

    options,args = p.parse_args()

    ROOT.gROOT.SetBatch(options.batch)

    if not options.signalws :
        print 'Error! Specify signal workspace! Exiting.'; import sys; sys.exit()
    if not options.file :
        print 'Error! Specify file with histograms. Exiting.'; import sys; sys.exit()

    if '-' in options.category :
        cat_range = options.category.split('-')
        for i in range(int(cat_range[0]), int(cat_range[1])+1) :
            options.category = int(i)
            main_singleCategory(options,args)

    elif options.category == 'all' :
        for i in range(0,17) :
#         for i in range(17,23) :
            options.category = int(i)
            main_singleCategory(options,args)
    else :
        options.category = int(options.category)
        main_singleCategory(options,args)


