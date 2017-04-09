import ROOT

##
## Warning! This has not been rerun in a long time. Might need some cleanup.
## Keeping it here in case it's useful in the future.
##


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

