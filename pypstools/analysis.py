# -*- coding: utf-8 -*-
""" Tools for analysing power systems.

(c) 2015 Juan Manuel Mauricio
"""

import numpy as np
import scipy.linalg
import scipy.integrate
from models2dict import psse_models_dic
import matplotlib.pyplot as plt

def is_hurwitz(A):
    '''Test whether the matrix A is Hurwitz (i.e. asymptotically stable).
    '''
    
    return max(np.real(np.linalg.eig(A)[0])) < 0


def uncontrollable_modes(A, B, returnEigenValues = False):
    '''Returns all the uncontrollable modes of the pair A,B.
    
    Does the PBH test for controllability for the system:
     dx = A*x + B*u
    
    Returns a list of the uncontrollable modes, and (optionally) 
    the corresponding eigenvalues.
    
    See Callier & Desoer "Linear System Theory", P. 253
    '''

    assert A.shape[0]==A.shape[1], "Matrix A is not square"
    assert A.shape[0]==B.shape[0], "Matrices A and B do not align"

    nStates = A.shape[0]
    nInputs = B.shape[1]

    eVal, eVec = np.linalg.eig(A)

    uncontrollableModes = []
    uncontrollableEigenValues = []

    for e,v in zip(eVal, eVec.T):
        M = np.matrix(np.zeros([nStates,(nStates+nInputs)]), dtype=complex)
        M[:,:nStates] = e*np.eye(nStates,nStates) - A
        M[:,nStates:] = B
        
        s = np.linalg.svd(M, compute_uv=False)
        if min(s) == 0: 
            uncontrollableModes.append(v.T[:,0])
            uncontrollableEigenValues.append(e)

    if returnEigenValues:
        return uncontrollableModes, uncontrollableEigenValues
    else:
        return uncontrollableModes
    


def is_controllable(A, B):
    '''Compute whether the pair (A,B) is controllable.
    
    Returns True if controllable, False otherwise.
    '''

    if uncontrollable_modes(A, B):
        return False
    else:
        return True



def is_stabilisable(A, B):
    '''Compute whether the pair (A,B) is stabilisable.

    Returns True if stabilisable, False otherwise.
    '''

    modes, eigVals = uncontrollable_modes(A, B, returnEigenValues=True)
    if not modes: 
        return True  #controllable => stabilisable
    
    if max(np.real(eigVals)) >= 0:
        return False
    else:
        return True


def controllability_gramian(A, B, T = np.inf):
    '''Compute the causal controllability Gramian of the continuous time system.
    
    The system is described as
     dx = A*x + B*u
     
    T is the horizon over which to compute the Gramian. If not specified, the 
    infinite horizon Gramian is computed. Note that the infinite horizon Gramian
    only exists for asymptotically stable systems.
    
    If T is specified, we compute the Gramian as
     Wc = integrate exp(A*t)*B*B.H*exp(A.H*t) dt 
    
    Returns the matrix Wc.
    '''
    
    assert A.shape[0]==A.shape[1], "Matrix A is not square"
    assert A.shape[0]==B.shape[0], "Matrix A and B do not align"

    if not np.isfinite(T):
        #Infinite time Gramian:
        eigVals, eigVecs = scipy.linalg.eig(A)
        assert np.max(np.real(eigVals)) < 0, "Can only compute infinite horizon Gramian for a stable system."
        
        Wc = scipy.linalg.solve_lyapunov(A, -B*B.T)
        return Wc
    
    # We need to solve the finite time Gramian
    # Boils down to solving an ODE:
    A = np.array(A,dtype=float)
    B = np.array(B,dtype=float)
    T = np.float(T)
    
    def gramian_ode(y, t0, A, B):
        temp = np.dot(scipy.linalg.expm(A*t0),B)
        dQ = np.dot(temp,np.conj(temp.T))
         
        return dQ.reshape((A.shape[0]**2,1))[:,0]
     
    y0 = np.zeros([A.shape[0]**2,1])[:,0]
    out = scipy.integrate.odeint(gramian_ode, y0, [0,T], args=(A,B))
    Q = out[1,:].reshape([A.shape[0], A.shape[0]])
    return Q


