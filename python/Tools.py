
import ROOT
import math

lower_range = 105
upper_range = 165
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

args_bkgonly = [# ROOT.RooFit.Extended()
    #,ROOT.RooFit.Save()
    ROOT.RooFit.Offset()
    ,ROOT.RooFit.PrintEvalErrors(-1)
    ,ROOT.RooFit.SumW2Error(True) # limitation from MC stats
    ]

args_datalimit = [ROOT.RooFit.Extended()
                  #,ROOT.RooFit.Save()
                  ,ROOT.RooFit.Offset()
                  ,ROOT.RooFit.PrintEvalErrors(-1)
                  ,ROOT.RooFit.SumW2Error(False) # expected in data
                  ]
                  
args_mclimit = [ROOT.RooFit.Extended()
                #,ROOT.RooFit.Save()
                ,ROOT.RooFit.Offset()
                ,ROOT.RooFit.PrintEvalErrors(-1)
                ,ROOT.RooFit.SumW2Error(True) # limitation from MC stats
                ]

##################################################################################
def SetBkgToConstant(function,thebool) :
    iter = function.BkgArgList.createIterator()
    var = iter.Next()
    while var :
        #print var.GetName(),var.isConstant()
        if var.GetName() == 'm_yy' :
            var = iter.Next()
            continue
        #print var.GetName(),var.isConstant()
        var.setConstant(thebool)
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
        text += '%-5s: %2.8f \pm %2.8f  '%(arglist[i].GetName(),arglist[i].getVal(),arglist[i].getError())
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
        signalwsfile = ROOT.TFile('res_SM_DoubleCB_workspace_me.root','READ')
        tmpsignalWS = signalwsfile.Get('signalWS')
        tmpsignalpdf = tmpsignalWS.pdf("sigPdf_Hyy_m125000_c%d"%(self.category))
        PrintRooThing(tmpsignalpdf)
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
            tmpname = var.GetName().replace('_Hyy_m125000_c%d'%(self.category),'').replace('_Hyy_c%d'%(self.category),'')
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

        self.smsignalyield = tmpsignalWS.var("sigYield_Hyy_m125000_c%d"%(self.category))
        #print 'setting signal yield to',self.smsignalyield.getVal()

        return 

    def Initialize(self) :
        
        if not hasattr(self,'category') :
            print 'ERROR: Initialize AFTER you set the category.'
            import sys; sys.exit()

        #
        # get the data
        #
        f = ROOT.TFile('couplings.root')
        categoryname = 'c%d_%s'%(self.category+1,categories[self.category])
        histname = 'HGamEventInfoAuxDyn_m_yy_over_1000_%s_AF2'%(categoryname)
        self.datahist = f.Get(histname.replace('AF2','data')).Clone()
        self.datahist.SetDirectory(0)
        self.af2hist = f.Get(histname).Clone()
        self.af2hist.SetDirectory(0)
        self.af2hist.SetName('af2hist_%s'%(self.name))
        self.higgshist = f.Get(histname.replace('AF2','Higgs')).Clone()
        self.higgshist.SetDirectory(0)
        self.higgshist.SetName('higgshist_%s'%(self.name))
        integral = self.af2hist.Integral()
        binwidth = self.af2hist.GetBinWidth(1)
        self.bins = int((upper_range-lower_range)/float(binwidth))
        self.rebin = 5
        self.bins_rebinned = int(self.bins/self.rebin)
        #print 'binwidth:',binwidth,'bins:',self.bins
        #print 'Integral:',integral
        self.obsVar.setBins(int(self.bins)) # was 600
        self.obsVar_rebinned.setBins(self.bins_rebinned)
        self.data = ROOT.RooDataHist('data','',ROOT.RooArgList(self.obsVar),self.af2hist,1.)

        hist_rebinned = self.af2hist.Clone()
        hist_rebinned.SetName(hist_rebinned.GetName()+'_rebinned')
        hist_rebinned.Rebin(self.rebin)
        self.data_rebinned = ROOT.RooDataHist('data_rebinned','',ROOT.RooArgList(self.obsVar_rebinned),hist_rebinned,1.)
        self.data_rebinned.plotOn(self.frame_rebinned)
        f.Close()

        #
        # Get the signal
        #
        #signalwsfile = ROOT.TFile('res_SM_DoubleCB_workspace_me.root','READ')
        # signalwsfile = ROOT.TFile('res_SM_DoubleCB_workspace_marc.root','READ')
        #self.signalWS = signalwsfile.Get('signalWS')
        #self.signalpdf = self.signalWS.pdf("sigPdf_Hyy_m125000_c%d"%(category))
        self.GetSignal()
        self.MakeTotalPdf()
        self.selectedpdf = self.totalPdf
        
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

    def __init__(self,name,ndof) :

        self.chisquare = -1
        self.ndof = ndof
        self.name = name
        self.workspace = ROOT.RooWorkspace(name,"")

        # Make the RooRealVar obsVar (m_yy)
        self.obsVar = self.workspace.factory('m_yy[%d,%d]'%(lower_range,upper_range))
        self.obsVar_rebinned = self.workspace.factory('m_yy[%d,%d]'%(lower_range,upper_range))

        self.obsVar.setRange("lower",lower_range,119) ; 
        self.obsVar.setRange("upper",131,upper_range) ; 
        self.obsVar.setRange("all",105,upper_range) ; 

        self.frame = self.obsVar.frame()

        self.frame_rebinned = self.obsVar_rebinned.frame()

        self.BkgArgList = ROOT.RooArgList('parlist_%s'%(name))
        self.BkgArgList.add(self.obsVar)

        self.SignalNormalization = self.workspace.factory('nSignal[0,-500,2000]')
        self.BkgNormalization    = self.workspace.factory('nBkg[100,0,1E6]')

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
        return

    def AddSpecial(self,expression) :
        self.function = self.workspace.factory(expression)
        return

    def TotalError(self) :
        self.total_error = math.sqrt(self.deltas_relative**2 + self.max_spur_signalmu**2)
        return self.total_error

    def PrintSpuriousSignalStudy(self) :
        text = ''
        self.passes = (self.max_spur_signalmu < 0.1) or (self.max_spur_signalz < 0.2)
        self.passes_new = ((self.max_spur_signalmu_compatible < 0.1) or (self.max_spur_signalz < 0.2)) and (self.pvalue_chi2 > 0.05)
        tmp = '{:<15} {:10.3f} {:10.3f} {:^6} {:10.3f} {:10.5f} {:10.5f} {:10.5f} {:^6} {:10.5f}'
        #tmp = '%<15s %10.3f %10.3f %6s %10.3f %10.5f %10.5f %10.5f %6s'
        tmp = tmp.format(self.name
                         ,self.max_spur_signalmu
                         ,self.max_spur_signalz
                         ,('PASS' if self.passes else 'FAIL')
                         ,self.max_spur_signalmu_compatible
                         ,self.chisquare
                         ,self.pvalue_chi2
                         ,self.TotalError()
                         ,('PASS' if self.passes_new else 'FAIL')
                         ,self.minNll
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
def GetInjectedSignalBias(function,mass=125) :
    tmpbkg = function.workspace.var("nBkg").getVal()
    function.workspace.var("nBkg").setVal(0)
    function.workspace.var("nSignal").setVal(function.smsignalyield.getVal())
    function.workspace.var("muCBNom").setVal(mass)

    injecteddata = function.totalPdf.generateBinned(ROOT.RooArgSet(function.obsVar),ROOT.RooFit.ExpectedData())

    function.workspace.var("nBkg").setVal(tmpbkg)
    function.workspace.var("nSignal").setVal(0)
    
    injecteddata.add(function.data)
    function.selectedpdf.fitTo(injecteddata,*args_datalimit) # to be revisited

    if mass == 125 :
        function.injectionerror = float(function.workspace.var("nSignal").getError())

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
        #function.selectedpdf.fitTo(function.data,*args_mclimit)
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
            bias_signalmu.append(math.fabs(y[-1]))
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

    return max(bias_signalmu)

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
    for i in range(lower_range,upper_range+1) :
        function.workspace.var("muCBNom").setVal(i)
        if isFFT :
            function.selectedpdf.fitTo(function.data_fft,*args_mclimit)
        else :
            function.selectedpdf.fitTo(function.data,*args_mclimit)

            c = ROOT.TCanvas()
            function.selectedpdf.plotOn(function.frame_rebinned)
            function.frame_rebinned.Draw()
            raw_input('pause')

            # ok. let's try to fix the bkg parameters now, and refit using mclimit to get the signal
            # error.
            #iter = function.selectedpdf.getVariables().createIterator()
            SetBkgToConstant(function,True)
            function.selectedpdf.fitTo(function.data,*args_mclimit)

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
            spur_signalmu.append(math.fabs(y[-1]))
            spur_signalmu_comp.append(math.fabs(y_comp[-1]))
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

    function.max_spur_signalmu_compatible = max(spur_signalmu_comp)
    function.max_spur_signalmu = max(spur_signalmu)
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

    for i in range(110,160) :
        function.workspace.var("muCBNom").setVal(i)
        function.selectedpdf.fitTo(function.data,*args_datalimit)
        S_fit = function.workspace.var("nSignal").getVal()
        DS_fit = float(function.workspace.var("nSignal").getError())
        if DS_fit == 0 :
            continue
        function.selectedpdf.fitTo(function.data,*args_mclimit)
        DS_mc = function.workspace.var("nSignal").getError()
        x.append(i)
        xe.append(0)
        y.append(S_fit/DS_fit)
        ye.append(DS_mc/DS_fit)
        yup.append((S_fit+DS_mc)/DS_fit)
        ydn.append((S_fit-DS_mc)/DS_fit)
        #print i,'spurious signal:',function.workspace.var("nSignal").getVal()

        if i >= 121 and i <= 129 :
            spur_signalz.append(math.fabs(y[-1]))

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

    function.max_spur_signalz = max(spur_signalz)
    return max(spur_signalz)

##################################################################################
def GetDeltaS_Relative(function) :
    function.workspace.var("muCBNom").setVal(125)
    function.selectedpdf.fitTo(function.data,*args_datalimit)
    function.deltas_relative = function.workspace.var("nSignal").getError()/float(function.smsignalyield.getVal())
    return float(function.deltas_relative)

##################################################################################
def PopulateFunctionList(functions,flist) :

    if 'exppoly' in flist :
        # exppoly
        functions.append(GetPackage('exppoly',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1))')

    if 'exppoly2' in flist :
        # exppoly2
        functions.append(GetPackage('exppoly2',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-10,10]'))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*a2) )')

    if 'exppoly2ndDOF' in flist :
        # exppoly2 with only x^2
        functions.append(GetPackage('exppoly2ndDOF'),1)
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('b1[-50,-100,100]'))
        functions[-1].AddBkgFunction('exp((m_yy - b1)/b1*(a1*(m_yy - b1)/b1))')

    if 'exppoly3' in flist :
        # exppoly3
        functions.append(GetPackage('exppoly3',3))
        for i in range(3) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*a3 ) ))')

    if 'exppoly4' in flist :
        # exppoly4
        functions.append(GetPackage('exppoly4',4))
        for i in range(4) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*a4 ) )))')

    if 'exppoly5' in flist :
        # exppoly5
        functions.append(GetPackage('exppoly5',5))
        for i in range(5) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*a5 )) ) ))')

    if 'exppoly6' in flist :
        # exppoly6
        functions.append(GetPackage('exppoly6',6))
        for i in range(6) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*a6 )) ) )))')

    if 'exppoly7' in flist :
        # exppoly7
        functions.append(GetPackage('exppoly7',7))
        for i in range(7) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*a7) )) ) )))')

    if 'exppoly8' in flist :
        # exppoly8
        functions.append(GetPackage('exppoly8',8))
        for i in range(8) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*a8)) )) ) )))')

    if 'exppoly9' in flist :
        # exppoly9
        functions.append(GetPackage('exppoly9',9))
        for i in range(9) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*(a8 + (m_yy - 100)/100*a9))) )) ) )))')

    if 'exppoly10' in flist :
        # exppoly10
        functions.append(GetPackage('exppoly10',10))
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
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].AddBkgFunction('1/(m_yy*m_yy*m_yy*m_yy)+100*a1/(m_yy*m_yy*m_yy*m_yy*m_yy)')

    if 'Laurent2' in flist :
        # 1/x^4 + 1/x^5
        functions.append(GetPackage('Laurent2',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-100,100]'))
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

    if 'Bernstein_4' in flist :
    #     # My Bernstein 4
        functions.append(GetPackage('Bernstein_4',4))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a4[0,-.9,.9]'))
        functions[-1].AddBkgFunction('a4*%s**4 + 4*a3*(1-%s)*%s**3 + 6*a2*(%s**2)*(1-%s)**2 + 4*a1*%s*(1-%s)**3 + (1-%s)**4'%(x,x,x,x,x,x,x,x))

    if 'Bernstein_5' in flist :
        # My Bernstein 5
        functions.append(GetPackage('Bernstein_5',5))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a4[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a5[0,-.9,.9]'))
        functions[-1].AddBkgFunction('a5*%s**5 + 5*a4*(1-%s)*%s**4 + 10*a3*(%s**3)*(1-%s)**2 + 10*a2*(%s**2)*(1-%s)**3 + 5*a1*%s*(1-%s)**4 + (1-%s)**5'%(x,x,x,x,x,x,x,x,x,x))

#     if 'Bernstein 3' in flist :
#         # Bernstein 3
#         functions.append(GetPackage('Bernstein 3'),3)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], 1 })')

#     if 'Bernstein 4' in flist :
#         # Bernstein 4
#         functions.append(GetPackage('Bernstein 4'),4)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-1,1], c2[0,-1,1], c3[0,-1,1], c4[0,-1,1], 1 })')

#     if 'Bernstein 5' in flist :
#         # Bernstein 5
#         functions.append(GetPackage('Bernstein 5'),5)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-1,1], c2[0,-1,1], c3[0,-1,1], c4[0,-1,1], c5[0,-1,1], 1 })')

#     if 'Bernstein 6' in flist :
#         # Bernstein 6
#         functions.append(GetPackage('Bernstein 6'),6)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], c4[0,-10,10], c5[0,-10,10], c6[0,-10,10] 1 })')

    if 'PowerSum1' in flist :
        functions.append(GetPackage('PowerSum1',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,0]'))
        functions[-1].AddBkgFunction('pow(m_yy,a1)')

#     if 'PowerSum2' in flist :
#         functions.append(GetPackage('PowerSum2',1))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10, 0]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0, -2, 2]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-10,10]'))
#         functions[-1].AddBkgFunction('pow(m_yy,a1)')

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
