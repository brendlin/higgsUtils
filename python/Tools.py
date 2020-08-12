
import ROOT
import math
import PlotFunctions as plotfunc

categories_ysy = [
    #None,
    'GGF_DIMUON',              # 1
    'GGF_RESOLVED_DIELECTRON', # 2
    'GGF_MERGED_DIELECTRON',   # 3
    'VBF_DIMUON',              # 4
    'VBF_RESOLVED_DIELECTRON', # 5
    'VBF_MERGED_DIELECTRON',   # 6
    'HIPTT_DIMUON',              # 7
    'HIPTT_RESOLVED_DIELECTRON', # 8
    'HIPTT_MERGED_DIELECTRON',   # 9
    ]

CategoryNames_ysy = {
    'GGF_DIMUON'             :'Inclusive Dimuon',
    'GGF_RESOLVED_DIELECTRON':'Inclusive Resolved Electron',
    'GGF_MERGED_DIELECTRON'  :'Inclusive Merged Electron',
    'VBF_DIMUON'             :'VBF Dimuon',
    'VBF_RESOLVED_DIELECTRON':'VBF Resolved Electron',
    'VBF_MERGED_DIELECTRON'  :'VBF Merged Electron',
    'HIPTT_DIMUON'             :'High-p_{TThrust} Dimuon',
    'HIPTT_RESOLVED_DIELECTRON':'High-p_{TThrust} Resolved Electron',
    'HIPTT_MERGED_DIELECTRON'  :'High-p_{TThrust} Merged Electron',
    }

selected_ysy = {
    'GGF_DIMUON'               :'ExpPoly2',
    'GGF_RESOLVED_DIELECTRON'  :'ExpPoly3',
    'GGF_MERGED_DIELECTRON'    :'ExpPoly2',
    'VBF_DIMUON'               :'Pow',
    'VBF_RESOLVED_DIELECTRON'  :'Exponential',
    'VBF_MERGED_DIELECTRON'    :'Pow',
    'HIPTT_DIMUON'             :'Pow',
    'HIPTT_RESOLVED_DIELECTRON':'Pow',
    'HIPTT_MERGED_DIELECTRON'  :'Pow',
    }

categories_couplings2017 = [
    #None,
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
    'M17_tH_Had_4j2b',       # 25
    'M17_tH_Had_4j1b',       # 26
    'M17_ttH_Had_BDT4',      # 27
    'M17_ttH_Had_BDT3',      # 28
    'M17_ttH_Had_BDT2',      # 29
    'M17_ttH_Had_BDT1',      # 30
    'M17_ttH_Lep',           # 31
    'M17_tH_lep_1fwd',       # 32
    'M17_tH_lep_0fwd',       # 33
    ]

CategoryNames_couplings2017 = {
    'Inclusive'             :'Inclusive',
    'M17_ggH_0J_Cen'        :'ggH 0J Central',
    'M17_ggH_0J_Fwd'        :'ggH 0J Forward',
    'M17_ggH_1J_LOW'        :'ggH 1J Low',
    'M17_ggH_1J_MED'        :'ggH 1J Med',
    'M17_ggH_1J_HIGH'       :'ggH 1J High',
    'M17_ggH_1J_BSM'        :'ggH 1J BSM',
    'M17_ggH_2J_LOW'        :'ggH 2J Low',
    'M17_ggH_2J_MED'        :'ggH 2J Med',
    'M17_ggH_2J_HIGH'       :'ggH 2J High',
    'M17_ggH_2J_BSM'        :'ggH 2J BSM',
    'M17_VBF_HjjLOW_loose'  :'VBF #font[12]{Hjj} Low-#font[12]{p}_{T}^{#font[12]{Hjj}}, loose BDT',
    'M17_VBF_HjjLOW_tight'  :'VBF #font[12]{Hjj} Low-#font[12]{p}_{T}^{#font[12]{Hjj}}, tight BDT',
    'M17_VBF_HjjHIGH_loose' :'VBF #font[12]{Hjj} High-#font[12]{p}_{T}^{#font[12]{Hjj}}, loose BDT',
    'M17_VBF_HjjHIGH_tight' :'VBF #font[12]{Hjj} High-#font[12]{p}_{T}^{#font[12]{Hjj}}, tight BDT',
    'M17_VHhad_loose'       :'VH hadronic, loose BDT',
    'M17_VHhad_tight'       :'VH hadronic, tight BDT',
    'M17_qqH_BSM'           :'qqH BSM',
    'M17_VHMET_LOW'         :'VH MET Low',
    'M17_VHMET_HIGH'        :'VH MET High/BSM Merged',
    'M17_VHMET_BSM'         :'VH MET BSM MERGED AWAY',
    'M17_VHlep_LOW'         :'VH Leptonic, Low-#font[12]{p}_{T}^{#font[12]{l+MET}}',
    'M17_VHlep_HIGH'        :'VH Leptonic, High-#font[12]{p}_{T}^{#font[12]{l+MET}}',
    'M17_VHdilep_LOW'       :'VH Dileptonic',
    'M17_VHdilep_HIGH'      :'VH Dileptonic MERGED AWAY ',
    'M17_tH_Had_4j2b'       :'ttH Hadronic 4j2b',
    'M17_tH_Had_4j1b'       :'ttH Hadronic 4j1b',
    'M17_ttH_Had_BDT4'      :'ttH Hadronic BDT4',
    'M17_ttH_Had_BDT3'      :'ttH Hadronic BDT3',
    'M17_ttH_Had_BDT2'      :'ttH Hadronic BDT2',
    'M17_ttH_Had_BDT1'      :'ttH Hadronic BDT1',
    'M17_ttH_Lep'           :'ttH Leptonic',
    'M17_tH_lep_1fwd'       :'ttH Leptonic 1fwd',
    'M17_tH_lep_0fwd'       :'ttH Leptonic 0fwd',
    }