def unobservable_modes(C, A, returnEigenValues = False):
    '''Returns all the unobservable modes of the pair A,C.
    
    Does the PBH test for observability for the system:
     dx = A*x
     y  = C*x
    
    Returns a list of the unobservable modes, and (optionally) 
    the corresponding eigenvalues.
    
    See Callier & Desoer "Linear System Theory", P. 253
    '''

    return uncontrollable_modes(A.getH(), C.getH(), returnEigenValues)


def is_observable(C, A):
    '''Compute whether the pair (C,A) is observable.
    
    Returns True if observable, False otherwise.
    '''
    
    return is_controllable(A.getH(), C.getH())


def is_detectable(C, A):
    '''Compute whether the pair (C,A) is detectable.

    Returns True if detectable, False otherwise.
    '''

    return is_stabilisable(A.getH(), C.getH())


#TODO
# def observability_gramian(A, B, T = np.inf):
#     '''Compute the observability Gramian of the continuous time system.
#     
#     The system is described as
#      dx = A*x + B*u
#      
#     T is the horizon over which to compute the Gramian. If not specified, the 
#     infinite horizon Gramian is computed. Note that the infinite horizon Gramian
#     only exists for asymptotically stable systems.
#     
#     If T is specified, we compute the Gramian as
#      Wc = integrate exp(A*t)*B*B.H*exp(A.H*t) dt 
#     
#     Returns the matrix Wc.
#     '''
#     
#     assert A.shape[0]==A.shape[1], "Matrix A is not square"
#     assert A.shape[0]==B.shape[0], "Matrix A and B do not align"
# 
#     if not np.isfinite(T):
#         #Infinite time Gramian:
#         eigVals, eigVecs = scipy.linalg.eig(A)
#         assert np.max(np.real(eigVals)) < 0, "Can only compute infinite horizon Gramian for a stable system."
#         
#         Wc = scipy.linalg.solve_lyapunov(A, -B*B.T)
#         return Wc
#     
#     # We need to solve the finite time Gramian
#     # Boils down to solving an ODE:
#     A = np.array(A,dtype=float)
#     B = np.array(B,dtype=float)
#     T = np.float(T)
#     
#     def gramian_ode(y, t0, A, B):
#         temp = np.dot(scipy.linalg.expm(A*t0),B)
#         dQ = np.dot(temp,np.conj(temp.T))
#          
#         return dQ.reshape((A.shape[0]**2,1))[:,0]
#      
#     y0 = np.zeros([A.shape[0]**2,1])[:,0]
#     out = scipy.integrate.odeint(gramian_ode, y0, [0,T], args=(A,B))
#     Q = out[1,:].reshape([A.shape[0], A.shape[0]])
#     return Q


def system_norm_H2(Acl, Bdisturbance, C):
    '''Compute a system's H2 norm.
    
    Acl, Bdisturbance are system matrices, describing the systems dynamics:
     dx/dt = Acl*x  + Bdisturbance*v
    where x is the system state and v is the disturbance.
    
    The system output is:
     z = C*x
    
    The matrix Acl must be Hurwitz for the H2 norm to be finite. 
     
    Parameters
    ----------
    A  : (n, n) Matrix, 
         Input
    Bdisturbance : (n, m) Matrix
         Input
    C : (n, q) Matrix
         Input

    Returns
    -------
    J2 : Systems H2 norm.
    '''
    
    if not is_hurwitz(Acl):
        return np.inf
    
    #first, compute the controllability Gramian of (Acl, Bdisturbance)
    P = controllability_gramian(Acl, Bdisturbance)
    
    #output the gain
    return np.sqrt(np.trace(C*P*C.T))
    

