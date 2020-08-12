#!/usr/bin/env python

import ROOT
import math
import PlotFunctions as plotfunc
import PyAnalysisPlotting as anaplot
import TAxisFunctions as taxisfunc
import Tools
import FunctionsModule
import ChiSquareTools
import os

# Get base path (higgsUtils)
the_path = ('/').join(os.path.abspath(__file__).split('/')[:-2])

# Add to macro path
ROOT.gROOT.SetMacroPath('%s:%s/share'%(ROOT.gROOT.GetMacroPath(),the_path))
ROOT.gROOT.ProcessLine('.L RooTwoSidedCBShape.cxx+')

ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
ROOT.RooMsgService.instance().setSilentMode(True)

fcns = {
    'official'  :['Exponential','ExpPoly2','ExpPoly3','Bernstein_4','Bernstein_5','Pow'],
    'selected'  :None, # to be filled in main_singleCategory
    'ExpPoly'   :['Exponential'] + list('ExpPoly%d'%(d) for d in range(2,4)),
    'Laurent'   :list('Laurent%d'%(d) for d in range(0,3)),
    'PolyOverX4':['1/x^4'] + list('poly%d/x^4'%(d) for d in range(1,6)),
    'Bernstein' :list('Bernstein_%d'%(d) for d in range(4,6)),
    'PowerSum'  :['Pow','Pow2'],
    }

