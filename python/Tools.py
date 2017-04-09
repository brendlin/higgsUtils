
import ROOT
import math
import PlotFunctions as plotfunc

lower_range = 105
upper_range = 160
ur = upper_range

categories = [
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
#    'M17_ttH',               # 25
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

CategoryNames = {
    'Inclusive'             :'Inclusive',
    'M17_ggH_0J_Cen'        :'ggH 0J Central'   ,       
    'M17_ggH_0J_Fwd'        :'ggH 0J Forward'   ,       
    'M17_ggH_1J_LOW'        :'ggH 1J Low'       ,       
    'M17_ggH_1J_MED'        :'ggH 1J Med'       ,       
    'M17_ggH_1J_HIGH'       :'ggH 1J High'      ,      
    'M17_ggH_1J_BSM'        :'ggH 1J BSM'       ,       
    'M17_ggH_2J_LOW'        :'ggH 2J Low'       ,       
    'M17_ggH_2J_MED'        :'ggH 2J Med'       ,       
    'M17_ggH_2J_HIGH'       :'ggH 2J High'      ,      
    'M17_ggH_2J_BSM'        :'ggH 2J BSM'       ,       
    'M17_VBF_HjjLOW_loose'  :'VBF #font[12]{Hjj} Low-#font[12]{p}_{T}^{#font[12]{Hjj}}, loose BDT' , 
    'M17_VBF_HjjLOW_tight'  :'VBF #font[12]{Hjj} Low-#font[12]{p}_{T}^{#font[12]{Hjj}}, tight BDT' , 
    'M17_VBF_HjjHIGH_loose' :'VBF #font[12]{Hjj} High-#font[12]{p}_{T}^{#font[12]{Hjj}}, loose BDT',
    'M17_VBF_HjjHIGH_tight' :'VBF #font[12]{Hjj} High-#font[12]{p}_{T}^{#font[12]{Hjj}}, tight BDT',
    'M17_VHhad_loose'       :'VH hadronic, loose BDT'      ,      
    'M17_VHhad_tight'       :'VH hadronic, tight BDT'      ,      
    'M17_qqH_BSM'           :'qqH BSM'          ,          
    'M17_VHMET_LOW'         :'VH MET Low',
    'M17_VHMET_HIGH'        :'VH MET High/BSM Merged',
    'M17_VHMET_BSM'         :'VH MET BSM',
    'M17_VHlep_LOW'         :'VH Leptonic, Low-#font[12]{p}_{T}^{#font[12]{l+MET}}',
    'M17_VHlep_HIGH'        :'VH Leptonic, High-#font[12]{p}_{T}^{#font[12]{l+MET}}',
    'M17_VHdilep_LOW'       :'VH Dileptonic',
    }

selected = {
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
    'M17_VHlep_LOW'         :'Pow',
    'M17_VHlep_HIGH'        :'Exponential',
    'M17_VHdilep_LOW'       :'Pow',
    }
                            

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
    pars = function.totalPdf.getParameters(ROOT.RooArgSet())
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
    pars = function.totalPdf.getParameters(ROOT.RooArgSet())
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
def printArgs(arglist,name='') :
    text = ''
    
    for i in range(len(arglist)) :
        if arglist[i].isConstant() :
            continue
        if arglist[i].GetName() == 'm_yy' :
            continue
        text += '%-5s: %2.8f \pm %2.8f %s '%(arglist[i].GetName(),arglist[i].getVal(),arglist[i].getError(),arglist[i].isConstant())
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

        self.smsignalyield = tmpsignalWS.var("sigYield_SM_m125000_c%d"%(self.category))
        #print 'setting signal yield to',self.smsignalyield.getVal()

        return 

    def Initialize(self) :
        
        if not hasattr(self,'category') :
            print 'ERROR: Initialize AFTER you set the category.'; import sys; sys.exit()
        if not hasattr(self,'filename') :
            print 'ERROR: Initialize AFTER you set the filename.'; import sys; sys.exit()
        if not hasattr(self,'signalwsfilename') :
            print 'ERROR: Initialize AFTER you set the signalws.'; import sys; sys.exit()

        #
        # get the data
        #
        f = ROOT.TFile(self.filename)
        categoryname = 'c%d_%s'%(self.category+1,categories[self.category])
        histname = 'HGamEventInfoAuxDyn_m_yy_over_1000_%s_AF2'%(categoryname)
        #print 'Using HGamEventInfoAuxDyn_m_yy_over_1000_c0_Inclusive_data'
        #self.datahist = f.Get('HGamEventInfoAuxDyn_m_yy_over_1000_c0_Inclusive_AF2').Clone()
        try :
            self.datahist = f.Get(histname.replace('AF2','data')).Clone()
        except ReferenceError :
            histname = histname+'_clone'
            self.datahist = f.Get(histname.replace('AF2','data')).Clone()
        self.datahist.SetDirectory(0)
        self.af2hist = f.Get(histname).Clone()
        self.af2hist.SetDirectory(0)
        self.af2hist_not_rebinned = self.af2hist.Clone()
        self.af2hist_not_rebinned.SetName(self.af2hist_not_rebinned.GetName()+'_not_rebinned')
        self.af2hist_not_rebinned.SetDirectory(0)
        self.af2hist.SetName('af2hist_%s'%(self.name))
#         self.higgshist = f.Get(histname.replace('AF2','Higgs')).Clone()
#         self.higgshist.SetDirectory(0)
#         self.higgshist.SetName('higgshist_%s'%(self.name))
        self.integral = self.af2hist.Integral(self.af2hist.FindBin(lower_range+0.0001),self.af2hist.FindBin(upper_range-0.000001))
        binwidth = self.af2hist.GetBinWidth(1)
        self.bins = int((upper_range-lower_range)/float(binwidth))
        #print 'binwidth:',binwidth,'bins:',self.bins
        print 'Integral:',self.integral
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
        self.GetSignal()
        self.MakeTotalPdf()
        
        #print self.signalpdf

    def PrintParameters(self) :
        text = ''
        self.workspace.var("muCBNom").setVal(125)
        self.totalPdf.fitTo(self.data,*args_mclimit)
        text += '%-10s: '%(self.name)
        text += printArgs(self.BkgArgList)
        return text

    def SetCategory(self,category) :
        self.category = int(category)

    def SetFileName(self,filename) :
        self.filename = filename

    def SetSignalWS(self,filename) :
        self.signalwsfilename = filename

    def __init__(self,name,ndof) :

        self.chisquare = -1
        self.ndof = ndof
        self.name = name
        self.workspace = ROOT.RooWorkspace(name,"")

        # Make the RooRealVar obsVar (m_yy)
        self.obsVar = self.workspace.factory('m_yy[%d,%d]'%(lower_range,upper_range))
        #self.obsVar_rebinned = self.workspace.factory('m_yy[%d,%d]'%(lower_range,upper_range))

        self.obsVar.setRange("lower",lower_range,120) ; 
        self.obsVar.setRange("upper",130,upper_range) ; 
        self.obsVar.setRange("all",105,upper_range) ; 

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
        #self.function_ext = ROOT.RooAddPdf(self.name+'_extended','b_ext',ROOT.RooArgList(self.function),ROOT.RooArgList(self.BkgNormalization))
        self.function_ext = ROOT.RooExtendPdf(self.name+'_extended','b_ext',self.function,self.BkgNormalization)
        getattr(self.workspace,'import')(self.function_ext)
        return

    def AddSpecial(self,expression) :
        self.function = self.workspace.factory(expression)
        return

    def TotalError(self) :
        self.total_error = math.sqrt(self.deltas_relative**2 + self.max_spur_signalmu**2)
        return self.total_error

    def PrintSpuriousSignalStudy(self) :
        if not hasattr(self,'toyBiasHist_fitResults') :
            self.toyBiasHist_fitResults = [1,0,0,0,0,0,0]
            self.ntoys_failed = -1
        if not hasattr(self,'toyBiasHist_fitResults_nosig') :
            self.toyBiasHist_fitResults_nosig = [0,0,0,0,0,0,0]
            self.ntoys_failed_nosig = -1
        text = ''
        self.passes = (math.fabs(self.max_spur_signalmu) < 0.1) or (math.fabs(self.max_spur_signalz) < 0.2)
        #self.passes_new = ((math.fabs(self.max_spur_signalmu_compatible) < 0.1) or (math.fabs(self.max_spur_signalz_compatible) < 0.2)) and (self.pvalue_chi2 > 0.05)
        self.passes_new = ((math.fabs(self.max_spur_signalmu_compatible) < 0.1) or (math.fabs(self.max_spur_signalz_compatible) < 0.2))
        tmp = '{:<15} {:9.2f}% {:9.2f}% {:5.2f}+{:5.2f}% {:5.2f}+{:5.2f}% {:9.2f}% {:^6} {:9.2f}% {:9.2f}% {:10.5f} {:10.5f} {:10.5f} {:^6} XXX'
        #tmp = '%<15s %10.3f %10.3f %6s %10.3f %10.5f %10.5f %10.5f %6s'
        tmp = tmp.format(self.name
                         ,self.max_spur_signalmu*100.
                         ,self.max_bias_signalmu*100. # in range 121-129
                         ,(self.toyBiasHist_fitResults[0]-1.0)*100 # toy bias
                         ,(self.toyBiasHist_fitResults[1])*100 # toy bias error
                         ,(self.toyBiasHist_fitResults_nosig[0])*100 # toy bias (no signal)
                         ,(self.toyBiasHist_fitResults_nosig[1])*100 # toy bias error (no signal)
                         ,self.max_spur_signalz*100.
                         ,('PASS' if self.passes else 'FAIL')
                         ,self.max_spur_signalmu_compatible*100.
                         ,self.max_spur_signalz_compatible*100.
                         ,self.chisquare
                         ,self.pvalue_chi2
                         ,self.TotalError()
                         ,('PASS' if self.passes_new else 'FAIL')
                         #,self.minNll
                         )
        text += tmp
        print text
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
def GetFFTVersion2(function) :
    from array import array
    ROOT.TVirtualFFT.SetTransform(0)

    # fit off most of the background
    function.nomfunction.fitTo(function.data,*args_bkgonly)
    function.data.plotOn(function.frame)
    function.nomfunction.plotOn(function.frame)

#     c = ROOT.TCanvas('asdf','asdf',500,500)
#     function.frame.Draw()

    # get the residual hist and the curve
    residgraph_before_fft = function.frame.residHist()
    rough_fit_curve = function.frame.getCurve()

    #tmp = ROOT.TCanvas()
    #residgraph_before_fft.Draw('ap')
    #rough_fit_curve.Draw('p')

    # fill the histogram that will be fft'd
    function.residhist_before_fft = ROOT.TH1F(function.name+'_residhist_before_fft','residhist_before_fft',function.bins,lower_range,upper_range)
    for i in range(residgraph_before_fft.GetN()) :
        function.residhist_before_fft.SetBinContent(i+1,residgraph_before_fft.GetY()[i])

    # do the fft
    ffthist = 0
    ffthist = function.residhist_before_fft.FFT(ffthist,"MAG M")
    ffthist.SetName(function.name+'_internal_fft_hist')
    ffthist.SetTitle("fft")
    fft = ROOT.TVirtualFFT.GetCurrentTransform()

    re_array = array('d',[0]*function.hist.GetNbinsX())
    im_array = array('d',[0]*function.hist.GetNbinsX())
    fft.GetPointsComplex(re_array,im_array)

    fft_back = ROOT.TVirtualFFT.FFT(1,fft.GetN(), "C2R M K");

    for i in range(len(re_array)) :
        if i < 5 :
            continue
        re_array[i] = 0
        im_array[i] = 0

    fft_back.SetPointsComplex(re_array,im_array)

    fft_back.Transform();
    hist_truncated = 0
    hist_truncated = ROOT.TH1.TransformHisto(fft_back,hist_truncated,"Re");
    hist_truncated.SetName(function.name+'truncated_output')
    #print 'hist_truncated:',hist_truncated.GetNbinsX(),hist_truncated.GetBinLowEdge(1),hist_truncated.GetBinLowEdge(hist_truncated.GetNbinsX()+1)

    #print 'nbins: hist_truncated:',hist_truncated.GetNbinsX(),'rough_fit_curve:',rough_fit_curve.GetN(),
    #print 'function.residhist_before_fft:',function.residhist_before_fft.GetNbinsX(),
    #print 'residgraph_before_fft:',residgraph_before_fft.GetN()

    # make the resulting fft histogram
    function.fft = function.residhist_before_fft.Clone()
    function.fft.SetName(function.hist.GetName()+'_fft')
    function.fft.SetTitle(function.hist.GetTitle()+' fft')
    for i in range(hist_truncated.GetNbinsX()) :
        function.fft.SetBinContent(i+1,hist_truncated.GetBinContent(i+1))
        function.fft.SetBinError(i+1,0)
    #print function.residhist_before_fft.Integral()/float(function.fft.Integral())
    function.fft.Scale(function.residhist_before_fft.Integral()/float(function.fft.Integral()))
    # add back the function
    for i in range(function.fft.GetNbinsX()) :
        #print 'adding',rough_fit_curve.GetY()[i]
        function.fft.AddBinContent(i+1,rough_fit_curve.Eval(function.fft.GetBinCenter(i+1)))
        function.fft.SetBinError(i+1,0.001)

    # make an outsize version of the fft histogram
    function.fft_x10 = function.residhist_before_fft.Clone()
    function.fft_x10.SetName(function.hist.GetName()+'_fftx10')
    function.fft_x10.SetTitle(function.hist.GetTitle()+' fft x10')
    for i in range(hist_truncated.GetNbinsX()) :
        function.fft_x10.SetBinContent(i+1,hist_truncated.GetBinContent(i+1))
        function.fft_x10.SetBinError(i+1,0)
    function.fft_x10.Scale(5*function.residhist_before_fft.Integral()/float(function.fft_x10.Integral()))
    for i in range(function.fft_x10.GetNbinsX()) :
        #print 'adding',rough_fit_curve.GetY()[i]
        function.fft_x10.AddBinContent(i+1,rough_fit_curve.Eval(function.fft_x10.GetBinCenter(i+1)))
        function.fft_x10.SetBinError(i+1,0.001)


#     function.hist.Draw()
#     function.fft.Draw('sames')
#     raw_input('asdf')

    function.data_fft = ROOT.RooDataHist('data','',ROOT.RooArgList(function.obsVar),function.fft,1.)
    function.data_fft_x10 = ROOT.RooDataHist('data','',ROOT.RooArgList(function.obsVar),function.fft_x10,1.)

    #print 'fft done.'
    return

##################################################################################
def GetFFT(function) :
    from array import array
    ROOT.TVirtualFFT.SetTransform(0)
    ffthist = 0
    ffthist = function.hist.FFT(ffthist,"MAG M")
    ffthist.SetTitle("fft")
    fft = ROOT.TVirtualFFT.GetCurrentTransform()

    re_array = array('d',[0]*function.hist.GetNbinsX())
    im_array = array('d',[0]*function.hist.GetNbinsX())
    fft.GetPointsComplex(re_array,im_array)
    # print re_array, im_array

    fft_back = ROOT.TVirtualFFT.FFT(1,fft.GetN(), "C2R M K");

    for i in range(len(re_array)) :
        if i < 10 :
            continue
        re_array[i] = 0
        im_array[i] = 0

    fft_back.SetPointsComplex(re_array,im_array)

    fft_back.Transform();
    hist_truncated = 0
    hist_truncated = ROOT.TH1.TransformHisto(fft_back,hist_truncated,"Re");
    #print 'hist_truncated:',hist_truncated.GetNbinsX(),hist_truncated.GetBinLowEdge(1),hist_truncated.GetBinLowEdge(hist_truncated.GetNbinsX()+1)

    function.fft = function.hist.Clone()
    function.fft.SetName(function.hist.GetName()+'_fft')
    function.fft.SetTitle(function.hist.GetTitle()+' fft')
    for i in range(hist_truncated.GetNbinsX()) :
        function.fft.SetBinContent(i+1,hist_truncated.GetBinContent(i+1))
    function.fft.Scale(function.hist.Integral()/float(function.fft.Integral()))

    function.data_fft = ROOT.RooDataHist('data','',ROOT.RooArgList(function.obsVar),function.fft,1.)

    print 'fft done.'
    return

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
def GetSignalBiasMuScan(function,index=0) :
    import PlotFunctions as plotfunc
    colors = plotfunc.KurtColorPalate()
    from array import array
    x = []
    y = []
    xe = []
    ye = []
    yup = []
    ydn = []
    bias_signalmu = []
    for i in range(lower_range,upper_range+1) :
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

    function.signalbiasmucv.SetFillColor(colors[index])
    function.signalbiasmucv.SetLineColor(colors[index])         
    function.signalbiasmuup.SetLineColorAlpha(colors[index],0.3)
    function.signalbiasmudn.SetLineColorAlpha(colors[index],0.3)

#     print 'signalmu',spur_signalmu
#     print 'signalerr',spur_signalerr
#     if max(spur_signalmu) <= 0.1 :
#         print 'PASS'
#     else :
#         print 'FAIL'

    function.max_bias_signalmu = maxAbs_PreserveSign(bias_signalmu)
    return maxAbs_PreserveSign(bias_signalmu)

##################################################################################
def GetSpuriousSignalMu(function,isFFT=False,index=0) :
    import PlotFunctions as plotfunc
    colors = plotfunc.KurtColorPalate()
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
    for j in range(lower_range*10,(upper_range+1)*10,5) :
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

#         import sys; sys.exit()
        x.append(i)
        xe.append(0)

        signal_yield = float(function.smsignalyield.getVal())
        error_data = function.workspace.var("nSignal").getError()
        spurious_yield = function.workspace.var("nSignal").getVal()

#         if i == 121 :
#             printArgs(function.BkgArgList)
#             print error_data

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
        
        function.spurioussignalmucv.SetFillColor(colors[index])
        function.spurioussignalmucv.SetLineColor(colors[index])
        function.spurioussignalmuup.SetLineColorAlpha(colors[index],0.3)
        function.spurioussignalmudn.SetLineColorAlpha(colors[index],0.3)

        function.spurioussignalmucomp = ROOT.TGraph(len(x),array('d',x),array('d',y_comp))
        function.spurioussignalmucomp.SetName('%s SS Mu compatibility'%(function.name))
        function.spurioussignalmucomp.SetTitle(function.name)
        function.spurioussignalmucomp.SetLineWidth(2)
        function.spurioussignalmucomp.SetFillColor(colors[index])         
        function.spurioussignalmucomp.SetLineColor(colors[index])         

#     print 'signalmu',spur_signalmu
#     print 'signalerr',spur_signalerr
#     if max(spur_signalmu) <= 0.1 :
#         print 'PASS'
#     else :
#         print 'FAIL'

    function.max_spur_signalmu_compatible = maxAbs_PreserveSign(spur_signalmu_comp)
    function.max_spur_signalmu = maxAbs_PreserveSign(spur_signalmu)
    return max(spur_signalmu)


##################################################################################
def GetSpuriousSignalZ(function,index=0) :
    import PlotFunctions as plotfunc
    colors = plotfunc.KurtColorPalate()
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

    for i in range(110,160) :
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

    function.spurioussignalzcv.SetFillColor(colors[index])
    function.spurioussignalzcv.SetLineColor(colors[index])
    function.spurioussignalzup.SetLineColorAlpha(colors[index],0.3)
    function.spurioussignalzdn.SetLineColorAlpha(colors[index],0.3)

    function.spurioussignalzcomp = ROOT.TGraph(len(x),array('d',x),array('d',y_comp))
    function.spurioussignalzcomp.SetName('%s SS Z compatibility'%(function.name))
    function.spurioussignalzcomp.SetTitle(function.name)
    function.spurioussignalzcomp.SetLineWidth(2)
    function.spurioussignalzcomp.SetFillColor(colors[index])
    function.spurioussignalzcomp.SetLineColor(colors[index])

    function.max_spur_signalz = maxAbs_PreserveSign(spur_signalz)
    function.max_spur_signalz_compatible = maxAbs_PreserveSign(spur_signalz_comp)
    return maxAbs_PreserveSign(spur_signalz)

##################################################################################
def GetDeltaS_Relative(function) :
    function.workspace.var("muCBNom").setVal(125)
    function.totalPdf.fitTo(function.data,*args_datalimit)
    var = function.workspace.var("nSignal")
    print 'INFO: Error options:',var.getError(),var.getAsymErrorLo(),var.getAsymErrorHi()
    function.deltas_relative = function.workspace.var("nSignal").getError()/float(function.smsignalyield.getVal())
    return float(function.deltas_relative)

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
def PopulateFunctionList(functions,flist) :

    if 'Exponential' in flist :
        # Exponential
        functions.append(GetPackage('Exponential',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1))')

    if 'ExpPoly2' in flist :
        # ExpPoly2
        functions.append(GetPackage('ExpPoly2',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-10,10]'))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*a2) )')

    if 'ExpPoly2ndDOF' in flist :
        # ExpPoly2 with only x^2
        functions.append(GetPackage('ExpPoly2ndDOF'),1)
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('b1[-50,-100,100]'))
        functions[-1].AddBkgFunction('exp((m_yy - b1)/b1*(a1*(m_yy - b1)/b1))')

    if 'ExpPoly3' in flist :
        # ExpPoly3
        functions.append(GetPackage('ExpPoly3',3))
        for i in range(3) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('ep3%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(ep31 + (m_yy - 100)/100*(ep32 + (m_yy - 100)/100*ep33 ) ))')

    if 'ExpPoly4' in flist :
        # ExpPoly4
        functions.append(GetPackage('ExpPoly4',4))
        for i in range(4) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*a4 ) )))')

    if 'ExpPoly5' in flist :
        # ExpPoly5
        functions.append(GetPackage('ExpPoly5',5))
        for i in range(5) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*a5 )) ) ))')

    if 'ExpPoly6' in flist :
        # ExpPoly6
        functions.append(GetPackage('ExpPoly6',6))
        for i in range(6) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*a6 )) ) )))')

    if 'ExpPoly7' in flist :
        # ExpPoly7
        functions.append(GetPackage('ExpPoly7',7))
        for i in range(7) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*a7) )) ) )))')

    if 'ExpPoly8' in flist :
        # ExpPoly8
        functions.append(GetPackage('ExpPoly8',8))
        for i in range(8) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*a8)) )) ) )))')

    if 'ExpPoly9' in flist :
        # ExpPoly9
        functions.append(GetPackage('ExpPoly9',9))
        for i in range(9) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*(a8 + (m_yy - 100)/100*a9))) )) ) )))')

    if 'ExpPoly10' in flist :
        # ExpPoly10
        functions.append(GetPackage('ExpPoly10',10))
        for i in range(10) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*(a8 + (m_yy - 100)/100*(a9 + (m_yy - 100)/100*a10)))) )) ) )))')


    if 'Laurent0' in flist :
        # 1/x^4
        functions.append(GetPackage('Laurent0',0))
        functions[-1].AddBkgFunction('1/(m_yy*m_yy*m_yy*m_yy)')

    if 'Laurent1' in flist :
        # 1/x^4 + 1/x^5
        functions.append(GetPackage('Laurent1',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].AddBkgFunction('1/(m_yy*m_yy*m_yy*m_yy)+100*a1/(m_yy*m_yy*m_yy*m_yy*m_yy)')

    if 'Laurent2' in flist :
        # 1/x^4 + 1/x^5
        functions.append(GetPackage('Laurent2',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-10,10]'))
        functions[-1].AddBkgFunction('1/(m_yy*m_yy*m_yy*m_yy)+100*a1/(m_yy*m_yy*m_yy*m_yy*m_yy) + 0.01*a2/(m_yy*m_yy*m_yy)')

    if '1/x^4 + a' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('1/x^4 + a',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1')

    if '1/x^4 + a + bx' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('1/x^4 + a + bx',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-100,100]'))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy - %d)'%(ur))

    if '1/x^4 + poly3' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('1/x^4 + poly3',3))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-100,100]'))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2'%(ur,ur))

    if '1/x^4 + poly4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('1/x^4 + poly4',4))
        for i in range(4) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-100,100]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2 + a4*(m_yy-%d)**3'%(ur,ur,ur))

    if '1/x^4 + poly5' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('1/x^4 + poly5',5))
        for i in range(5) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-100,100]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2 + a4*(m_yy-%d)**3 + a5*(m_yy-%d)**4'%(ur,ur,ur,ur))

    if '1/x^4 + poly6' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('1/x^4 + poly6',6))
        for i in range(6) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1000,1000]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2 + a4*(m_yy-%d)**3 + a5*(m_yy-%d)**4 + a6*(m_yy-%d)**5'%(ur,ur,ur,ur,ur))

    if 'poly1/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('poly1/x^4',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-1,1]'))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy - %d))/(m_yy*m_yy*m_yy*m_yy)'%(ur))

    if 'poly2/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('poly2/x^4',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-1,1]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-1,1]'))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur))

    if 'poly3/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('poly3/x^4',3))
        for i in range(3) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur))

    if 'poly4/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('poly4/x^4',4))
        for i in range(4) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3 + a4*(m_yy-%d)**4)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur))

    if 'poly5/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('poly5/x^4',5))
        for i in range(5) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3 + a4*(m_yy-%d)**4 + a5*(m_yy-%d)**5)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur,ur))

    if 'poly6/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('poly6/x^4',6))
        for i in range(6) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3 + a4*(m_yy-%d)**4 + a5*(m_yy-%d)**5 + a6*(m_yy-%d)**6)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur,ur,ur))

    if 'poly7/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(GetPackage('poly7/x^4',7))
        for i in range(7) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + 0.001*a2*(m_yy-%d)**2 + 0.0001*a3*(m_yy-%d)**3 + 0.000001*a4*(m_yy-%d)**4 + 0.00000001*a5*(m_yy-%d)**5 + 0.00000001*a6*(m_yy-%d)**6 + 0.000000001*a7*(m_yy-%d)**7)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur,ur,ur,ur))


    extent = upper_range-lower_range
    x = '((m_yy-%s)/%s)'%(lower_range,extent)

    if 'Bernstein_3' in flist :
    #     # My Bernstein 3
        functions.append(GetPackage('Bernstein_3',3))
        for i in range(3) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
            #functions[-1].AddBkgFunction(ROOT.RooGenericPdf(name,name,'(1-%s)**3 + a1*%s*(1-%s)**2 + a2*3*(%s**2)*(1-%s) + a3*%s**3'%(x,x,x,x,x,x),functions[-1].BkgArgList))
            functions[-1].AddBkgFunction('%s**3 + 3*a1*%s**2*(1-%s) + 3*a2*%s*(1-%s)**2 + a3*(%s)**3'%(x,x,x,x,x,x))

