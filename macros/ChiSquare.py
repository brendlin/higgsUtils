#!/usr/bin/env python

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

    if options.category in [30,31] :
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

    options.outdir += '_c%02d_%s'%(options.category,Tools.categories[options.category])

    functions = []
    Tools.PopulateFunctionList(functions,flist)
    Tools.LinkFunctionsForFtest(functions)
    if len(functions) == 0 :
        print 'Error! no functions loaded!'
        import sys; sys.exit()

    for f in functions :
        f.SetCategory(options.category)
        f.SetFileName(options.file)
        f.SetSignalWS(options.signalws)
        f.Initialize()

    ##
    ## Plot the data and af2 (fit bkg-only just before this.) SpuriousSignal_05_M17_ggH_1J_BSM
    ##
    for f in functions :
        f.function.fitTo(f.data,*(Tools.args_bkgonly))
    cans.append(plotfunc.RatioCanvas("TemplateFit_%02d_%s"%(options.category,Tools.categories[options.category]),"main plot",600,500))
    functions[0].af2hist.SetMarkerSize(0)
    #rebin = Tools.RebinUntilSmallErrors(functions[0].af2hist,0,Tools.lower_range,Tools.upper_range,errormax=0.3)
    rebin = 5
    functions[0].af2hist.Rebin(rebin)
    binwidth = functions[0].af2hist.GetBinWidth(1)
    bins = int((Tools.upper_range-Tools.lower_range)/float(binwidth))
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
        f.chisquare = Tools.GetChiSquare_ForSpuriousSignal(f.frame,f.af2_rebinned,f.function,f.ndof)
        f.pvalue_chi2 = ROOT.TMath.Prob(f.chisquare*(f.bins-1-f.ndof),f.bins-1-f.ndof)
        print 'Original chi2: %2.6f p-value: %2.6f'%(f.chisquare,f.pvalue_chi2)
        f.minNll = 0
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

        f.chisquare_toy = Tools.ChiSquareToys_ForSpuriousSignal(f,options.outdir)

    if not options.family == 'selected' :
        plotfunc.SetColors(cans[-1])
    plotfunc.FormatCanvasAxes(cans[-1])
    plotfunc.SetXaxisRanges(cans[-1],Tools.lower_range,Tools.upper_range)
    plotfunc.SetAxisLabels(cans[-1],'m_{#gamma#gamma} [GeV]','entries','pull')
    the_text = [plotfunc.GetAtlasInternalText()
                ,plotfunc.GetSqrtsText(13)+', '+plotfunc.GetLuminosityText(36.1)
                ,Tools.CategoryNames[Tools.categories[options.category]]]
    plotfunc.DrawText(cans[-1],the_text,0.19,0.70,0.59,0.91,totalentries=3)
    plotfunc.MakeLegend(cans[-1]       ,0.60,0.70,0.90,0.91,totalentries=3)
    #plotfunc.GetTopPad(cans[-1]).GetPrimitive('legend').AddEntry(0,'^{ }background-only fit','')
    #list(plotfunc.GetTopPad(cans[-1]).GetPrimitive('legend').GetListOfPrimitives())[-1].SetLabel('^{ }background-only fit')
    plotfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),-4,4)
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(cans[-1]),ignorelegend=False,minzero=True)


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

    options,args = p.parse_args()

    ROOT.gROOT.SetBatch(options.batch)

    if not options.signalws :
        print 'Error! Specify signal workspace! Exiting.'; import sys; sys.exit()
    if not options.file :
        print 'Error! Specify file with histograms. Exiting.'; import sys; sys.exit()

    if options.category == 'all' :
        for i in range(0,17) :
            options.category = int(i)
            main_singleCategory(options,args)
    else :
        options.category = int(options.category)
        main_singleCategory(options,args)