def main_singleCategory(options,args) :

    # Seems important to keep the style class in memory for some reason
    mystyle = plotfunc.SetupStyle()

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
        fcns['selected'] = [Tools.selected_couplings2017[category_name]]
        background_label = '#gamma#gamma'
        lumi = 36.1
    elif options.analysis == 'ysy' :
        category_name = Tools.categories_ysy[options.category]
        category_title = Tools.CategoryNames_ysy[category_name]
        fcns['selected'] = [Tools.selected_ysy[category_name]]
        background_label = 'll#gamma'
        lumi = 139
    else :
        print('Error - do not understand analysis name %s'%(options.analysis))
        import sys; sys.exit()


    family_name = {
        'official':'official_functions',
        'selected':'selected_function',
        }.get(options.family,options.family+'_family')

    # A list of options is provided
    if options.functions :
        flist = options.functions.split(',')
        options.outdir += '_'.join(flist)

    # Otherwise a family must be provided:
    else :
        flist = fcns.get(options.family)
        options.outdir += family_name

    # Sync up colors according to the function.
    tmp_colors = plotfunc.KurtColorPalate()
    tmp_colors[5] = ROOT.kOrange+2
    selected_colors_dict = dict()
    for i,f in enumerate(fcns['official']) :
        selected_colors_dict[f] = tmp_colors[i]

    # The first color is for the MC histogram.
    # The subsequent colors are associated with the functions.
    colors = [ROOT.kGray+2]
    for f in flist :
        colors.append(selected_colors_dict[f])

    # For non-official functions, fill in some more colors.
    for c in tmp_colors :
        if c not in colors :
            colors.append(c)

    options.outdir += '_c%02d_%s'%(options.category,category_name)

    functions = []
    FunctionsModule.PopulateFunctionList(functions,flist,options.lower,options.upper)
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

    ## Spurious signal Z, Mu
    syst_hist = ROOT.TH1F('syst_hist','syst (0-bkg)',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        syst_hist.SetBinContent(i+1,abs(Tools.GetSpuriousSignalMu(f,color=colors[i+1])))
        syst_hist.GetXaxis().SetBinLabel(i+1,f.name)
        Tools.GetSpuriousSignalZ(f,color=colors[i+1],lower_range=options.lower,upper_range=options.upper)
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
        injected_hist.SetBinContent(i+1,Tools.GetSignalBiasMuScan(f,color=colors[i+1]))
    injected_hist.SetLineStyle(2)
    if False :
        plotfunc.AddHistogram(cans[-1],injected_hist,drawopt='hist')

    ## Systematic with injection - 125 GeV
    injected_hist_125 = ROOT.TH1F('injected_hist_125','injection syst 125',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        injected_hist_125.SetBinContent(i+1,Tools.GetInjectedSignalBias(f,125))
    injected_hist_125.SetLineStyle(2)
    if False :
        plotfunc.AddHistogram(cans[-1],injected_hist_125,drawopt='hist')

    ## Error on the signal (in the injection case) - only 125
    error_hist_inj = ROOT.TH1F('error_hist_inj','stat (inject SM)',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        error_hist_inj.SetBinContent(i+1,f.injectionerror_rel) # only 125
    cans[-1].cd()
    error_hist_inj.SetLineStyle(2)
    if False :
        plotfunc.AddHistogram(cans[-1],error_hist_inj,drawopt='hist')

    plotfunc.SetColors(cans[-1])
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    taxisfunc.AutoFixYaxis(cans[-1],ignorelegend=True,minzero=True)

    the_text = [plotfunc.GetAtlasInternalText()
                ,plotfunc.GetSqrtsText(13)+', '+plotfunc.GetLuminosityText(lumi)
                ,category_title]

    def PlotCanvas(name,title,yaxislabel,members_to_plot,yrange=0.5,boxlim=0.1) :
        cans.append(ROOT.TCanvas(name,title,600,500))
        for f in functions :
            for m in members_to_plot :
                plotfunc.AddHistogram(cans[-1],getattr(f,m),drawopt='l')
        plotfunc.FormatCanvasAxes(cans[-1])
        plotfunc.MakeLegend(cans[-1],.6,.75,.9,.93,totalentries=4,extend=True)
        plotfunc.DrawText(cans[-1],the_text,.20,.75,.59,.93,totalentries=4)
        cans[-1].GetPrimitive('legend').SetFillStyle(1001)
        plotfunc.SetAxisLabels(cans[-1],'m_{%s} [GeV]'%(background_label),yaxislabel)
        #taxisfunc.SetYaxisRanges(cans[-1],-yrange,yrange)
        taxisfunc.AutoFixYaxis(cans[-1])
        taxisfunc.SetXaxisRanges(cans[-1],options.lower,options.upper)
        Tools.DrawBox(121,129,-boxlim,boxlim)

    ## Spurious signal mu canvas
    PlotCanvas('c%02d_spurious_signal_mu'%(options.category),'spurious signal mu','S_{spur}/S_{SM}',
               ['spurioussignalmucv','spurioussignalmuup','spurioussignalmudn'])

    ## Stats-limited spurious signal mu canvas
    PlotCanvas('c%02d_spurious_signal_mu_statlim'%(options.category),'spurious signal mu (stat-limited)',
               '(S_{spur}#pm1#sigma)/S_{SM}',['spurioussignalmucomp'])

    ## Spurious signal Z canvas
    PlotCanvas('c%02d_spurious_signal_z'%(options.category),'spurious signal z','S_{spur}/#Delta^{}S',
               ['spurioussignalzcv','spurioussignalzup','spurioussignalzdn'],1.0,0.2)

    ## Stats-limited spurious signal z canvas
    PlotCanvas('c%02d_spurious_signal_z_statlim'%(options.category),'spurious signal Z (stat-limited)',
               '(S_{spur}#pm1#sigma)/#Delta^{}S',['spurioussignalzcomp'],1.0,0.2)

    ## Injected signal bias canvas
    PlotCanvas('c%02d_signal_bias_mu'%(options.category),'signal bias mu','S_{bias}/#Delta^{}S',
               #['signalbiasmucv','signalbiasmuup','signalbiasmudn'])
               ['signalbiasmucv'])

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

    # Rebin to get 1 bin per GeV
    rebin = int(functions[0].af2hist.GetNbinsX() / 55)

    if options.rebin == 'dynamic' :
        print('Dynamically rebinning')
        rebin = Tools.RebinUntilSmallErrors(functions[0].af2hist,0,Tools.lower_range,Tools.upper_range,errormax=0.3)
    elif int(options.rebin) > 0 :
        rebin = int(options.rebin)

    functions[0].af2hist.Rebin(rebin)
    binwidth = functions[0].af2hist.GetBinWidth(1)
    bins = int((functions[0].upper_range-functions[0].lower_range)/float(binwidth))
    functions[0].af2hist.SetTitle('%s MC'%(background_label))
    functions[0].af2hist.SetLineWidth(2)
    plotfunc.AddHistogram(cans[-1],functions[0].af2hist,drawopt='le')
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
            color = selected_colors_dict.get(f.name)
            pull.SetMarkerColor(color); pull.SetLineColor(color);
            curve.SetLineColor(color); curve.SetFillColor(0)
        
        plotfunc.AddRatioManual(cans[-1],curve,pull,drawopt1='l',drawopt2='p')

    plotfunc.SetColors(cans[-1],these_colors=colors)
    plotfunc.FormatCanvasAxes(cans[-1])
    plotfunc.SetXaxisRanges(cans[-1],functions[0].lower_range,functions[0].upper_range)
    plotfunc.SetAxisLabels(cans[-1],'m_{%s} [GeV]'%(background_label),'entries','pull')
    plotfunc.DrawText(cans[-1],the_text,0.19,0.70,0.59,0.91,totalentries=3)
    plotfunc.MakeLegend(cans[-1]       ,0.60,0.70,0.90,0.91,totalentries=3,extend=True)

    if options.family == 'selected' :
        list(plotfunc.GetTopPad(cans[-1]).GetPrimitive('legend').GetListOfPrimitives())[2].SetLabel('^{ }background-only fit')

    plotfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),-3.99,3.99)
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(cans[-1]),ignorelegend=True,ignoretext=False,minzero=True)


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

    # Run tests, sort functions
    for f in functions :
        f.RunTests()
        f.passes = f.passes_1sig_chi2

    # Sort functions by passing, then ndof, then max(spurSig)
    functions_sorted = sorted(functions,key = lambda x: (not x.passes,x.ndof,abs(x.max_spur_signalmu)))

    for i,f in enumerate(functions) :
        selected = ' selected' if ((f.name == functions_sorted[0].name) and functions_sorted[0].passes) else ''
        row = f.PrintSpuriousSignalStudy(skipHeader=i)+selected
        print row
        a.write(row+'\n')

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
    p.add_option('--family',type='string',default='',dest='family',help='families: %s'%(', '.join(fcns.keys())))
    p.add_option('--functions','--f',type='string',default='',dest='functions',help='functions Exponential,ExpPoly2, etc.')
    p.add_option('--batch',action='store_true',default=False,dest='batch',help='run in batch mode')
    p.add_option('--save',action='store_true',default=False,dest='save',help='save cans to pdf')

    p.add_option('--signalws',type='string',default='',dest='signalws',help='e.g. res_SM_DoubleCB_workspace_me.root')
    p.add_option('--file',type='string',default='',dest='file',help='file (in which the histogram is contained)')
    p.add_option('--analysis',type='string',default='couplings2017',dest='analysis',help='Which analysis (for steering category names, etc)')

    # Expert options
    p.add_option('--lower',type='int'   ,default=105,dest='lower',help='Lower window (defaut is 105)')
    p.add_option('--upper',type='int'   ,default=160,dest='upper',help='Upper window (defaut is 160)')
    p.add_option('--rebin',type='string',default='0',dest='rebin',help='Rebinning strategy (Default: 1 GeV/bin. Pick any compatible rebin number... or "dynamic")')

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


