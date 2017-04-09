import Tools

##################################################################################
def PopulateFunctionList(functions,flist) :

    if 'Exponential' in flist :
        # Exponential
        functions.append(Tools.GetPackage('Exponential',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1))')

    if 'ExpPoly2' in flist :
        # ExpPoly2
        functions.append(Tools.GetPackage('ExpPoly2',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-10,10]'))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*a2) )')

    if 'ExpPoly2ndDOF' in flist :
        # ExpPoly2 with only x^2
        functions.append(Tools.GetPackage('ExpPoly2ndDOF'),1)
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('b1[-50,-100,100]'))
        functions[-1].AddBkgFunction('exp((m_yy - b1)/b1*(a1*(m_yy - b1)/b1))')

    if 'ExpPoly3' in flist :
        # ExpPoly3
        functions.append(Tools.GetPackage('ExpPoly3',3))
        for i in range(3) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('ep3%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(ep31 + (m_yy - 100)/100*(ep32 + (m_yy - 100)/100*ep33 ) ))')

    if 'ExpPoly4' in flist :
        # ExpPoly4
        functions.append(Tools.GetPackage('ExpPoly4',4))
        for i in range(4) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*a4 ) )))')

    if 'ExpPoly5' in flist :
        # ExpPoly5
        functions.append(Tools.GetPackage('ExpPoly5',5))
        for i in range(5) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*a5 )) ) ))')

    if 'ExpPoly6' in flist :
        # ExpPoly6
        functions.append(Tools.GetPackage('ExpPoly6',6))
        for i in range(6) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*a6 )) ) )))')

    if 'ExpPoly7' in flist :
        # ExpPoly7
        functions.append(Tools.GetPackage('ExpPoly7',7))
        for i in range(7) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*a7) )) ) )))')

    if 'ExpPoly8' in flist :
        # ExpPoly8
        functions.append(Tools.GetPackage('ExpPoly8',8))
        for i in range(8) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*a8)) )) ) )))')

    if 'ExpPoly9' in flist :
        # ExpPoly9
        functions.append(Tools.GetPackage('ExpPoly9',9))
        for i in range(9) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*(a8 + (m_yy - 100)/100*a9))) )) ) )))')

    if 'ExpPoly10' in flist :
        # ExpPoly10
        functions.append(Tools.GetPackage('ExpPoly10',10))
        for i in range(10) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
        functions[-1].AddBkgFunction('exp((m_yy - 100)/100*(a1 + (m_yy - 100)/100*(a2 + (m_yy - 100)/100*(a3 + (m_yy - 100)/100*(a4 + (m_yy - 100)/100*(a5 + (m_yy - 100)/100*(a6 + (m_yy - 100)/100*(a7 + (m_yy - 100)/100*(a8 + (m_yy - 100)/100*(a9 + (m_yy - 100)/100*a10)))) )) ) )))')


    if 'Laurent0' in flist :
        # 1/x^4
        functions.append(Tools.GetPackage('Laurent0',0))
        functions[-1].AddBkgFunction('1/(m_yy*m_yy*m_yy*m_yy)')

    if 'Laurent1' in flist :
        # 1/x^4 + 1/x^5
        functions.append(Tools.GetPackage('Laurent1',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].AddBkgFunction('1/(m_yy*m_yy*m_yy*m_yy)+100*a1/(m_yy*m_yy*m_yy*m_yy*m_yy)')

    if 'Laurent2' in flist :
        # 1/x^4 + 1/x^5
        functions.append(Tools.GetPackage('Laurent2',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,10]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-10,10]'))
        functions[-1].AddBkgFunction('1/(m_yy*m_yy*m_yy*m_yy)+100*a1/(m_yy*m_yy*m_yy*m_yy*m_yy) + 0.01*a2/(m_yy*m_yy*m_yy)')

    if '1/x^4 + a' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('1/x^4 + a',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1')

    if '1/x^4 + a + bx' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('1/x^4 + a + bx',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-100,100]'))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy - %d)'%(ur))

    if '1/x^4 + poly3' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('1/x^4 + poly3',3))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-100,100]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-100,100]'))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2'%(ur,ur))

    if '1/x^4 + poly4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('1/x^4 + poly4',4))
        for i in range(4) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-100,100]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2 + a4*(m_yy-%d)**3'%(ur,ur,ur))

    if '1/x^4 + poly5' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('1/x^4 + poly5',5))
        for i in range(5) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-100,100]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2 + a4*(m_yy-%d)**3 + a5*(m_yy-%d)**4'%(ur,ur,ur,ur))

    if '1/x^4 + poly6' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('1/x^4 + poly6',6))
        for i in range(6) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1000,1000]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000/(m_yy*m_yy*m_yy*m_yy) + a1 + a2*(m_yy-%d) + a3*(m_yy-%d)**2 + a4*(m_yy-%d)**3 + a5*(m_yy-%d)**4 + a6*(m_yy-%d)**5'%(ur,ur,ur,ur,ur))

    if 'poly1/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('poly1/x^4',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-1,1]'))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy - %d))/(m_yy*m_yy*m_yy*m_yy)'%(ur))

    if 'poly2/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('poly2/x^4',2))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-1,1]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-1,1]'))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur))

    if 'poly3/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('poly3/x^4',3))
        for i in range(3) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur))

    if 'poly4/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('poly4/x^4',4))
        for i in range(4) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3 + a4*(m_yy-%d)**4)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur))

    if 'poly5/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('poly5/x^4',5))
        for i in range(5) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3 + a4*(m_yy-%d)**4 + a5*(m_yy-%d)**5)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur,ur))

    if 'poly6/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('poly6/x^4',6))
        for i in range(6) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + a2*(m_yy-%d)**2 + a3*(m_yy-%d)**3 + a4*(m_yy-%d)**4 + a5*(m_yy-%d)**5 + a6*(m_yy-%d)**6)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur,ur,ur))

    if 'poly7/x^4' in flist :
        # 1/x^4 plus polynomial
        functions.append(Tools.GetPackage('poly7/x^4',7))
        for i in range(7) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-1,1]'%(i+1)))
        functions[-1].AddBkgFunction('100000000000*(1 + a1*(m_yy-%d) + 0.001*a2*(m_yy-%d)**2 + 0.0001*a3*(m_yy-%d)**3 + 0.000001*a4*(m_yy-%d)**4 + 0.00000001*a5*(m_yy-%d)**5 + 0.00000001*a6*(m_yy-%d)**6 + 0.000000001*a7*(m_yy-%d)**7)/(m_yy*m_yy*m_yy*m_yy)'%(ur,ur,ur,ur,ur,ur,ur))


    if 'Bernstein_3' in flist :
    #     # My Bernstein 3
        functions.append(Tools.GetPackage('Bernstein_3',3))
        for i in range(3) :
            functions[-1].BkgArgList.add(functions[-1].workspace.factory('a%d[0,-10,10]'%(i+1)))
            #functions[-1].AddBkgFunction(ROOT.RooGenericPdf(name,name,'(1-%s)**3 + a1*%s*(1-%s)**2 + a2*3*(%s**2)*(1-%s) + a3*%s**3'%(x,x,x,x,x,x),functions[-1].BkgArgList))
            x = '((m_yy-%s)/%s)'%(functions[-1].lower_range,functions[-1].upper_range-functions[-1].lower_range)
            functions[-1].AddBkgFunction('%s**3 + 3*a1*%s**2*(1-%s) + 3*a2*%s*(1-%s)**2 + a3*(%s)**3'%(x,x,x,x,x,x))