def system_norm_Hinf(Acl, Bdisturbance, C, D = None, lowerBound = 0, upperBound = np.inf, relTolerance = 1e-3):
    '''Compute a system's Hinfinity norm.
    
    Acl, Bdisturbance are system matrices, describing the systems dynamics:
     dx/dt = Acl*x  + Bdisturbance*v
    where x is the system state and v is the disturbance.
    
    The system output is:
     z = C*x + D*v
    
    The matrix Acl must be Hurwitz for the Hinf norm to be finite. 
    
    The norm is found by iterating over the Riccati equation. The search can 
    be sped up by providing lower and upper bounds for the norm. If ommitted, 
    these are determined automatically. 
    The search proceeds via bisection, and terminates when a specified relative
    tolerance is achieved.
     
    Parameters
    ----------
    A  : (n, n) Matrix
         Input
    Bdisturbance : (n, m) Matrix
         Input
    C : (q, n) Matrix
         Input
    D : (q,m) Matrix
         Input (optional)
    lowerBound: float
         Input (optional)
    upperBound: float 
         Input (optional)
    relTolerance: float
         Input (optional)

    Returns
    -------
    Jinf : Systems Hinf norm.
    
    '''


    if not is_hurwitz(Acl):
        return np.inf

    
    eps = 1e-10
    
    if D is None:
        #construct a fake feed-through matrix
        D = np.matrix(np.zeros([C.shape[0], Bdisturbance.shape[1]]))
    

    def test_upper_bound(gamma, A, B, C, D):
        '''Is the given gamma an upper bound for the Hinf gain?
        '''
        #Construct the R matrix:
        Rric = -gamma**2*np.matrix(np.eye(D.shape[1],D.shape[1])) + D.T*D
        #test that Rric is negative definite
        eigsR = np.linalg.eig(Rric)[0]
        if max(np.real(eigsR)) > -eps:
            return False, None
        
        #matrices for the Ricatti equation:
        Aric = A - B*np.linalg.inv(Rric)*D.T*C
        Bric = B
        Qric = C.T*C - C.T*D*np.linalg.inv(Rric)*D.T*C

        try:
            X = scipy.linalg.solve_continuous_are(Aric, Bric, Qric, Rric)
        except np.linalg.linalg.LinAlgError:
            #Couldn't solve
            return False, None
                 
        eigsX = np.linalg.eig(X)[0]
        if (np.min(np.real(eigsX)) < 0) or (np.sum(np.abs(np.imag(eigsX)))>eps):
            #The ARE has to return a pos. semidefinite solution, but X is not
            return False, None  
  
        CL = A + B*np.linalg.inv(-Rric)*(B.T*X + D.T*C)
        eigs = np.linalg.eig(CL)[0]
          
        return (np.max(np.real(eigs)) < -eps), X
    
    #our ouptut ricatti solution
    X = None
    
    #Are we supplied an upper bound? 
    if not np.isfinite(upperBound):
        upperBound = max([1,lowerBound])
        counter = 1
        while True:
            isOK, X2 = test_upper_bound(upperBound, Acl, Bdisturbance, C, D)

            if isOK:
                X = X2.copy()
                break

            upperBound *= 2
            counter += 1
            assert counter<1024, 'Exceeded max. number of iterations searching for upper bound'
            
    #perform a bisection search to find the gain:
    while (upperBound-lowerBound)>relTolerance*upperBound:
        g = 0.5*(upperBound+lowerBound)
         
        stab, X2 = test_upper_bound(g, Acl, Bdisturbance, C, D)
        if stab:
            upperBound = g
            X = X2
        else:
            lowerBound = g
     
    assert X is not None, 'No solution found! Check supplied upper bound'
    
    return upperBound
    


def ss_analysis(A):
    '''     
    Definition:ss_analysis(A)
    
    Type: Function of small_signal module

    ----
    
    Computes right and left eigenvalues and eigenvectors and computes participations factor
    matrix
    
    Parameters
    ----------
    A : System matrix array_like
    
    Returns
    -------
    w :       (M,) ndarray 
              eigenvalues.
    v_right : (M, M) ndarray
              The normalized (unit "length") eigenvectors, such that the
              column ``v_right[:,i]`` is the right eigenvector corresponding to the
              eigenvalue ``w_right[i]``.
    v_left :  (M, M) ndarray
              The normalized (unit "length") eigenvectors, such that the
              column ``v_left[:,i]`` is the right eigenvector corresponding to the
              eigenvalue ``w_left[i]``.
    
    pf:       (M, M) ndarray
              Participation factors matrix computed as PSS/E. 
    
    Example
    -------
    >>> import numpy as np 
    >>> from small_signal import ss_analysis  
    
    Linelized system from Kundur's book example 13.2 
    
    >>> A=np.array(
               [[  -1.489,   -0.179,   -0.092,   -0.94 ,   -0.   ,    0.231,    2.5  ],
                [  -0.064,   -2.929,   -0.056,    1.529,    0.   ,    0.079,    0.   ],
                [  29.55 ,    0.   ,  -36.64 ,    0.   ,    0.   ,   -5.983,    0.   ],
                [   0.   ,   12.66 ,   -0.   ,  -22.79 ,    0.   ,    3.191,    0.   ],
                [  -0.091,    0.01 ,   -0.08 ,    0.054,   -0.127,   -0.158,    0.   ],
                [   0.   ,    0.   ,    0.   ,    0.   ,  377.   ,    0.   ,    0.   ],
                [   0.   ,    0.   ,    0.   ,    0.   ,    0.   ,    0.   ,   -1.   ]]
                )
    >>> w,v_right,v_left,pf= ss_analysis(A)

    '''

    n = A.shape[0]
    
    w_right,v_right = np.linalg.eig(A)
    w=w_right
    
    v_left = np.linalg.inv(v_right)
    
    pf = np.zeros((n,n))
    
    for j in range(n):
    
        
        norm_den = sum(abs(v_right[:,j]*v_left[j,:]))
        
        for i in range(n):
            
            pf[i,j] = abs((v_right[i,j])*(v_left[j,i]))/norm_den

            
    return w,v_right,v_left,pf
   