selected_couplings2017 = {
    'M17_ggH_0J_Cen'        :'ExpPoly2',
    'M17_ggH_0J_Fwd'        :'ExpPoly2',
    'M17_ggH_1J_LOW'        :'ExpPoly2',
    'M17_ggH_1J_MED'        :'ExpPoly2',
    'M17_ggH_1J_HIGH'       :'Pow',
    'M17_ggH_1J_BSM'        :'Exponential',
    'M17_ggH_2J_LOW'        :'ExpPoly2',
    'M17_ggH_2J_MED'        :'ExpPoly2',
    'M17_ggH_2J_HIGH'       :'Pow',
    'M17_ggH_2J_BSM'        :'Pow',
    'M17_VBF_HjjLOW_loose'  :'Exponential',
    'M17_VBF_HjjLOW_tight'  :'Exponential',
    'M17_VBF_HjjHIGH_loose' :'Exponential',
    'M17_VBF_HjjHIGH_tight' :'Exponential',
    'M17_VHhad_loose'       :'Exponential',
    'M17_VHhad_tight'       :'Exponential',
    'M17_qqH_BSM'           :'Exponential',
    'M17_VHMET_LOW'         :'Exponential',
    'M17_VHMET_HIGH'        :'Exponential',
    'M17_VHMET_BSM'         :'Exponential',
    'M17_VHlep_LOW'         :'Exponential',
    'M17_VHlep_HIGH'        :'Exponential',
    'M17_VHdilep_LOW'       :'Pow',
    'M17_VHdilep_HIGH'      :'None',
    'M17_tH_Had_4j2b'       :'Pow',
    'M17_tH_Had_4j1b'       :'Pow',
    'M17_ttH_Had_BDT4'      :'Exponential',
    'M17_ttH_Had_BDT3'      :'Exponential',
    'M17_ttH_Had_BDT2'      :'Exponential',
    'M17_ttH_Had_BDT1'      :'Exponential',
    'M17_ttH_Lep'           :'Pow',
    'M17_tH_lep_1fwd'       :'Pow',
    'M17_tH_lep_0fwd'       :'Pow',
    }
                            
def BkgHistName_couplings2017(category) :
    categoryname = 'c%d_%s'%(category+1,categories_couplings2017[category])
    histname = 'HGamEventInfoAuxDyn_m_yy_over_1000_%s_AF2'%(categoryname)
    return histname

def GetDataHist_couplings2017(category,file) :
    histname = BkgHistName_couplings2017(category)
    try :
        datahist = file.Get(histname.replace('AF2','data')).Clone()
    except ReferenceError :
        histname = histname+'_clone'
        tmp = file.Get(histname.replace('AF2','data'))
        if not tmp :
            print 'Error! Hist %s does not exist. Wrong file?'%(histname)
            import sys; sys.exit()
        datahist = tmp.Clone()

    return datahist

def BkgHistName_ysy(category) :
    return 'Template_c%s'%(category+1)

def GetDataHist_ysy(category,file) :
    tmp = file.Get('Template_c%d'%(category+1))
    datahist = tmp.Clone()
    return datahist

args_bkgonly = [# ROOT.RooFit.Extended()
    #,ROOT.RooFit.Save()
    ROOT.RooFit.Offset()
    ,ROOT.RooFit.PrintEvalErrors(-1)
    ,ROOT.RooFit.Minimizer('Minuit2','migrad')
    ,ROOT.RooFit.SumW2Error(True) # limitation from MC stats
    ]

args_datalimit = [ROOT.RooFit.Extended()
                  #,ROOT.RooFit.Save()
                  ,ROOT.RooFit.Minimizer('Minuit2','migrad') # Minuit2, migrad --> minos
                  ,ROOT.RooFit.Offset()
                  ,ROOT.RooFit.PrintEvalErrors(-1)
                  ,ROOT.RooFit.SumW2Error(False) # expected in data
                  ]

args_mclimit = [ROOT.RooFit.Extended()
                #,ROOT.RooFit.Save()
#                 ,ROOT.RooFit.Minimizer('Minuit2','migrad')
                #,ROOT.RooFit.Minimizer('Minuit2'), ROOT.RooFit.Minos(True), ROOT.RooFit.Strategy(1)
                ,ROOT.RooFit.Offset()
                ,ROOT.RooFit.PrintEvalErrors(1)
                ,ROOT.RooFit.SumW2Error(True) # limitation from MC stats
                ]

plotOptions_sb = [ROOT.RooFit.Range("lower,upper"),
                  ROOT.RooFit.NormRange("lower,upper"),
                  ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative)
                  ]

plotOptions_sb_all = [ROOT.RooFit.Range("all"),
                      ROOT.RooFit.NormRange("lower,upper"),
                      ROOT.RooFit.Normalization(1.,ROOT.RooAbsReal.Relative)
                      ]

# args_mclimit_fast = [ROOT.RooFit.Extended()
#                      #,ROOT.RooFit.Save()
#                      ,ROOT.RooFit.Minimizer('Minuit2','migrad') # Minuit2, migrad --> minos
#                      #,ROOT.RooFit.Minimizer('Minuit2'), ROOT.RooFit.Minos(True), ROOT.RooFit.Strategy(1)
#                      ,ROOT.RooFit.Offset()
#                      ,ROOT.RooFit.PrintEvalErrors(-1)
#                      ,ROOT.RooFit.SumW2Error(True) # limitation from MC stats
#                      ]

##################################################################################
def DrawBox(xmin,xmax,ymin,ymax) :
    a = ROOT.TLine()
    a.DrawLine(xmin,ymin,xmax,ymin)
    a.DrawLine(xmin,ymax,xmax,ymax)
    a.DrawLine(xmin,ymin,xmin,ymax)
    a.DrawLine(xmax,ymin,xmax,ymax)
    return

##################################################################################
def ClearRooPlot(frame) :
    for i in range(int(frame.numItems())) :
        j = int(frame.numItems()) - i - 1
        #print frame.getObject(j).GetName()
        frame.remove(frame.getObject(j).GetName())

##################################################################################
def maxAbs_PreserveSign(a_list) :
    result_preserveSign = 0
    max_abs = 0
    for i,a in enumerate(a_list) :
        if math.fabs(a) > max_abs :
            max_abs = math.fabs(a)
            result_preserveSign = a
    return result_preserveSign

##################################################################################
def SetBkgToConstant(function,thebool) :
    iter = function.BkgArgList.createIterator()
    var = iter.Next()
    while var :
        #print var.GetName(),var.isConstant()
        if var.GetName() == 'm_yy' :
            var = iter.Next()
            continue
        #print var.GetName(),var.isConstant(),type(var)
        var.setConstant(thebool)
        #print var.GetName(),var.isConstant(),type(var)
        var = iter.Next()
    return

##################################################################################
def snapshot(function) :
    initial_state = dict()
    pars = function.getParameters(ROOT.RooArgSet())
    iter = pars.createIterator()
    var = iter.Next()
    while var :
        #print var.GetName(),var.isConstant()
        if var.GetName() == 'm_yy' :
            var = iter.Next()
            continue
        #print var.GetName(),var.isConstant(),type(var)
        initial_state[var.GetName()] = var.getVal()
        var = iter.Next()
    return initial_state

##################################################################################
def reset_to_snapshot(function,initial_state) :
    pars = function.getParameters(ROOT.RooArgSet())
    iter = pars.createIterator()
    var = iter.Next()
    while var :
        #print var.GetName(),var.isConstant()
        if var.GetName() == 'm_yy' :
            var = iter.Next()
            continue
        #print var.GetName(),var.isConstant(),type(var)
        var.setVal(initial_state[var.GetName()])
        var = iter.Next()
    return

