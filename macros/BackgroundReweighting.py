
import ROOT
import PlotFunctions as plotfunc
import TAxisFunctions as taxisfunc
import PyAnalysisPlotting as anaplot
import Tools
import os 

offset = 0

plotfunc.SetupStyle()

categories = [
    'Inclusive',
    'M17_ggH_0J_Cen',        # 1
    'M17_ggH_0J_Fwd',        # 2
    'M17_ggH_1J_LOW',        # 3
    'M17_ggH_1J_MED',        # 4
    'M17_ggH_1J_HIGH',       # 5
    'M17_ggH_1J_BSM',        # 6
    'M17_ggH_2J_LOW',        # 7
    'M17_ggH_2J_MED',        # 8
    'M17_ggH_2J_HIGH',       # 9
    'M17_ggH_2J_BSM',        # 10
    'M17_VBF_HjjLOW_loose',  # 11
    'M17_VBF_HjjLOW_tight',  # 12
    'M17_VBF_HjjHIGH_loose', # 13
    'M17_VBF_HjjHIGH_tight', # 14
    'M17_VHhad_loose',       # 15
    'M17_VHhad_tight',       # 16
    'M17_qqH_BSM',           # 17
    'M17_VHMET_LOW',         # 18
    'M17_VHMET_HIGH',        # 19
    'M17_VHMET_BSM',         # 20
    'M17_VHlep_LOW',         # 21
    'M17_VHlep_HIGH',        # 22
    'M17_VHdilep_LOW',       # 23
    'M17_VHdilep_HIGH',      # 24
    'M17_ttH_Had_6j2b',      # 25
    'M17_ttH_Had_6j1b',      # 26
    'M17_ttH_Had_5j2b',      # 27
    'M17_ttH_Had_5j1b',      # 28
    'M17_ttH_Had_4j2b',      # 29
    'M17_ttH_Had_4j1b',      # 30
    'M17_ttH_Lep',           # 31
    'M17_ttH_Lep_0fwd',      # 32
    'M17_ttH_Lep_1fwd',      # 33
    ]

def integral(hist,f,l) :
    return hist.Integral(hist.FindBin(f+0.00000001),hist.FindBin(l+0.00000001))

jj_file = ROOT.TFile('AF2_jj.root','read')
yj_file = ROOT.TFile('AF2_yj.root','read')
af2_file = ROOT.TFile('AF2_Tweaks_Inclusive.root','read')

cans = []

def DoRescaleProcedure(af2,bkg,name,ci,c) :
    cans = []
    if integral(af2,105,160) == 0 :
        return [],0,1,1
    if integral(bkg,105,160) == 0 :
        return [],0,1,1

    cans.append(plotfunc.RatioCanvas('UntouchedRatio_%d_%s_%s'%(ci,c,name),'%d_%s_%s'%(ci,c,name),500,500))
    af2_rebin = plotfunc.AddHistogram(cans[-1],af2)
    bkg_rebin = bkg.Clone()
    bkg_rebin.SetName(bkg_rebin.GetName()+'_forRebinning')
    
    Tools.RebinUntilSmallErrors(af2_rebin,bkg_rebin,binmin=105,binmax=160)
    af2_rebin.Scale(integral(bkg_rebin,105,160)/integral(af2_rebin,105,160))
    
    unused,af2_bkg_ratio = plotfunc.AddRatio(cans[-1],bkg_rebin,af2_rebin)
    taxisfunc.AutoFixAxes(cans[-1])
    taxisfunc.SetXaxisRanges(cans[-1],105,160)

    function = ROOT.TF1('%d_%s'%(ci,c),'[0]*(x-132.5)/(160-105) + [1]',105,160)
    af2_bkg_ratio.Fit('%d_%s'%(ci,c))
    #function.SetParameters(-2,1)
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),0,2)

    af2_integral = integral(af2,105,160)
    af2_result = af2.Clone()
    af2_result.SetTitle(af2_result.GetName()+'_rescaled')
    af2_result.Multiply(function)
    integral_factor = af2_integral / float(integral(af2_result,105,160))
    Tools.RebinUntilSmallErrors(af2_result,bkg,binmin=105,binmax=160,errormax=1)
    if integral(af2_result,105,160) :
        af2_result.Scale(integral(bkg,105,160)/integral(af2_result,105,160))
    

    cans.append(plotfunc.RatioCanvas('rescaled_%d_%s_%s'%(ci,c,name),'%d_%s_%s_rescaled'%(ci,c,name),500,500))
    plotfunc.AddHistogram(cans[-1],bkg)
    plotfunc.AddRatio(cans[-1],af2_result,bkg)

    taxisfunc.AutoFixAxes(cans[-1])
    taxisfunc.SetXaxisRanges(cans[-1],105,160)
    taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(cans[-1]),0,2)

    return cans,function.GetParameter(0),function.GetParameter(1),integral_factor