def compute_damp(A):

    n = A.shape[0]
    
    w,v = np.linalg.eig(A)
    omega_0 = abs(w)
    damp = -w.real/omega_0
    freq = np.sqrt(1-damp**2)*omega_0
    freq_hz = freq/(2.0*np.pi)
    
    new_line  = '\n'
    str_out =  '='*8 + ' ' + '='*9 + ' ' + '='*9 + ' ' + '='*9 + ' ' + '='*9 + '\n'
    str_out += '{:8s} {:9s} {:9s} {:9s} {:9s} '.format('eig #','real','imag','damp','freq' ) + '\n'  
    str_out += '='*8 + ' ' + '='*9 + ' ' + '='*9 + ' ' + '='*9 + ' ' + '='*9 + '\n'  
    for it in range(n):
        if damp[it]<0.2:
            
            str_out +=  '  {:6s}   {:5.2f}     {:5.2f}     {:3.2f}     {:3.2f}   '.format('**'+str(it+1)+'**',w[it].real, w[it].imag,damp[it], freq_hz[it]) + '\n'  
        else:
            str_out +=  '  {:4d}     {:5.2f}     {:5.2f}      {:3.2f}    {:3.2f} '.format(it+1,w[it].real, w[it].imag,damp[it], freq_hz[it]) + '\n'              
            
    str_out += '='*8 + ' ' + '='*9 + ' ' + '='*9 + ' ' + '='*9 + ' ' + '='*9 + '\n'        
    return w,damp, freq, str_out



def plot_pf(pf):
    n = pf.shape[0]
    x = np.array(np.arange(n))+1
    y = np.array(np.arange(n))+1
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax_pf = fig.add_subplot(111)
    ax_pf.contour(X,Y,pf)
    ax_pf.grid(True)

    

def plot_pf_mode(w,pf, mode, states_dict, variable = 'all', width = 0.5, figsize=(15,6)):
    '''     
    Plots participation factors for a mode
    
    
    Parameters
    ----------
    w           : (M,) ndarray 
                   eigenvalues.
    pf          :  (M, M) ndarray
                   Participation factors matrix computed as PSS/E.              
    mode        :  integer
    
    states_dict : dictionary 
                  example: states_dict = {'omega_1':{'number':1, 'tex':r'\omega_1'},'delta_1':{'number':2, 'tex':r'\delta_1'}}
    width       : double 
                  width of the bars in the bar-plot 
                  
    fig_size : tuple
    Returns
    -------
    fig : matplotlib figure instance
    
    Example
    -------
    >>> import numpy as np 
    >>> from small_signal import ss_analysis, plot_pf_mode  
    
    Linelized system from Kundur's book example 13.2 
    
    >>> A=np.array(
               [[  -1.489,   -0.179,   -0.092,   -0.94 ,   -0.   ,    0.231,    2.5  ],
                [  -0.064,   -2.929,   -0.056,    1.529,    0.   ,    0.079,    0.   ],
                [  29.55 ,    0.   ,  -36.64 ,    0.   ,    0.   ,   -5.983,    0.   ],
                [   0.   ,   12.66 ,   -0.   ,  -22.79 ,    0.   ,    3.191,    0.   ],
                [  -0.091,    0.01 ,   -0.08 ,    0.054,   -0.127,   -0.158,    0.   ],
                [   0.   ,    0.   ,    0.   ,    0.   ,  377.   ,    0.   ,    0.   ],
                [   0.   ,    0.   ,    0.   ,    0.   ,    0.   ,    0.   ,   -1.   ]]
                )
    >>> w,v_right,v_left,pf= ss_analysis(A)
    >>> states_dict = {'e_1_q':{'number':1, 'tex':"$e'_q$"},
                       'e_1_d':{'number':2, 'tex':"$e'_d$"},
                       'psi_k_d':{'number':3, 'tex':r'$\psi kd$'},
                       'psi_k_q':{'number':4, 'tex':r'$\psi kq$'},
                       'omega':{'number':5, 'tex':r"$\omega$"},
                       'delta':{'number':6, 'tex':r"$\delta$"}}
        
    >>> mode = 3
    >>> fig = plot_pf_mode(w,pf, mode, states_dict, width = 0.5)
    >>> fig.show() 
    '''
    
    import matplotlib.pyplot as plt
    n = pf.shape[0]
    fig = plt.figure()
    fig.set_size_inches(figsize)
    ax_pf_mode = fig.add_subplot(111)
    
    plt.title(u'Participation factors for mode: {:2.2f} +/- j{:2.3f} '.format(w[mode-1].real, w[mode-1].imag))
    max_pf = pf[:,mode-1].max()  
    
    X = []
    Y = []
    T_ticks= []
    T_ticks_labels = []
    it_state = 0
    tick = 0
    for item in states_dict:
        if variable == 'all':
        
    #        print item, states_dict[item]['number']
            state_number = item
            