##################################################################################
def printArgs(arglist,name='',doprint=True) :
    text = ''
    
    for i in range(len(arglist)) :
        if arglist[i].isConstant() :
            continue
        if arglist[i].GetName() == 'm_yy' :
            continue
        text += '%-3s: %2.8f \pm %2.8f %s '%(arglist[i].GetName(),arglist[i].getVal(),arglist[i].getError(),arglist[i].isConstant())
    if doprint :
        print text
    return text

##################################################################################
def printArgSetArgs(argSet,nest='') :
    iter = argSet.createIterator()
    var = iter.Next()
    while var :
        print nest+' ',var.GetName(),type(var),var.getVal(),'isConstant:',var.isConstant(),
        if hasattr(var,'getMin') :
            print 'min',var.getMin(),'max',var.getMax()
        else :
            print 
        var = iter.Next()
    return

##################################################################################
def PrintRooThing(thing,nest='') :
    print nest+thing.GetName(),type(thing)
    
    if hasattr(thing,'getComponents') : # a RooAbsArg function
        print nest+'Components:'
        printArgSetArgs(thing.getComponents(),nest=nest)
        iter = thing.getComponents().createIterator()
        var = iter.Next()
        while var :
            if var == thing :
                var = iter.Next()
                continue
            PrintRooThing(var,nest=nest+'   ')
            var = iter.Next()
    if hasattr(thing,'getVariables') : # a RooAbsArg function
        print nest+'Variables:'
        printArgSetArgs(thing.getVariables(),nest=nest)

    return

##################################################################################
def GetMaxBinError(hist,binmin,binmax) :
    the_max = 0
    #print 'nbinsx:',hist.GetNbinsX()
    for i in range(hist.GetNbinsX()) :
        if hist.GetBinCenter(i+1) < binmin :
            continue
        if hist.GetBinCenter(i+1) > binmax :
            continue
        if hist.GetBinContent(i+1) == 0 :
            the_max = 2
            continue
        err = hist.GetBinError(i+1)/hist.GetBinContent(i+1)
        if err > the_max :
            the_max = err
    return the_max

    # rebin until your smallest error is uh small

##################################################################################
def FindRebinFactors(hist) :
    # find factors
    factors = []
    for bin in range(hist.GetNbinsX()) :
        if bin < 2 :
            continue
        if hist.GetNbinsX() / float(bin) == hist.GetNbinsX() / bin :
            factors.append(bin)
    # print 'Possible rebin factors:',factors
    return factors

##################################################################################
def RebinUntilSmallErrors(hist1,hist2,binmin,binmax,errormax=0.3,do_rebin=True) :

    factors = FindRebinFactors(hist1)

    for fac in factors :
        blah = hist1.Clone()
        blah.SetName('blah')
        blah.Rebin(fac)

        blah2 = 0
        if hist2 :
            blah2 = hist2.Clone()
            blah2.SetName('blah2')
            blah2.Rebin(fac)

        if GetMaxBinError(blah,binmin,binmax) > errormax :
            continue
        if blah2 and GetMaxBinError(blah2,binmin,binmax) > errormax :
            continue
        # print 'picked',fac
        if do_rebin :
            if hist2 :
                hist2.Rebin(fac)
            hist1.Rebin(fac)
            # print 'rebinned'
        break
    # print 'fac',fac
    return fac

##################################################################################
def BlindThePull(graph) :
    from array import array
    if False :
        return ROOT.TGraphAsymmErrors(1,array('d',[1]),array('d',[1])
                                      ,array('d',[1]),array('d',[1])
                                      ,array('d',[1]),array('d',[1])
                                      )
    
    x = graph.GetX()
    y = graph.GetY()
    n = graph.GetN()
    yeh = graph.GetEYhigh()
    yel = graph.GetEYlow()
    xeh = graph.GetEXhigh()
    xel = graph.GetEXlow()

    x1 = []
    xeh1 = []
    xel1 = []
    y1 = []
    yeh1 = []
    yel1 = []
    ey1 = []
    n1 = 0
    
    for i in range(n) :
        if (119 < x[i]) and (x[i] < 131) :
            continue
        #if (x[i] > 150) :
        #    continue
        x1.append(x[i])
        y1.append(y[i])
        xeh1.append(xeh[i])
        xel1.append(xel[i])
        yeh1.append(yeh[i])
        yel1.append(yel[i])
        n1 += 1

    #print x1
    #print y1
    tmp = ROOT.TGraphAsymmErrors(n1,array('d',x1),array('d',y1)
                                 ,array('d',xel1),array('d',xeh1)
                                 ,array('d',yel1),array('d',yeh1)
                                 )
    tmp.SetName(graph.GetName()+'_graph')
    return tmp

##################################################################################
def DivideCurves(curve1,curveref) :
    from array import array
    if False :
        return ROOT.TGraph(1,array('d',[1]),array('d',[1]))
    n = 0
    y1 = curve1.GetY()
    y2 = curveref.GetY()
    ratio = []
    for i in range(curveref.GetN()) :
        if y2[i] == 0 :
            continue
        if math.isnan(y1[i]) :
            continue
        #print 'y1[i]',y1[i],'y2[i]',y2[i]
        ratio.append(y1[i]/y2[i])
        n += 1
    if ratio == [] :
        return 0
    t = ROOT.TGraph(n,curve1.GetX(),array('d',ratio))
    t.SetName(curve1.GetName()+'diff')
    return t

##################################################################################
def GetPullDist(graph) :
    h = ROOT.TH1F(graph.GetName()+'hist',graph.GetName(),200,-30,30);
    y = graph.GetY()
    for i in range(graph.GetN()) :
        h.Fill(y[i])
    return h


##################################################################################
class GetPackage :

    def GetSignal(self) :
        signalwsfile = ROOT.TFile(self.signalwsfilename,'READ')
        if signalwsfile.IsZombie() :
            print 'Error! File %s has a problem. Exiting.'%(self.signalwsfilename); import sys; sys.exit()
        tmpsignalWS = signalwsfile.Get('signalWS')
        # tmpsignalWS.importClassCode()
        tmpsignalpdf = tmpsignalWS.pdf("sigPdf_SM_m125000_c%d"%(self.category)) # Me: sigPdf_SM_m125000_c Marc: sigPdf_Hyy_m125000_c28 

        #PrintRooThing(tmpsignalpdf)
#         self.signalpdf = tmpsignalpdf        