#     if 'Bernstein 3' in flist :
#         # Bernstein 3
#         functions.append(GetPackage('Bernstein 3'),3)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], 1 })')

#     if 'Bernstein_4' in flist :
#     #     # My Bernstein 4
#         functions.append(GetPackage('Bernstein_4',4))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-.9,.9]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-.9,.9]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-.9,.9]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a4[0,-.9,.9]'))
#         functions[-1].AddBkgFunction('a4*%s**4 + 4*a3*(1-%s)*%s**3 + 6*a2*(%s**2)*(1-%s)**2 + 4*a1*%s*(1-%s)**3 + (1-%s)**4'%(x,x,x,x,x,x,x,x))

    if 'Bernstein_4' in flist :
        # Bernstein 4
        functions.append(GetPackage('Bernstein 4',4))
        functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], c4[0,-10,10], 1 })')
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c1'))
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c2'))
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c3'))
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c4'))

    if 'Bernstein_5' in flist :
        # My Bernstein 5
        functions.append(GetPackage('Bernstein_5',5))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a4[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a5[0,-.9,.9]'))
        functions[-1].AddBkgFunction('a5*%s**5 + 5*a4*(1-%s)*%s**4 + 10*a3*(%s**3)*(1-%s)**2 + 10*a2*(%s**2)*(1-%s)**3 + 5*a1*%s*(1-%s)**4 + (1-%s)**5'%(x,x,x,x,x,x,x,x,x,x))

#     if 'Bernstein 5' in flist :
#         # Bernstein 5
#         functions.append(GetPackage('Bernstein 5'),5)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-1,1], c2[0,-1,1], c3[0,-1,1], c4[0,-1,1], c5[0,-1,1], 1 })')

#     if 'Bernstein 6' in flist :
#         # Bernstein 6
#         functions.append(GetPackage('Bernstein 6'),6)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], c4[0,-10,10], c5[0,-10,10], c6[0,-10,10] 1 })')

    if 'Pow' in flist :
        functions.append(GetPackage('Pow',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,0]'))
        functions[-1].AddBkgFunction('pow(m_yy,a1)')

    if 'Pow2' in flist :
        functions.append(GetPackage('Pow2',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10, 0]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0, -2, 2]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-10,10]'))
        functions[-1].AddBkgFunction('pow(m_yy,a1) + a2*pow(m_yy,a3)')

    return


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
