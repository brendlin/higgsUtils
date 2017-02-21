
import ROOT
import math
import PlotFunctions as plotfunc
import PyAnalysisPlotting as anaplot
import TAxisFunctions as taxisfunc
plotfunc.SetupStyle()
import Tools
import os

ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)
ROOT.RooMsgService.instance().setSilentMode(True)

def main_singleCategory(options,args) :

    if options.category in [21,22,23,30,31] :
        print 'Error! Too few AF2 stats. Not going to do it.'
        return

    cans = []

    options.outdir = ''

    if options.functions :
        flist = options.functions.split(',')
        options.outdir += '_'.join(flist)

    elif options.family == 'official' :
        flist = ['exppoly','exppoly2','Bernstein_4','Bernstein_5','PowerSum1','Laurent0','Laurent1','Laurent2']
        options.outdir += 'official_functions'

    elif options.family == 'exppoly' :
        flist = ['exppoly'] + list('exppoly%d'%(d) for d in range(2,3))
        options.outdir += 'exppoly_family'

    elif options.family == 'Laurent' :
        flist = list('Laurent%d'%(d) for d in range(0,3))
        options.outdir += 'Laurent_family'

    elif options.family == 'PolyOverX4' :
        flist = ['1/x^4'] + list('poly%d/x^4'%(d) for d in range(1,6))
        options.outdir += 'PolyOverX4_family'

    elif options.family == 'Bernstein' :
        flist = list('Bernstein_%d'%(d) for d in range(4,6))
        options.outdir += 'Bernstein_family'

    elif options.family == 'PowerSum' :
        flist = ['PowerSum1','PowerSum2']
        options.outdir += 'PowerSum_family'

    else :
        flist = [
            'exppoly', # bad
            'exppoly2',
            'exppoly3',
            ]
        options.outdir += '_'.join(flist)

    options.outdir += '_c%02d_%s'%(options.category,Tools.categories[options.category])

    functions = []
    Tools.PopulateFunctionList(functions,flist)
    if len(functions) == 0 :
        print 'Error! no functions loaded!'
        import sys; sys.exit()

    for f in functions :
        f.SetCategory(options.category)
        f.Initialize()


    cans.append(ROOT.TCanvas("c%02d_error_summary"%(options.category),"error_summary",500,400))
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
    plotfunc.AddHistogram(cans[-1],injected_hist,drawopt='hist')

    ## Systematic with injection - 125 GeV
#     injected_hist_125 = ROOT.TH1F('injected_hist_125','injection syst 125',len(flist),0,len(flist))
#     for i,f in enumerate(functions) :
#         injected_hist_125.SetBinContent(i+1,Tools.GetInjectedSignalBias(f,125))
#     injected_hist_125.SetLineStyle(2)
#     plotfunc.AddHistogram(cans[-1],injected_hist_125,drawopt='hist')

    ## Error on the signal (in the injection case) - only 125
    error_hist_inj = ROOT.TH1F('error_hist_inj','stat (inject SM)',len(flist),0,len(flist))
    for i,f in enumerate(functions) :
        error_hist_inj.SetBinContent(i+1,f.injectionerror/float(f.smsignalyield.getVal())) # only 125
    cans[-1].cd()
    error_hist_inj.SetLineStyle(2)
    plotfunc.AddHistogram(cans[-1],error_hist_inj,drawopt='hist')

    plotfunc.SetColors(cans[-1])
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    #plotfunc.AutoFixAxes(cans[-1],ignorelegend=True)
    taxisfunc.AutoFixYaxis(cans[-1],ignorelegend=True,minzero=True)





    ##
    ## Spurious signal mu canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_spurious_signal_mu"%(options.category),"spurious signal mu",500,400))
    
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
    a = ROOT.TLine(); a.DrawLine(121,-0.1,129,-0.1)
    a.DrawLine(121, 0.1,129, 0.1)
    a.DrawLine(121,-0.1,121, 0.1)
    a.DrawLine(129,-0.1,129, 0.1)





    ##
    ## Stats-limited spurious signal mu canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_spurious_signal_mu_statlim"%(options.category),"spurious signal mu (stat-limited)",500,400))
    functions[0].spurioussignalmucomp.Draw('al')
    for i,f in enumerate(functions[1:]) :
        f.spurioussignalmucomp.Draw('l')
    plotfunc.MakeLegend(cans[-1],.6,.75,.9,.9)
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','S_{spur}/S_{SM}')
    taxisfunc.SetYaxisRanges(cans[-1],-0.5,0.5)
    taxisfunc.SetXaxisRanges(cans[-1],110,160)
    a = ROOT.TLine(); a.DrawLine(121,-0.1,129,-0.1)
    a.DrawLine(121, 0.1,129, 0.1)
    a.DrawLine(121,-0.1,121, 0.1)
    a.DrawLine(129,-0.1,129, 0.1)





    ##
    ## Spurious signal Z canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_spurious_signal_z"%(options.category),"spurious signal z",500,400))
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
    a = ROOT.TLine();
    a.DrawLine(121,-0.2,129,-0.2)
    a.DrawLine(121, 0.2,129, 0.2)
    a.DrawLine(121,-0.2,121, 0.2)
    a.DrawLine(129,-0.2,129, 0.2)




    ##
    ## Injected signal bias canvas
    ##
    cans.append(ROOT.TCanvas("c%02d_signal_bias_mu"%(options.category),"signal bias mu",500,400))
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
    a = ROOT.TLine();
    a.DrawLine(121,-0.1,129,-0.1)
    a.DrawLine(121, 0.1,129, 0.1)
    a.DrawLine(121,-0.1,121, 0.1)
    a.DrawLine(129,-0.1,129, 0.1)

    ##
    ## Plot the data and af2 (fit bkg-only just before this.)
    ##
    cans.append(plotfunc.RatioCanvas("c%02d_mainplot"%(options.category),"main plot",500,400))
    functions[0].af2hist.SetMarkerSize(0)
    plotfunc.AddHistogram(cans[-1],functions[0].af2hist,drawopt='')
    plotfunc.AddHistogram(cans[-1],functions[0].higgshist,drawopt='')
    plotfunc.AddHistogram(cans[-1],functions[0].datahist)
    for i in plotfunc.GetTopPad(cans[-1]).GetListOfPrimitives() :
        if hasattr(i,'Rebin') :
            i.Rebin(functions[0].rebin)
    for f in functions :
        roofitresult = f.function.fitTo(f.data,*(Tools.args_bkgonly))
        f.function.plotOn(f.frame_rebinned)
        # Get the chi2 from the background-only fit
        f.chisquare = f.frame_rebinned.chiSquare(1) # n-1 bins
        f.minNll = 0
        f.pvalue_chi2 = ROOT.TMath.Prob(f.chisquare*(f.bins_rebinned-1),f.bins_rebinned-1)
        curve = f.frame_rebinned.getCurve(); curve.SetMarkerSize(0); curve.SetLineWidth(1)
        curve.SetTitle(f.name)
        resid = f.frame_rebinned.residHist(); resid.SetMarkerSize(0)
        plotfunc.AddRatioManual(cans[-1],curve,resid,drawopt1='l',drawopt2='l')
        del roofitresult
    plotfunc.SetColors(cans[-1])
    plotfunc.MakeLegend(cans[-1],.6,.40,.9,.9)
    plotfunc.SetXaxisRanges(cans[-1],Tools.lower_range,Tools.upper_range)
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(cans[-1]),ignorelegend=True)

    ##
    ## Plot all the functions
    ##