#         import sys; sys.exit()

        argset = tmpsignalpdf.getVariables()
        iter = argset.createIterator()
        var = iter.Next()
        while var :
            if var.GetName() == 'm_yy_m125000_c%d'%(self.category) :
                var = iter.Next()
                continue
            #print var.GetName(),type(var),var.getVal(),'isConstant:',var.isConstant()
            tmpname = var.GetName().replace('_SM_m125000_c%d'%(self.category),'').replace('_SM_c%d'%(self.category),'')
            #print 'Adding %s to workspace'%tmpname
            #workspacearg = '%s[0,0,1]'%(tmpname)
            workspacearg = '%s[%2.3f,%2.3f,%2.3f]'%(tmpname,var.getVal(),var.getMin(),var.getMax())
            #print workspacearg
            #self.BkgArgList.add(self.workspace.factory(workspacearg))
            self.workspace.factory(workspacearg)
            self.workspace.var(tmpname).setConstant(True)
            self.workspace.var(tmpname).setVal(var.getVal())
            self.workspace.var(tmpname).setRange(var.getMin(),var.getMax())
            var = iter.Next()

        #print "Final result"
        #printArgSetArgs(self.BkgArgList)
        #print "Final result"

        self.workspace.var('muCBNom').setRange(100,200)

        #myy = 'm_yy_m125000_c%d'%(self.category)
        self.signalpdf = self.workspace.factory("HggTwoSidedCBPdf::sigPdf(m_yy, prod::muCB(muCBNom), prod::sigmaCB(sigmaCBNom), alphaCBLo, nCBLo, alphaCBHi, nCBHi)")
        if not self.signalpdf :
            # Try RooTwoSidedCBShape instead of HggTwoSidedCBPdf
            self.signalpdf = self.workspace.factory("RooTwoSidedCBShape::sigPdf(m_yy, prod::muCB(muCBNom), prod::sigmaCB(sigmaCBNom), alphaCBLo, nCBLo, alphaCBHi, nCBHi)")
        if not self.signalpdf :
            print('Error - signal pdf workspace factory call failed')
            import sys; sys.exit()

        self.smsignalyield = tmpsignalWS.var("sigYield_SM_m125000_c%d"%(self.category))
        #print 'setting signal yield to',self.smsignalyield.getVal()

        return 

    def Initialize(self) :
        
        if not hasattr(self,'analysis') :
            print 'ERROR: Initialize AFTER you set the analysis.'; import sys; sys.exit()
        if not hasattr(self,'category') :
            print 'ERROR: Initialize AFTER you set the category.'; import sys; sys.exit()
        if not hasattr(self,'filename') :
            print 'ERROR: Initialize AFTER you set the filename.'; import sys; sys.exit()
        if not hasattr(self,'signalwsfilename') :
            print 'Warning: Initialize AFTER you set the signalws. Proceeding without one';

        #
        # get the data
        #
        f = ROOT.TFile(self.filename)
        if f.IsZombie() :
            print 'Error! File %s does not exist. Exiting.'%(self.filename)
            import sys; sys.exit()

        # Get the data hist
        if self.analysis == 'couplings2017' :
            self.datahist = GetDataHist_couplings2017(self.category,f)
            self.af2hist = f.Get(BkgHistName_couplings2017(self.category)).Clone()

        elif self.analysis == 'ysy' :
            self.datahist = GetDataHist_ysy(self.category,f)
            self.af2hist = f.Get(BkgHistName_ysy(self.category)).Clone()

        else :
            print('Error - unrecognized analysis %s'%(self.analysis))
            import sys; sys.exit()

        self.datahist.SetDirectory(0)
        self.af2hist.SetDirectory(0)
        self.af2hist_not_rebinned = self.af2hist.Clone()
        self.af2hist_not_rebinned.SetName(self.af2hist_not_rebinned.GetName()+'_not_rebinned')
        self.af2hist_not_rebinned.SetDirectory(0)
        self.af2hist.SetName('af2hist_%s'%(self.name))
