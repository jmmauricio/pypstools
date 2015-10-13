# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:05:47 2014

@author: jmmauricio-s
"""
import numpy as np
import matplotlib.pyplot as plt

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
            
            str_out +=  '  {:6s}   {:5.2f}     {:5.2f}     {:5.2f}     {:5.2f}   '.format('**'+str(it+1)+'**',w[it].real, w[it].imag,damp[it], freq_hz[it]) + '\n'  
        else:
            str_out +=  '  {:4d}     {:5.2f}     {:5.2f}      {:5.2f}    {:5.2f} '.format(it+1,w[it].real, w[it].imag,damp[it], freq_hz[it]) + '\n'              
            
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

    

def plot_pf_mode(w,pf, mode, states_dict, width = 0.5):
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
    fig.set_size_inches(15,6)
    ax_pf_mode = fig.add_subplot(111)
    
    plt.title(u'Participation factors for mode: {:2.2f}±j{:2.3f} '.format(w[mode-1].real, w[mode-1].imag))
    max_pf = pf[:,mode-1].max()  
    ax_pf_mode.bar(range(n), pf[:,mode-1]/max_pf, width, color='r')

    T_ticks= range(n)
    T_ticks_labels = ['unknown']*n
    
    for item in states_dict:
        
        print item, states_dict[item]['number']
        state_number = states_dict[item]['number']
        T_ticks_labels[state_number-1] = states_dict[item]['tex']

    ax_pf_mode.set_xticks(np.array(T_ticks)+width/2)
    ax_pf_mode.set_xticklabels(T_ticks_labels)
       
    for label in ax_pf_mode.get_xticklabels():
        label.set_rotation(60)
        label.set_horizontalalignment('right')   

    return fig

states = ['omega9','omega10','omega11','omega12']
def mode_shape(v_right, mode, states, states_dict):
    fig = plt.figure()
    
    ax_mshape = fig.add_subplot(111) 
    ax_mshape = plt.subplot(111, polar=True)
    max_r = np.abs(v_right[:,mode-1]).max()
    ax_mshape.set_rmax(max_r)
       
    for item_s in states:
        it_s=states_dict[item_s]['number']
        
        #ax.plot(np.angle(v_right[it_s,16]), np.abs(v_right[it_s,16]) ,'.r', linewidth=3)
        #ax.arrow(0.0,0.0,np.angle(v_right[it_s,mode]),np.abs(v_right[it_s,mode]),lw=1) 
     
        ang = np.angle(v_right[it_s,mode-1])
        m = np.abs(v_right[it_s,mode-1])
        ax_mshape.annotate("", xytext=(0.0,0.0), xy=(ang,m), arrowprops=dict(facecolor='black',lw=1))
        ax_mshape.text(ang,m+max_r*0.1, states_dict[item_s]['tex'], rotation=0)

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
    
    for item in f_str:
        
        it_eof += 1
        
    # States list
        if item[0:55]== '   ROW   BUS  X-- NAME --X  MC  MODEL             STATE': # starts states list
            s_reading = True        
        
            
        if item[0:8]=='     PTI' and s_reading: #ends matrix
        
             s_reading = False
            
        if s_reading:
            state_row = item.split()
            print state_row
    
            
            if state_row[5]=='GENROU' or state_row[5]=='GENSAL':
                for item_state in models_data.psse_models_dic[state_row[5]]['STATEs']:
                    
                    if state_row[6] == item_state.keys()[0]:
                        tex =  '$\sf ' + item_state[state_row[6]]['tex'] + ' _{' + state_row[1] + '}$'
                        state_name = item_state[state_row[6]]['name'] +  str(state_row[1])
                        states_dict.update({state_name:{'number':int(state_row[0]), 'tex':tex}})
                              
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
            print 'reading ' + item[0:8]       
            
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
            print 'reading ' + item[0:8]
    
            
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
            print 'reading ' + item[0:8]
    
            
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
            print 'reading ' + item[0:8]    
            
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
    A,B,C,D,states_dict = read_psse_abcd(mlis_file)    
    w,v_right,v_left,pf = ss_analysis(A)
    reales= list(np.around(w.real, decimals=2))
    imaginarios= list(np.around(w.imag, decimals=2))

     
#    mlis_file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/benches/ieee_12_generic/code/ieee12g_pvsync_10/results/ieee12g_10_pvs_small_signal.dat'
#    A,B,C,D,states_dict = read_psse_abcd(mlis_file)    
#    w,v_right,v_left,pf = ss_analysis(A)
#    reales= list(np.around(w.real, decimals=2))
#    imaginarios= list(np.around(w.imag, decimals=2))

#    A=np.array(
#               [[  -1.489,   -0.179,   -0.092,   -0.94 ,   -0.   ,    0.231,    2.5  ],
#                [  -0.064,   -2.929,   -0.056,    1.529,    0.   ,    0.079,    0.   ],
#                [  29.55 ,    0.   ,  -36.64 ,    0.   ,    0.   ,   -5.983,    0.   ],
#                [   0.   ,   12.66 ,   -0.   ,  -22.79 ,    0.   ,    3.191,    0.   ],
#                [  -0.091,    0.01 ,   -0.08 ,    0.054,   -0.127,   -0.158,    0.   ],
#                [   0.   ,    0.   ,    0.   ,    0.   ,  377.   ,    0.   ,    0.   ],
#                [   0.   ,    0.   ,    0.   ,    0.   ,    0.   ,    0.   ,   -1.   ]]
#                )
#    w,v_right,v_left,pf= ss_analysis(A)
#    
#    states_dict = {'e_1_q':{'number':1, 'tex':"$e'_q$"},
#                   'e_1_d':{'number':2, 'tex':"$e'_d$"},
#                   'psi_k_d':{'number':3, 'tex':r'$\psi kd$'},
#                   'psi_k_q':{'number':4, 'tex':r'$\psi kq$'},
#                   'omega':{'number':5, 'tex':r"$\omega$"},
#                   'delta':{'number':6, 'tex':r"$\delta$"}}
#             
#    mode = 3         
#    fig = plot_pf_mode(w,pf, mode, states_dict, width = 0.5)
#    fig.show()
#    print pf
#    w,damp, freq, str_out = compute_damp(A)
#    print str_out
    