#            print(states_dict[item])
    
            
            if states_dict[item].has_key('tex'):
                
                T_ticks_labels += ['{:s}: {:s}'.format(states_dict[item]['bus'], states_dict[item]['tex'])]
                T_ticks += [it_state]
                X += [it_state]
                Y += [pf[it_state,mode-1]/max_pf]
                 

        for item_var in variable:       

                  
            if states_dict[item].has_key('name'):
                if states_dict[item]['name']==item_var:
        #        print item, states_dict[item]['number']
                    state_number = item
                    
#                    print(states_dict[item])
            
                    
                    if states_dict[item].has_key('tex'):
                        
                        T_ticks_labels += ['{:s}: {:s}'.format(states_dict[item]['bus'], states_dict[item]['tex'])]
                        T_ticks += [tick]
                        X += [it_state]
                        Y += [pf[it_state,mode-1]/max_pf]
                tick += 1
        
        it_state += 1
    ax_pf_mode.bar(X, Y, width, color='r')
    ax_pf_mode.set_xticks(np.array(T_ticks)+width/2)
    ax_pf_mode.set_xticklabels(T_ticks_labels)
       
    for label in ax_pf_mode.get_xticklabels():
        label.set_rotation(60)
        label.set_horizontalalignment('right')   

    return fig

def mode_shape(v_right, mode, variable, states_dict, threshold=0.1):
    fig = plt.figure()
    
    ax_mshape = fig.add_subplot(111) 
    ax_mshape = plt.subplot(111, polar=True)
    
#    ax_mshape.set_rmax(max_r)
    
    states_list = []
    for item in states_dict:
        
        if states_dict[item].has_key('name'):
            if states_dict[item]['name'] == variable:
#                print('state: {:d}'.format(item))    
                states_list += [item]
                
            

#        it_s=states_dict[item_s]['tex']['number']
#        
        #ax.plot(np.angle(v_right[it_s,16]), np.abs(v_right[it_s,16]) ,'.r', linewidth=3)
        #ax.arrow(0.0,0.0,np.angle(v_right[it_s,mode]),np.abs(v_right[it_s,mode]),lw=1) 
#   
    m_max = 0.0
    for item in states_list:  # to obtain the maximun lenght of the arrow
                
        i = item-1
        j = mode-1
        m = np.abs(v_right[i,j])
        if m>m_max:
            m_max = m
        
        
    for item in states_list:  
        i = item-1
        j = mode-1
        
        ang = np.angle(v_right[i,j])
        m = np.abs(v_right[i,j])
        m_pu = m/m_max
        
        if m_pu>threshold:
            ax_mshape.annotate("", xytext=(0.0,0.0), xy=(ang,m_pu), arrowprops=dict(facecolor='black',lw=m/m_max))
            bus = states_dict[item]['bus']
            ax_mshape.text(ang,m_pu+0.1, '{:s}: {:s}'.format(bus,states_dict[item]['tex']), rotation=0)
            
    ax_mshape.set_rmax(1.2)
    ax_mshape.get_yaxis().set_ticklabels([])
    
    return fig