#         self.higgshist = f.Get(histname.replace('AF2','Higgs')).Clone()
#         self.higgshist.SetDirectory(0)
#         self.higgshist.SetName('higgshist_%s'%(self.name))
        self.integral = self.af2hist.Integral(self.af2hist.FindBin(self.lower_range+0.0001),self.af2hist.FindBin(self.upper_range-0.000001))
        binwidth = self.af2hist.GetBinWidth(1)
        self.bins = int((self.upper_range-self.lower_range)/float(binwidth))
        #print 'binwidth:',binwidth,'bins:',self.bins
        #print 'Integral:',self.integral
        self.obsVar.setBins(int(self.bins)) # was 600
        self.data = ROOT.RooDataHist('data','',ROOT.RooArgList(self.obsVar),self.af2hist,1.)
        self.data_realdata = ROOT.RooDataHist('data','',ROOT.RooArgList(self.obsVar),self.datahist,1.)
        f.Close()

        #
        # Get the signal
        #
        #signalwsfile = ROOT.TFile('res_SM_DoubleCB_workspace_me.root','READ')
        # signalwsfile = ROOT.TFile('res_SM_DoubleCB_workspace_marc.root','READ')
        #self.signalWS = signalwsfile.Get('signalWS')
        #self.signalpdf = self.signalWS.pdf("sigPdf_SM_m125000_c%d"%(category))
        if hasattr(self,'signalwsfilename') and self.signalwsfilename :
            self.GetSignal()
            self.MakeTotalPdf()
        
        #print self.signalpdf

    def PrintParameters(self) :
        text = ''
        #self.workspace.var("muCBNom").setVal(125)
        #self.totalPdf.fitTo(self.data,*args_mclimit)
        text += '%-10s: '%(self.name)
        text += printArgs(self.BkgArgList,doprint=False)
        return text

    def SetAnalysis(self,analysis) :
        self.analysis = analysis

    def SetCategory(self,category) :
        self.category = int(category)

    def SetFileName(self,filename) :
        self.filename = filename

    def SetSignalWS(self,filename) :
        self.signalwsfilename = filename

    def __init__(self,name,ndof,lower,upper) :

        self.lower_range = lower
        self.upper_range = upper

        self.lower_blind = 120
        self.upper_blind = 130

        self.chisquare = -1
        self.ndof = ndof
        self.name = name
        self.workspace = ROOT.RooWorkspace(name,"")

        # Make the RooRealVar obsVar (m_yy)
        self.obsVar = self.workspace.factory('m_yy[%d,%d]'%(self.lower_range,self.upper_range))
        #self.obsVar_rebinned = self.workspace.factory('m_yy[%d,%d]'%(lower_range,upper_range))

        self.obsVar.setRange("lower",self.lower_range,self.lower_blind) ; 
        self.obsVar.setRange("upper",self.upper_blind,self.upper_range) ; 
        self.obsVar.setRange("all",self.lower_range,self.upper_range) ; 

        self.frame = self.obsVar.frame()

        #self.frame_rebinned = self.obsVar_rebinned.frame()

        self.BkgArgList = ROOT.RooArgList('parlist_%s'%(name))
        self.BkgArgList.add(self.obsVar)

        self.SignalNormalization = self.workspace.factory('nSignal[0,-500,2000]')
        self.BkgNormalization    = self.workspace.factory('nBkg[100,0,1E7]')

        tmpname = self.name+' Dummy x^-4'
        self.nomfunction = ROOT.RooGenericPdf(tmpname,tmpname,'1/(m_yy*m_yy*m_yy*m_yy)',self.BkgArgList)
        #getattr(self.workspace,'import')(self.nomfunction)
        
        return
    
    def MakeTotalPdf(self) :
        self.totalPdf = ROOT.RooAddPdf(self.name+'_total_pdf','s+b',ROOT.RooArgList(self.signalpdf,self.function),ROOT.RooArgList(self.SignalNormalization,self.BkgNormalization))
        getattr(self.workspace,'import')(self.totalPdf)

        return

    def AddBkgFunction(self,expression) :
        self.function = ROOT.RooGenericPdf(self.name,self.name,expression,self.BkgArgList)
        getattr(self.workspace,'import')(self.function)
        #self.function_ext = ROOT.RooAddPdf(self.name+'_extended','b_ext',ROOT.RooArgList(self.function),ROOT.RooArgList(self.BkgNormalization))
        #self.function_ext = ROOT.RooExtendPdf(self.name+'_extended','b_ext',self.function,self.BkgNormalization)
        self.function_ext = self.workspace.factory("SUM::model(nBkg_ext[20,0,1E7]*%s)"%(self.name))
        return

    def AddSpecial(self,expression) :
        self.function = self.workspace.factory(expression)
        return

    def TotalError(self) :
        self.total_error = math.sqrt(self.deltas_relative**2 + self.max_spur_signalmu**2)
        return self.total_error

    def RunTests(self) :
        self.passes_nominal   =  (math.fabs(self.max_spur_signalmu           ) < 0.1) or (math.fabs(self.max_spur_signalz           ) < 0.2)
        self.passes_1sig_chi2 = ((math.fabs(self.max_spur_signalmu_compatible) < 0.1) or (math.fabs(self.max_spur_signalz_compatible) < 0.2)) and (self.pvalue_chi2 > 0.01)
        return

    def PrintSpuriousSignalStudy(self,
                                 skipHeader=False,
                                 doInjectionBias=False,
                                 doToyBias=False,
                                 doToyBiasNoSignal=False,
                                 doNominalSpTest=False,
                                 doRelaxedSpTest=True,
                                 doCompatibilityMu=True,
                                 doCompatibilityZ=True,
                                 ) :

        if not hasattr(self,'toyBiasHist_fitResults') :
            self.toyBiasHist_fitResults = [1,0,0,0,0,0,0]
            self.ntoys_failed = -1
        if not hasattr(self,'toyBiasHist_fitResults_nosig') :
            self.toyBiasHist_fitResults_nosig = [0,0,0,0,0,0,0]
            self.ntoys_failed_nosig = -1

        # If they have not been run already,
        # check the different spurious signal test flavors
        self.RunTests()

        header = ''
        text = ''

        header += '{:<15} '.format('Function Name')
        text += '{:<15} '.format(self.name)

        header += '{:>9} '.format('chi2')
        text += '{:9.3g} '.format(self.chisquare)

        header += '{:>10} '.format('p(chi2)')
        text += '{:9.3g}% '.format(self.pvalue_chi2*100.)

        header += '{:>9} '.format('Nspur')
        text += '{:9.3g} '.format(self.nspur)

        header += '{:>10} '.format('Sspur/DS')
        text += '{:9.3g}% '.format(self.max_spur_signalz*100.)

        header += '{:>10} '.format('Sspur/Ssmh')
        text += '{:9.3g}% '.format(self.max_spur_signalmu*100)

        if doInjectionBias :
            header += '{:>10} '.format('inj bias')
            text += '{:9.2f}% '.format(self.max_bias_signalmu*100.)

        if doToyBias :
            header += '{:>15} '.format('Toy bias')
            text += '{:5.2f} '.format((self.toyBiasHist_fitResults[0]-1.0)*100)
            text += '+/-'
            text += '{:5.2f}% '.format((self.toyBiasHist_fitResults[1])*100)

        if doToyBiasNoSignal :
            header += '{:>15} '.format('Toy bias NoSig')
            text += '{:5.2f} '.format((self.toyBiasHist_fitResults_nosig[0])*100)
            text += '+/-'
            text += '{:5.2f}% '.format((self.toyBiasHist_fitResults_nosig[1])*100)

        if doNominalSpTest :
            header += '{:>10} '.format('pass Nom')
            text += '{:>10} '.format('PASS' if self.passes_nominal else 'FAIL')

        if doRelaxedSpTest :
            header += '{:>10} '.format('1sig,chi2')
            text += '{:>10} '.format('PASS' if self.passes_1sig_chi2 else 'FAIL')

        if doCompatibilityMu :
            header += '{:>10} '.format('Relax spur')
            text += '{:9.3g}% '.format(self.max_spur_signalmu_compatible*100.)

        if doCompatibilityZ :
            header += '{:>10} '.format('Relax DS')
            text += '{:9.3g}% '.format(self.max_spur_signalz_compatible*100.)

        header += '{:>10} '.format('stat err')
        text += '{:9.3g}% '.format(self.deltas_relative*100)

        header += '{:>10} '.format('tot err')
        text += '{:9.3g}% '.format(self.TotalError()*100)

        header += '\n'

        if not skipHeader :
            text = header + text

        return text

    def PrintAdditionalStatInfo(self) :
        text = ''
        if not hasattr(self,'toyBiasHist_fitResults') :
            self.toyBiasHist_fitResults = [0,0,0,0,0,0,0]
            self.ntoys_failed = -1
        if not hasattr(self,'toyBiasHist_fitResults_nosig') :
            self.toyBiasHist_fitResults_nosig = [0,0,0,0,0,0,0]
            self.ntoys_failed_nosig = -1
        tmp = '{:<15} {:9.2f}% {:9.2f}% {:6.2f}+{:4.2f}% {:9.2f}% {:9.2f}% {:6.2f}+{:4.2f}% {:6d} {:6d}'
        tmp = tmp.format(self.name
                         ,self.deltas_relative*100
                         ,(self.toyBiasHist_fitResults_nosig[4])*100 # mean reported error of toys
                         ,(self.toyBiasHist_fitResults_nosig[2])*100 # fitted sigma of all toys
                         ,(self.toyBiasHist_fitResults_nosig[3])*100 # fitted sigma of all toys (error)
                         ,self.injectionerror_rel*100
                         ,(self.toyBiasHist_fitResults[4])*100 # mean reported error of toys
                         ,(self.toyBiasHist_fitResults[2])*100 # fitted sigma of all toys
                         ,(self.toyBiasHist_fitResults[3])*100 # fitted sigma of all toys (error)
                         ,self.ntoys_failed
                         ,self.ntoys_failed_nosig
#                          ,self.chisquare_sb
#                          ,self.pvalue_chi2_sb
                         )
        text += tmp
        print text
        return text

# end of class.