#     if False :
#         cans.append(ROOT.TCanvas('fit_canvas','fit_canvas',725,500))
#         common_frame = functions[0].frame
#         functions[0].data.plotOn(common_frame)
#         for f in functions :
#             f.function.fitTo(f.data,*(Tools.args_bkgonly))
#             f.selectedpdf.SetName('%s fit total'%f.name)
#             f.selectedpdf.SetTitle(f.name)
#             f.workspace.var("nSignal").setVal(f.smsignalyield.getVal())
#             f.selectedpdf.plotOn(common_frame,ROOT.RooFit.Range("FULL"))
#             dummy = ROOT.RooArgSet(); dummy.add(f.function)
#             f.selectedpdf.plotOn(common_frame,ROOT.RooFit.Components(dummy),ROOT.RooFit.Range("FULL"),ROOT.RooFit.LineStyle(ROOT.kDashed))
#         functions[0].nomfunction.plotOn(common_frame)
#         common_frame.Draw()




    ##
    ## Print out the nominal parameters
    ##
    if not os.path.exists(options.outdir) :
        os.makedirs(options.outdir)
    a = open('%s/parameters.txt'%(options.outdir),'w')
    for f in functions :
        a.write(f.PrintParameters())
        a.write('\n')
    chi = u"\u03C7"
    header = '{:<15} {:^10} {:^10} {:^7} {:^10} {:^10} {:^10} {:^10} {:^6} {:^10}'
    header = header.format('c%d Function'%(options.category),'Sspur/Ssmh','Sspur/DS','Result','Relax spur','chi2','p(chi2)','tot err','Newult','minNll')
    print header
    #
    # Choiose the write function
    #
    choice = []
    choice_new = []
    def sortnew(item) :
        return item[1]
    def sortold(item) :
        return item[2]
    a.write(header+'\n')
    for f in functions :
        a.write(f.PrintSpuriousSignalStudy()+'\n')
        if f.passes_new :
            choice_new.append([f.name,f.total_error,f.ndof])
        if f.passes :
            choice.append([f.name,f.total_error,f.ndof])
    print choice
    choice = sorted(choice,key=sortold)
    result = ''
    if choice :
        for c in choice :
            if c[2] == choice[0][2] :
                result += 'Old test picked %s with total uncertainty %2.2f %%\n'%(c[0],c[1]*100)
    else :
        result += 'NO OLD FUNCTION\n'
    choice_new = sorted(choice_new,key=sortnew)
    if choice_new :
        result_new = 'New test picked %s with total uncertainty %2.2f %%\n'%(choice_new[0][0],choice_new[0][1]*100)
    else :
        result_new = 'NO NEW FUNCTION\n'
    a.write(result)
    a.write(result_new)
    print result
    print result_new
    a.close()

    for can in cans[:-1] :
        plotfunc.FormatCanvasAxes(can)

    anaplot.UpdateCanvases(options,cans)
    if not options.batch :
        raw_input('Press enter to exit')
    anaplot.doSaving(options,cans)

    return

if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--category','--c',type='string',default='',dest='category',help='category (0-30something)')
    p.add_option('--family',type='string',default='',dest='family',help='functions exppoly,exppoly2,blah')
    p.add_option('--functions','--f',type='string',default='',dest='functions',help='functions exppoly,exppoly2,blah')
    p.add_option('--batch',action='store_true',default=False,dest='batch',help='run in batch mode')
    p.add_option('--save',action='store_true',default=False,dest='save',help='save cans to pdf')
    
    options,args = p.parse_args()

    ROOT.gROOT.SetBatch(options.batch)

    if options.category == 'all' :
        for i in range(0,33) :
            options.category = int(i)
            main_singleCategory(options,args)
    else :
        options.category = int(options.category)
        main_singleCategory(options,args)