# =============================================================================================

def read_psse_abcd(mlis_file):
    import os
    
    if os.name=='posix':
    ##    sys.path.append(r"/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/psse_tools/")
        return_str = '\r'
    if os.name=='nt':
    ##    sys.path.append(r"E:\jmmauricio\Documents\public\jmmauricio6\RESEARCH\psse_tools")    
        return_str = '\n'
    
    f=open(mlis_file, 'r')
    
    f_str = f.readlines()
    
    it = 0
    i_block = 0
    i_row = 0
    it_eof = 0
    n_eof = len(f_str)
    
    s_reading = False
    a_reading = False
    b_reading = False
    c_reading = False
    d_reading = False

    states_dict = {}  # name -> state number
    
    it_row = 0  
    
    for item in f_str:
        
        it_eof += 1
        
    # States list
        if item[0:55]== '   ROW   BUS  X-- NAME --X  MC  MODEL             STATE': # starts states list
            s_reading = True        
        
        
        if item[0:8]=='     PTI' and s_reading: #ends matrix
        
             s_reading = False
            
        if s_reading:
            state_row = item.split()

#            print('Estado:')

            
            if it_row>0:
                eig_number = item[0:8].strip()
                bus = item[8:14].strip()
                bus_name = item[14:34].strip() 
                id = item[33:37].strip()
                model = item[37:45].strip()
                k = item[45:60].strip()
                
#                print([eig_number,bus,bus_name,id,model,k])
                states_dict.update({int(eig_number):{}})
                
                if psse_models_dic.has_key(model):   # check if model exists in models dict
                    states_dict.update({int(eig_number):{'model':model, 'bus': bus, 'id': id}})
                    
                    if psse_models_dic[model].has_key('STATEs'): # check if states list exists in models dict
                        k_str_list = k.split('+')

                        if len(k_str_list)>1:   # get state number
                            k_value = int(k_str_list[1])
                        else:
                            k_value = 0
                            
                        state_dict = psse_models_dic[model]['STATEs'][k_value][k]
                        
                        if state_dict.has_key('tex'):
                            tex = state_dict['tex']
                            states_dict[int(eig_number)].update({'tex':tex})
                        else:
                            states_dict[int(eig_number)].update({'tex':'ukn'})     
                                       
                        if state_dict.has_key('name'):
                            name = state_dict['name']
                            states_dict[int(eig_number)].update({'name':name})
                        else:
                            states_dict[int(eig_number)].update({'name':None})                 
#            print(it_row)    
            it_row += 1    
            