##################################################################################
def ToyInjectedSignalBias(function,rel_error_for_hist,inject_signal=True) :
    flag = 'inject_signal' if inject_signal else 'no_signal'
    offset = 1 if inject_signal else 0
    # Based on the number of expected data events!
    asimov = ROOT.RooHistPdf("asdf","asdf",ROOT.RooArgSet(function.obsVar),function.data)
    asimov_bkg = function.workspace.var('asimov_bkg')
    if not asimov_bkg :
        asimov_bkg = function.workspace.factory('asimov_bkg[%5.5f,0,1E6]'%(function.integral))
    asimov_sig = function.workspace.var('asimov_sig')
    if not asimov_sig :
        asimov_sig = function.workspace.factory('asimov_sig[%5.5f,0,1E6]'%(function.smsignalyield.getVal()))
    asimov_total = ROOT.RooAddPdf(function.name+'_total_pdf_asimov','b_extended',ROOT.RooArgList(asimov),ROOT.RooArgList(asimov_bkg))
    asimov_signal = ROOT.RooAddPdf(function.name+'_total_pdf_signal','s_extended',ROOT.RooArgList(function.signalpdf),ROOT.RooArgList(asimov_sig))
    #asimov_total.fitTo(function.data)

    toyBkgErrorHist = 0
    toyBiasHist     = 0
    ntoys_failed    = 0

    # DO NOT USE THIS injecteddata = asimov_signal.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.ExpectedData(),ROOT.RooFit.Name('tmp_injecteddata'))

    print 'Throwing 20000 toys...'
    for i in range(20000) :
        if not i%100 : print i
        asimov_data = asimov_total.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.Extended(),ROOT.RooFit.Name("tmp_asimov_data_%d_%s"%(i,function.name)))
        function.workspace.var("muCBNom").setVal(125)
        function.workspace.var('nSignal').setVal(0)
        if inject_signal :
            # add a specific number of signal events
            injecteddata = asimov_signal.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.Extended(),ROOT.RooFit.Name('tmp_injecteddata_%d_%s'%(i,function.name)))
            asimov_data.add(injecteddata)

        initial_state = snapshot(function)
        #result = function.totalPdf.fitTo(asimov_data,ROOT.RooFit.Warnings(False),ROOT.RooFit.PrintLevel(-1),ROOT.RooFit.Save(),*args_datalimit)
        function.totalPdf.fitTo(asimov_data,ROOT.RooFit.Warnings(False),ROOT.RooFit.PrintLevel(-1),*args_datalimit)
        # ROOT.RooFit.PrintLevel(-1)
        # ROOT.RooFit.PrintEvalErrors(-1)
        #print 'Actual:',function.smsignalyield.getVal(),'fit:',function.workspace.var("nSignal").getVal()
        
        rel_error = function.workspace.var('nSignal').getError()/asimov_sig.getVal()
        if not toyBkgErrorHist :
            toyBkgErrorHist = ROOT.TH1F('%s_toyBkgErrorHist_%s'%(function.name,flag),'toy bkg error',1000,0,rel_error_for_hist*3)
            toyBiasHist     = ROOT.TH1F('%s_toyBiasHist_%s'%(function.name,flag)    ,'toy bias'     ,100,offset-rel_error_for_hist*5,offset+rel_error_for_hist*5)
        else :
            #if (result.status() == 0) :
            if True :
                toyBkgErrorHist.Fill(rel_error)
                toyBiasHist.Fill(function.workspace.var('nSignal').getVal()/asimov_sig.getVal())
            else :
                ntoys_failed += 1

        reset_to_snapshot(function,initial_state)
#         del result
#         del asimov_data
#         ROOT.gROOT.ProcessLine('delete tmp_asimov_data_%d_%s'%(i,function.name))
#         if inject_signal :
#             del injecteddata
#             ROOT.gROOT.ProcessLine('delete tmp_injecteddata_%d_%s'%(i,function.name))

#         print asimov_data.GetName()
#         print injecteddata.GetName()
#         print asimov_data
#         print injecteddata

    print 'Throwing toys done.'
    
    c = ROOT.TCanvas('c%02d_toy_study_%s_%s'%(function.category,function.name,flag),"toy study results, %s (%s)"%(function.name,flag),600,500)
    toyBiasHist.Fit('gaus')
    c.GetPrimitive('%s_toyBiasHist_%s'%(function.name,flag)).SetDrawOption('pE1')
    result = toyBiasHist.GetFunction('gaus')
    print 'Mean:',result.GetParameter(1),'Error on mean:',result.GetParError(1),'sigma:',result.GetParameter(2),'Error on sigma:',result.GetParError(2)

    print 'Toy Bkg Error hist mean and rms: %2.5f, %2.5f'%(toyBkgErrorHist.GetMean(),toyBkgErrorHist.GetRMS())

    if False:
        asimov_data.plotOn(function.frame,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
        function.totalPdf.plotOn(function.frame)
        function.frame.Draw()
        c2 = ROOT.TCanvas()
        toyBkgErrorHist.Draw()
        d = ROOT.TCanvas('d','d',600,500)
        toyBiasHist.Draw()
        raw_input('wait')

    if inject_signal :
        function.toyBiasHist = toyBiasHist
        function.toyBkgErrorHist = toyBkgErrorHist
        function.toyBiasHist_fitResults = [result.GetParameter(1),result.GetParError(1),result.GetParameter(2),result.GetParError(2),toyBkgErrorHist.GetMean()]
        function.ntoys_failed = ntoys_failed
    else :
        function.toyBiasHist_nosig = toyBiasHist
        function.toyBkgErrorHist_nosig = toyBkgErrorHist
        function.toyBiasHist_fitResults_nosig = [result.GetParameter(1),result.GetParError(1),result.GetParameter(2),result.GetParError(2),toyBkgErrorHist.GetMean()]
        function.ntoys_failed_nosig = ntoys_failed

    return c


##################################################################################
def GetInjectedSignalBias(function,mass=125) :
    tmpbkg = function.workspace.var("nBkg").getVal()
    function.workspace.var("nBkg").setVal(0)
    function.workspace.var("nSignal").setVal(function.smsignalyield.getVal())
    function.workspace.var("muCBNom").setVal(mass)

    injecteddata = function.totalPdf.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.ExpectedData())

    function.workspace.var("nBkg").setVal(tmpbkg)
    function.workspace.var("nSignal").setVal(0)
    
    injecteddata.add(function.data)
    function.totalPdf.fitTo(injecteddata,*args_datalimit) # to be revisited

    if mass == 125 :
        function.injectionerror_rel = function.workspace.var("nSignal").getError()/float(function.smsignalyield.getVal())

    del injecteddata
    function.workspace.var("muCBNom").setVal(125)
    return math.fabs(1.-function.workspace.var("nSignal").getVal()/float(function.smsignalyield.getVal()))