#     if 'Bernstein 3' in flist :
#         # Bernstein 3
#         functions.append(Tools.GetPackage('Bernstein 3'),3)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], 1 })')

#     if 'Bernstein_4' in flist :
#     #     # My Bernstein 4
#         functions.append(Tools.GetPackage('Bernstein_4',4))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-.9,.9]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-.9,.9]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-.9,.9]'))
#         functions[-1].BkgArgList.add(functions[-1].workspace.factory('a4[0,-.9,.9]'))
#         x = '((m_yy-%s)/%s)'%(functions[-1].lower_range,functions[-1].upper_range-functions[-1].lower_range)
#         functions[-1].AddBkgFunction('a4*%s**4 + 4*a3*(1-%s)*%s**3 + 6*a2*(%s**2)*(1-%s)**2 + 4*a1*%s*(1-%s)**3 + (1-%s)**4'%(x,x,x,x,x,x,x,x))

    if 'Bernstein_4' in flist :
        # Bernstein 4
        functions.append(Tools.GetPackage('Bernstein 4',4))
        functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], c4[0,-10,10], 1 })')
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c1'))
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c2'))
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c3'))
        functions[-1].BkgArgList.add(functions[-1].workspace.var('c4'))

    if 'Bernstein_5' in flist :
        # My Bernstein 5
        functions.append(Tools.GetPackage('Bernstein_5',5))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a4[0,-.9,.9]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a5[0,-.9,.9]'))
        x = '((m_yy-%s)/%s)'%(functions[-1].lower_range,functions[-1].upper_range-functions[-1].lower_range)
        functions[-1].AddBkgFunction('a5*%s**5 + 5*a4*(1-%s)*%s**4 + 10*a3*(%s**3)*(1-%s)**2 + 10*a2*(%s**2)*(1-%s)**3 + 5*a1*%s*(1-%s)**4 + (1-%s)**5'%(x,x,x,x,x,x,x,x,x,x))

#     if 'Bernstein 5' in flist :
#         # Bernstein 5
#         functions.append(Tools.GetPackage('Bernstein 5'),5)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-1,1], c2[0,-1,1], c3[0,-1,1], c4[0,-1,1], c5[0,-1,1], 1 })')

#     if 'Bernstein 6' in flist :
#         # Bernstein 6
#         functions.append(Tools.GetPackage('Bernstein 6'),6)
#         functions[-1].AddSpecial('RooBernstein(m_yy, { c1[0,-10,10], c2[0,-10,10], c3[0,-10,10], c4[0,-10,10], c5[0,-10,10], c6[0,-10,10] 1 })')

    if 'Pow' in flist :
        functions.append(Tools.GetPackage('Pow',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10,0]'))
        functions[-1].AddBkgFunction('pow(m_yy,a1)')

    if 'Pow2' in flist :
        functions.append(Tools.GetPackage('Pow2',1))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a1[0,-10, 0]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a2[0, -2, 2]'))
        functions[-1].BkgArgList.add(functions[-1].workspace.factory('a3[0,-10,10]'))
        functions[-1].AddBkgFunction('pow(m_yy,a1) + a2*pow(m_yy,a3)')

    return
