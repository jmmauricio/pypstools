# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 14:54:21 2014

@author: jmmauricio-s
"""

def part(part_title):
    '''  
    Generates a part in RestructuredText
    
    Parameters
    ----------
    
    part_title : string
                 Name of the part.
    
    
    Returns
    -------
    rst_str : string  
        String in the form of RSText part format.

    
    Examples
    --------
    >>> import pypstools.publisher.rst_basic as rst
    >>> print rst.part('Nombre de la parte')
    ##################
    Nombre de la parte
    ##################
    
    '''
    
    rst_str = ''
    
    aux_str = part_title
    rst_str += '#'*len(aux_str) + '\n'
    rst_str += aux_str  + '\n'
    rst_str += '#'*len(aux_str) + '\n'
    rst_str += '\n'*2
    
    return rst_str
    
    
def chapter(chap_title):
    '''  
    Generates a chapter in RestructuredText
    
    Parameters
    ----------
    
    chap_title : string
                 Name of the chapter.
    
    
    Returns
    -------
    rst_str : string  
        String in the form of RSText chapter format.

    
    Examples
    --------
    >>> import pypstools.publisher.rst_basic as rst
    >>> print rst.chapter('Nombre de la parte')
    ###################
    Nombre del capítulo
    ###################
    
    '''    
    rst_str = ''
    
    aux_str = chap_title
    rst_str += '='*len(aux_str) + '\n'
    rst_str += aux_str  + '\n'
    rst_str += '='*len(aux_str) + '\n'
    rst_str += '\n'*2
    
    return rst_str
    
    
def section(sec_title):
    '''  
    Generates a section in RestructuredText
    
    Parameters
    ----------
    
    sec_title : string
                 Name of the section.
    
    
    Returns
    -------
    rst_str : string  
        String in the form of RSText section format.

    
    Examples
    --------
    >>> import pypstools.publisher.rst_basic as rst
    >>> print rst.section('Nombre de la sección')
    Nombre de la sección
    ===================
    
    '''    
    rst_str = ''
    
    aux_str = sec_title
    rst_str += aux_str  + '\n'
    rst_str += '='*len(aux_str) + '\n'
    rst_str += '\n'*2
    
    return rst_str
    
    
def subsection(subsec_title):
    
    rst_str = ''
    
    aux_str = subsec_title
    rst_str += aux_str  + '\n'
    rst_str += '-'*len(aux_str) + '\n'
    rst_str += '\n'*2
    
    return rst_str
    

def figure(fig_name, fig_dir=True, caption = '', width='600px', align='left', alt='alt'):
    '''  
    Generates a figure in RestructuredText
    
    Parameters
    ----------
    
    fig_name : name of the figure file
                 Name of the section.
    
    
    Returns
    -------
    rst_str : string  
        String in the form of RSText section format.
    fig_dir :
        Whether the.png files are inside a png directory. Default is True.
    width :
        Withi of the figure in pixels. Default is '600px'.
    align : Figure alignments. Default is 'left'.
    alt : alternative text. Default is 'alt'.
    

    
    Examples
    --------
    >>> import pypstools.publisher.rst_basic as rst
    >>> print rst.figure('hola.png')
    .. figure:: ./png/hola.png
        :width: 600px
        :align: left
        :alt: alt
        :caption: 'Figure with electric powers'
    
    '''     
    
    fig_extension = fig_name.split('.')[-1]
    rst_str = ''
    
    if fig_dir:
        rst_str += '.. figure:: ./' + fig_extension + '/' + fig_name + '\n'
    else:
        rst_str += '.. figure:: ' + fig_name + '\n'
    rst_str += '   :width: ' + width + '\n'
    rst_str += '   :align: ' + align + '\n'
    rst_str += '   :alt: ' + alt + '\n'
    rst_str += '\n'
    rst_str += '   '
    rst_str += caption
    rst_str += '\n'*2
    
    return rst_str
    
def list2rst(table_list):
    columns_len = [0.0]*len(table_list[0])
    
    for item_rows in table_list:
        it_col = 0
    
        
        for item_cols in item_rows:
            
            col_len = len(str(item_cols))
            if col_len>columns_len[it_col]:
                columns_len[it_col] = len(str(item_cols))
            it_col +=1
    
    str_table = ''
    
    header = ''
    for item in columns_len:
        header += '='*item + ' '
    header += '\n'
    str_table += header
    it_row = 0   
    for item_row in  table_list:
        it_col = 0
        for item_col in item_row:
            str_table += eval("'{:" + str(columns_len[it_col]) + "s}'.format(str(item_col) )") + ' '
    
                
            it_col += 1
        str_table += '\n'
        if it_row==0:
            str_table += header
        it_row += 1 
    
    str_table += header
    rst_str = str_table
    return rst_str


if __name__ == '__main__':
    caption = u'Esta es una prueba de una caption muy larga para probar como esto funciona'
    rst_str = figure('hola.svg', fig_dir=True,caption = caption, width='600px', align='left', alt='alt')
    
    print(rst_str)