##################################################################################
def GetSignalBiasMuScan(function,color=ROOT.kBlack) :
    import PlotFunctions as plotfunc
    from array import array
    x = []
    y = []
    xe = []
    ye = []
    yup = []
    ydn = []
    bias_signalmu = []
    for i in range(function.lower_range,function.upper_range+1) :
        #function.workspace.var("muCBNom").setVal(i)
        #function.totalPdf.fitTo(function.data,*args_mclimit)
        GetInjectedSignalBias(function,mass=i)

        x.append(i)
        xe.append(0)

        signal_yield = float(function.smsignalyield.getVal())
        error_data = function.workspace.var("nSignal").getError()
        signal_bias = function.workspace.var("nSignal").getVal()

        y.append(signal_bias/signal_yield-1.)
        ye.append(error_data/signal_yield)

        yup.append((signal_bias+error_data)/signal_yield-1.)
        ydn.append((signal_bias-error_data)/signal_yield-1.)

        if i >= 121 and i <= 129 :
            bias_signalmu.append(y[-1])
        #print i,'spurious signal:',function.workspace.var("nSignal").getVal()

    function.signalbiasmu = ROOT.TGraphErrors(len(x),array('d',x),array('d',y)
                                                  ,array('d',xe),array('d',ye)
                                                  )
    function.signalbiasmu.SetName('%s SigBias Mu'%(function.name))
    function.signalbiasmu.SetTitle(function.name)

    function.signalbiasmucv = ROOT.TGraph(len(x),array('d',x),array('d',y))
    function.signalbiasmucv.SetName('%s SigBias Mu cv'%(function.name))
    function.signalbiasmucv.SetTitle(function.name)
    function.signalbiasmucv.SetLineWidth(2)

    function.signalbiasmuup = ROOT.TGraph(len(x),array('d',x),array('d',yup)) 
    function.signalbiasmuup.SetName('%s SigBias Mu up'%(function.name))
    function.signalbiasmuup.SetTitle(function.name+'up remove')

    function.signalbiasmudn = ROOT.TGraph(len(x),array('d',x),array('d',ydn))
    function.signalbiasmudn.SetName('%s SigBias Mu dn'%(function.name))
    function.signalbiasmudn.SetTitle(function.name+'dn remove')

    function.signalbiasmucv.SetFillColor(color)
    function.signalbiasmucv.SetLineColor(color)
    function.signalbiasmuup.SetLineColorAlpha(color,0.3)
    function.signalbiasmudn.SetLineColorAlpha(color,0.3)

#     print 'signalmu',spur_signalmu
#     print 'signalerr',spur_signalerr
#     if max(spur_signalmu) <= 0.1 :
#         print 'PASS'
#     else :
#         print 'FAIL'

    function.max_bias_signalmu = maxAbs_PreserveSign(bias_signalmu)
    return maxAbs_PreserveSign(bias_signalmu)

##################################################################################
def GetSpuriousSignalMu(function,isFFT=False,color=ROOT.kBlack) :
    import PlotFunctions as plotfunc
    from array import array
    x = []
    y = []
    xe = []
    ye = []
    yup = []
    ydn = []
    spur_signalmu = []
    y_comp = []
    spur_signalmu_comp = []
    signal_yield = float(function.smsignalyield.getVal())

    for j in range(function.lower_range*10,(function.upper_range+1)*10,5) :
        i = j/10.
        function.workspace.var("muCBNom").setVal(i)
        if isFFT :
            function.totalPdf.fitTo(function.data_fft,*args_mclimit)
        else :
            #print 'Spurious signal mu',i
            function.totalPdf.fitTo(function.data,*args_mclimit)
            #var = function.workspace.var("nSignal")
            #print 'INFO: Error options:',var.getError(),var.getAsymErrorLo(),var.getAsymErrorHi(),var.getErrorHi(),var.getErrorLo(),result.status()
            #del result

            # ok. let's try to fix the bkg parameters now, and refit using mclimit to get the signal
            # error.
            SetBkgToConstant(function,True)
            function.totalPdf.fitTo(function.data,*args_mclimit)

        error_data = function.workspace.var("nSignal").getError()
        spurious_yield = function.workspace.var("nSignal").getVal()

        if i < (function.lower_range + 5) or i > (function.upper_range - 5) :
            SetBkgToConstant(function,False)
            continue

        x.append(i)
        xe.append(0)

        y.append(spurious_yield/signal_yield)
        ye.append(error_data/signal_yield)

        yup.append((spurious_yield+error_data)/signal_yield)
        ydn.append((spurious_yield-error_data)/signal_yield)

        tmp_y_comp = 0
        if spurious_yield-error_data > 0 :
            tmp_y_comp = spurious_yield-error_data
        elif spurious_yield+error_data < 0 :
            tmp_y_comp = spurious_yield+error_data
        y_comp.append(tmp_y_comp/signal_yield)

        if i >= 121 and i <= 129 :
            spur_signalmu.append(y[-1])
            spur_signalmu_comp.append(y_comp[-1])
        #print i,'spurious signal:',function.workspace.var("nSignal").getVal()

        SetBkgToConstant(function,False)

    if isFFT :
        #print 'populating SS mu fft'
        function.spurioussignalmu_fft = ROOT.TGraphErrors(len(x),array('d',x),array('d',y)
                                                      ,array('d',xe),array('d',ye)
                                                      )
        function.spurioussignalmu_fft.SetName('%s SS Mu (fft)'%(function.name))
        function.spurioussignalmu_fft.SetTitle(function.name+' (fft)')
        function.spurioussignalmu_fft.GetYaxis().SetTitle('S_{spur}/S_{SM}')
        function.spurioussignalmu_fft.GetXaxis().SetTitle('m_{#gamma#gamma}')

    else :
        function.spurioussignalmu = ROOT.TGraphErrors(len(x),array('d',x),array('d',y)
                                                      ,array('d',xe),array('d',ye)
                                                      )
        function.spurioussignalmu.SetName('%s SS Mu'%(function.name))
        function.spurioussignalmu.SetTitle(function.name)

        function.spurioussignalmucv = ROOT.TGraph(len(x),array('d',x),array('d',y))
        function.spurioussignalmucv.SetName('%s SS Mu cv'%(function.name))
        function.spurioussignalmucv.SetTitle(function.name)
        function.spurioussignalmucv.SetLineWidth(2)

        function.spurioussignalmuup = ROOT.TGraph(len(x),array('d',x),array('d',yup)) 
        function.spurioussignalmuup.SetName('%s SS Mu up'%(function.name))
        function.spurioussignalmuup.SetTitle(function.name+'up remove')

        function.spurioussignalmudn = ROOT.TGraph(len(x),array('d',x),array('d',ydn))
        function.spurioussignalmudn.SetName('%s SS Mu dn'%(function.name))
        function.spurioussignalmudn.SetTitle(function.name+'dn remove')
        
        function.spurioussignalmucv.SetFillColor(color)
        function.spurioussignalmucv.SetLineColor(color)
        function.spurioussignalmuup.SetLineColorAlpha(color,0.3)
        function.spurioussignalmudn.SetLineColorAlpha(color,0.3)

        function.spurioussignalmucomp = ROOT.TGraph(len(x),array('d',x),array('d',y_comp))
        function.spurioussignalmucomp.SetName('%s SS Mu compatibility'%(function.name))
        function.spurioussignalmucomp.SetTitle(function.name)
        function.spurioussignalmucomp.SetLineWidth(2)
        function.spurioussignalmucomp.SetFillColor(color)
        function.spurioussignalmucomp.SetLineColor(color)