cans = []
for i,c in enumerate(categories) :
    #print 'HGamEventInfoAuxDyn_m_yy_over_1000_c%d_%s_AF2'%(i+offset,c)
    tmp = []

    af2 = af2_file.Get('HGamEventInfoAuxDyn_m_yy_over_1000_c%d_%s_AF2' %(i+offset,c)).Clone()
    yj  = yj_file .Get('HGamEventInfoAuxDyn_m_yy_over_1000_c%d_%s_data'%(i+offset,c))
    jj  = jj_file .Get('HGamEventInfoAuxDyn_m_yy_over_1000_c%d_%s_data'%(i+offset,c))

    data_blinded = af2_file.Get('HGamEventInfoAuxDyn_m_yy_over_1000_c%d_%s_data'%(i+offset,c))
    data_integral = integral(data_blinded,105,160)
    
    af2.Sumw2(); yj.Sumw2(); jj.Sumw2();

    yj_newcans,yj_par0,yj_par1,yj_integral_factor = DoRescaleProcedure(af2,yj,'yj',i+offset,c)
    jj_newcans,jj_par0,jj_par1,jj_integral_factor = DoRescaleProcedure(af2,jj,'jj',i+offset,c)
    tmp += yj_newcans
    tmp += jj_newcans

    fractions_file = open('fractions.txt','read')
    for l,line in enumerate(fractions_file) :
        if (l != i+offset) :
            continue
        #print l,line
        yy_frac = float(line.split()[-3])/100.
        yj_frac = float(line.split()[-2])/100.
        jj_frac = float(line.split()[-1])/100.
    fractions_file.close()
    print yy_frac,yj_frac,jj_frac

    #                                         yj                                        jj
    function = ROOT.TF1('%d_%s'%(i+offset,c),'([0]*(x-132.5)/(160-105) + [1])*[2]*[3] + ([4]*(x-132.5)/(160-105) + [5])*[6]*[7] + [8]',105,160)
    function.SetParameters(yj_par0,yj_par1,yj_frac,yj_integral_factor,jj_par0,jj_par1,jj_frac,jj_integral_factor,yy_frac)

    data_integral = float(integral(data_blinded,105,120) + integral(data_blinded,130,160) )
    af2_integral = float(integral(af2,105,120)+integral(af2,130,160) )

    rebin = 10

    # yy for stack
    af2_yy_stack = af2.Clone(); af2_yy_stack.SetName(af2_yy_stack.GetName()+'_yy_forStack')
    af2_yy_stack.Scale( yy_frac * data_integral / af2_integral )
    af2_yy_stack.Rebin(rebin)

    # yj for stack
    af2_yj_stack = af2.Clone(); af2_yj_stack.SetName(af2_yj_stack.GetName()+'_yj_forStack')
    function_yj = ROOT.TF1('%d_%s'%(i+offset,c),'([0]*(x-132.5)/(160-105) + [1])*[2]*[3]',105,160)
    function_yj.SetParameters(yj_par0,yj_par1,yj_frac,yj_integral_factor)
    af2_yj_stack.Multiply(function_yj)
    af2_yj_stack.Scale( data_integral / af2_integral )
    af2_yj_stack.Rebin(rebin)

    # jj for stack
    af2_jj_stack = af2.Clone(); af2_jj_stack.SetName(af2_jj_stack.GetName()+'_jj_forStack')
    function_jj = ROOT.TF1('%d_%s'%(i+offset,c),'([0]*(x-132.5)/(160-105) + [1])*[2]*[3]',105,160)
    function_jj.SetParameters(jj_par0,jj_par1,jj_frac,jj_integral_factor)
    af2_jj_stack.Multiply(function_jj)
    af2_jj_stack.Scale( data_integral / af2_integral )
    af2_jj_stack.Rebin(rebin)
    
    anaplot.PrepareBkgHistosForStack([af2_jj_stack,af2_yj_stack,af2_yy_stack],'')
    
    # full thing.
    af2.Multiply(function)
    af2.Scale( data_integral / float(integral(af2,105,120)+integral(af2,130,160) ) )
 
    main_can = plotfunc.RatioCanvas('Mimic_Plot_%s_%s'%(i+offset,c),'Mimic plot',500,500)
    plotfunc.AddHistogram(main_can,af2_jj_stack)
    plotfunc.AddHistogram(main_can,af2_yj_stack)
    plotfunc.AddHistogram(main_can,af2_yy_stack)
    plotfunc.Stack(main_can)

    #print Tools.FindRebinFactors(af2)
    af2.Rebin(rebin)
    data_blinded.Rebin(rebin)
    af2.SetMarkerSize(0); af2.SetLineColor(1); af2.SetLineWidth(2); af2.SetFillColor(1)
    af2.SetFillStyle(3254);
    plotfunc.AddHistogram(main_can,af2,drawopt='E2')

    if False :
        # RATIO
        plotfunc.AddRatio(main_can,data_blinded,af2)
        taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(main_can),0.5,1.5)
    else :
        # PULL
        plotfunc.AddRatio(main_can,data_blinded,af2,divide='pull')
        taxisfunc.SetYaxisRanges(plotfunc.GetBotPad(main_can),-3.5,4.5)
    taxisfunc.SetXaxisRanges(main_can,105,160)
    taxisfunc.AutoFixYaxis(plotfunc.GetTopPad(main_can),minzero=True)
    tmp.append(main_can)
    
    for can in tmp :
        plotfunc.FormatCanvasAxes(can)

    anaplot.UpdateCanvases(tmp)
    os.system('mkdir -p c%02d_%s'%(i,c))
    for can in tmp :
        can.Print('c%02d_%s/%s.pdf'%(i,c,can.GetName()))

    cans += yj_newcans
    cans += jj_newcans

raw_input('pause')
