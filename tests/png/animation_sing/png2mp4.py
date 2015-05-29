# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:31:04 2015

@author: jmmauricio
"""

FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS
#FFMPEG_BIN = "ffmpeg.exe" # on Windows

import subprocess as sp


command = [ FFMPEG_BIN,
        '-framerate', '10', 
        '-pattern_type', 'glob', 
        '-i', '*.png', 
        '-c:v', 'libx264', 
        '-pix_fmt', 'yuv420p', 
        'out.mp4' ]
        
pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE)