#            states_dict.update({state_name:{'number':int(state_row[0]), 'tex':tex}})
#            K_value_list = state_row[5].split('+')
#            if len(K_value_list)>1:
#                state_number = int(K_value_list[1])
#                
#            else:
#                state_number = 0
#            
#            print(state_row[4])
#            if state_row[4]=='GENROU' or state_row[4]=='GENSAL':
#                print(psse_models_dic[state_row[4]]['STATEs'][state_number])
#            if state_row[4]=='GENROU' or state_row[4]=='GENSAL':
#                print(psse_models_dic[state_row[4]]['STATEs'][0])
#                for item_state in psse_models_dic[state_row[4]]['STATEs'][state_row[5]]:
#                    
#                    if state_row[6] == item_state.keys()[0]:
#                        tex =  '$\sf ' + item_state[state_row[6]]['tex'] + ' _{' + state_row[1] + '}$'
#                        state_name = item_state[state_row[6]]['name'] +  str(state_row[1])
#                        states_dict.update({state_name:{'number':int(state_row[0]), 'tex':tex}})
                        
                              
    # A matrix
        
        if item[0:8]== 'A MATRIX': # starts matrix or block
            a_reading = True        
            it = 0 
            i_row =0
            if i_block==1:
                A = A_block
            if i_block>1:
                A = np.hstack((A,A_block))
            i_block += 1
     
            
        if item[0:8]=='     PTI' and a_reading: #ends matrix
        
            if a_reading == True:
                if i_block==1:
                    A = A_block
                if i_block>1:
                    A = np.hstack((A,A_block))
            a_reading = False
            it = 0
            i_block = 0
            i_row = 0

        if item[0:1]==return_str: # if reading == True -> ends block
            a_reading = False
            
           
                
        if a_reading == True: # if read lines
            if i_row == 1:
                A_row = np.array(item.split()[1:], dtype='float')
                A_block = A_row
            if i_row > 1:
                A_row = np.array(item.split()[1:], dtype='float')
                A_block = np.vstack((A_block,A_row))
                
            i_row += 1
    
    # B matrix
    
        if item[0:8]== 'B MATRIX': # starts matrix or block
            b_reading = True        
            it = 0 
            i_row =0
            if i_block==1:
                B = B_block
            if i_block>1:
                B = np.hstack((B,B_block))
            i_block += 1

    
            
        if item[0:8]=='     PTI' and b_reading: #ends matrix
        
            if b_reading == True:
                if i_block==1:
                    B = B_block
                if i_block>1:
                    B = np.hstack((B,B_block))
            b_reading = False
            i_block = 0
            i_row = 0
    
    
        if item[0:1]==return_str: # if reading == True -> ends block
            b_reading = False
           
                
        if b_reading == True: # if read lines
            if i_row == 1:
                B_row = np.array(item.split()[1:], dtype='float')
                B_block = B_row
            if i_row > 1:
                B_row = np.array(item.split()[1:], dtype='float')
                B_block = np.vstack((B_block,B_row))
                
            i_row += 1
            
            
    # C matrix
    
        if item[0:8]== 'H MATRIX': # starts matrix or block
            c_reading = True        
            i_row =0
            if i_block==1:
                C = C_block
            if i_block>1:
                C = np.hstack((C,C_block))
            i_block += 1

    
            
        if item[0:8]=='     PTI' and c_reading: #ends matrix      
            if c_reading == True:
                if i_block==1:
                    C = C_block
                if i_block>1:
                    C = np.hstack((C,C_block))
            c_reading = False
            it = 0
            i_block = 0
            i_row = 0
    
        if item[0:1]==return_str: # if reading == True -> ends block
            c_reading = False
                           
        if c_reading == True: # if read lines
            if i_row == 1:
                C_row = np.array(item.split()[1:], dtype='float')
                C_block = C_row
            if i_row > 1:
                C_row = np.array(item.split()[1:], dtype='float')
                C_block = np.vstack((C_block,C_row))
                
            i_row += 1
            
    # D matrix

        if item[0:8]== 'F MATRIX': # starts matrix or block
            d_reading = True        
            it = 0 
            i_row =0
            if i_block==1:
                D = D_block
            if i_block>1:
                D = np.hstack((D,D_block))
            i_block += 1

            
        if ((item[0:8]=='     PTI' or it_eof==n_eof) and  d_reading):  #ends matrix
        
            if d_reading == True:

                if i_block==1:
                    D = D_block
                if i_block>1:
                    D = np.hstack((D,D_block))
                    D_row = np.array(item.split()[1:], dtype='float')
                    D = np.vstack((D,D_row))

                
        if d_reading == True: # if read lines
        
            if i_row == 1:
                D_row = np.array(item.split()[1:], dtype='float')
                D_block = D_row
                
            if i_row > 1:
                D_row = np.array(item.split()[1:], dtype='float')
                D_block = np.vstack((D_block,D_row))
                
            i_row += 1
         
    D = np.vstack((D,D_row))
    
    return A,B,C,D,states_dict
    
    
if __name__ == '__main__':
    
    mlis_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_base/results/ieee12g_base_small_signal.dat'
    mlis_file = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/results/small_signal_channels_118.dat'
    mlis_file = '/home/jmmauricio/Documents/public/jmmauricio6/INGELECTUS/ingelectus/projects/aress/code/tests/ieee_118/results/small_signal_channels_no_sta_118.dat'
    mlis_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_base/results/ieee12g_base_small_signal.dat'    
    mlis_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_10/results/ieee12g_10_pvs_small_signal.dat'
    A,B,C,D,states_dict = read_psse_abcd(mlis_file) 
    w,damp, freq, str_out = compute_damp(A)
    w,v_right,v_left,pf= ss_analysis(A)
    mode = 245
    mode = 186
    mode = 19
    variable = ['omega']
#    variable = 'all'
    plot_pf_mode(w,pf, mode, states_dict, variable='all', width = 0.5)
    variable = 'omega'
    threshold = 0.3
    fig = mode_shape(v_right, mode, variable, states_dict, threshold)