#     print 'signalmu',spur_signalmu
#     print 'signalerr',spur_signalerr
#     if max(spur_signalmu) <= 0.1 :
#         print 'PASS'
#     else :
#         print 'FAIL'

    function.max_spur_signalmu_compatible = maxAbs_PreserveSign(spur_signalmu_comp)
    function.max_spur_signalmu = maxAbs_PreserveSign(spur_signalmu)
    function.nspur = function.max_spur_signalmu * signal_yield
    return function.max_spur_signalmu


##################################################################################
def GetSpuriousSignalZ(function,color=ROOT.kBlack,lower_range=110,upper_range=160) :
    import PlotFunctions as plotfunc
    from array import array
    x = []
    y = []
    xe = []
    ye = []
    yup = []
    ydn = []
    spur_signalz = []
    y_comp = []
    spur_signalz_comp = []

    for i in range(lower_range,upper_range) :
        function.workspace.var("muCBNom").setVal(i)
        function.totalPdf.fitTo(function.data,*args_datalimit)
        S_fit = function.workspace.var("nSignal").getVal()
        DS_fit = float(function.workspace.var("nSignal").getError())
        if DS_fit == 0 :
            continue
        #print 'Spurious signal Z',i
        function.totalPdf.fitTo(function.data,*args_mclimit)
        SetBkgToConstant(function,True)
        function.totalPdf.fitTo(function.data,*args_mclimit)
        DS_mc = function.workspace.var("nSignal").getError()
        SetBkgToConstant(function,False)

        if i < (function.lower_range + 5) or i > (function.upper_range - 5) :
            SetBkgToConstant(function,False)
            continue

        x.append(i)
        xe.append(0)
        y.append(S_fit/DS_fit)
        ye.append(DS_mc/DS_fit)
        yup.append((S_fit+DS_mc)/DS_fit)
        ydn.append((S_fit-DS_mc)/DS_fit)
        #print i,'spurious signal:',function.workspace.var("nSignal").getVal()

        # significance
        tmp_y_comp = 0
        if S_fit-DS_mc > 0 :
            tmp_y_comp = S_fit-DS_mc
        elif S_fit+DS_mc < 0 :
            tmp_y_comp = S_fit+DS_mc
        y_comp.append(tmp_y_comp/DS_fit)

        if i >= 121 and i <= 129 :
            spur_signalz.append(y[-1])
            spur_signalz_comp.append(y_comp[-1])

    function.spurioussignalz = ROOT.TGraphErrors(len(x),array('d',x),array('d',y)
                                                  ,array('d',xe),array('d',ye)
                                                  )
    function.spurioussignalz.SetName('%s SS Mu'%(function.name))
    function.spurioussignalz.SetTitle(function.name)

    function.spurioussignalzcv = ROOT.TGraph(len(x),array('d',x),array('d',y))
    function.spurioussignalzcv.SetName('%s SS Mu cv'%(function.name))
    function.spurioussignalzcv.SetTitle(function.name)
    function.spurioussignalzcv.SetLineWidth(2)

    function.spurioussignalzup = ROOT.TGraphErrors(len(x),array('d',x),array('d',yup))
    function.spurioussignalzup.SetName('%s SS Mu up'%(function.name))
    function.spurioussignalzup.SetTitle(function.name+'up remove')

    function.spurioussignalzdn = ROOT.TGraphErrors(len(x),array('d',x),array('d',ydn))
    function.spurioussignalzdn.SetName('%s SS Mu dn'%(function.name))
    function.spurioussignalzdn.SetTitle(function.name+'dn remove')

    function.spurioussignalzcv.SetFillColor(color)
    function.spurioussignalzcv.SetLineColor(color)
    function.spurioussignalzup.SetLineColorAlpha(color,0.3)
    function.spurioussignalzdn.SetLineColorAlpha(color,0.3)

    function.spurioussignalzcomp = ROOT.TGraph(len(x),array('d',x),array('d',y_comp))
    function.spurioussignalzcomp.SetName('%s SS Z compatibility'%(function.name))
    function.spurioussignalzcomp.SetTitle(function.name)
    function.spurioussignalzcomp.SetLineWidth(2)
    function.spurioussignalzcomp.SetFillColor(color)
    function.spurioussignalzcomp.SetLineColor(color)

    function.max_spur_signalz = maxAbs_PreserveSign(spur_signalz)
    function.max_spur_signalz_compatible = maxAbs_PreserveSign(spur_signalz_comp)
    return maxAbs_PreserveSign(spur_signalz)

##################################################################################
def GetDeltaS_Relative(function) :
    function.workspace.var("muCBNom").setVal(125)
    function.totalPdf.fitTo(function.data,*args_datalimit)
    var = function.workspace.var("nSignal")
    #print 'INFO: Error options:',var.getError(),var.getAsymErrorLo(),var.getAsymErrorHi()
    function.deltas_relative = function.workspace.var("nSignal").getError()/float(function.smsignalyield.getVal())
    return float(function.deltas_relative)


##################################################################################
def SetFamilyColors(can,flist) :
    import PlotFunctions as plotfunc
    
    n = 0; step = 0
    famcolors = plotfunc.KurtColorPalate()
    nfam = 0
    alphafam = dict()

    can.SetLeftMargin(0.09)
    can.SetRightMargin(0.25)
    plotfunc.MakeLegend(can,.76,.9 - 0.024*len(flist) ,.98,.9)

    for i in can.GetListOfPrimitives() :
        ikey = i.GetName()[:3]
        if hasattr(i,'SetMarkerColorAlpha') :
            if ikey not in alphafam.keys() :
                alphafam[ikey] = dict()
                alphafam[ikey]['n'] = 1
                alphafam[ikey]['step'] = 0
                alphafam[ikey]['color'] = famcolors[nfam]
                #print 'making for key',ikey,famcolors[nfam]
                nfam += 1
            else :
                alphafam[ikey]['n'] += 1
    for i in can.GetListOfPrimitives() :
        ikey = i.GetName()[:3]
        if hasattr(i,'SetMarkerColorAlpha') and alphafam[ikey]['n'] > 1 :
            #print .05 + alphafam[ikey]['step']*.95/(alphafam[ikey]['n'] - 1)
            i.SetLineColorAlpha(alphafam[ikey]['color'],.05 + alphafam[ikey]['step']*.95/(alphafam[ikey]['n'] - 1))
            alphafam[ikey]['step'] += 1
        elif hasattr(i,'SetMarkerColor') :
            i.SetLineColor(alphafam[ikey]['color'])

    return
