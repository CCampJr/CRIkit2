"""
Created on Sun Oct  4 00:28:16 2015

@author: camp
"""

import numpy as _np
from PyQt5.QtGui import (QColor as _QColor)

class plotStyle:

    COLOR_DICT = {'Blue':[0, 0, 1],
                  'Red':[1, 0, 0],
                  'Green':[0, .5, 0],
                  'Cyan':[0, .8, .8],
                  'Magenta':[1, 0, 1],
                  'Yellow':[.8, .8, 0]
                  }

    COLOR_VEC = ['Blue', 'Green', 'Red', 'Magenta', 'Yellow', 'Cyan']

    LINEWIDTH = 1.0

    MARKER_VEC = ['None',  #none
                  '.',  #point
                  ',',  #pixel
                  'o',  #circle
                  'v',  #triangle_down
                  '^',  #triangle_up
                  '<',  #triangle_left
                  '>',  #triangle_right
                  '8',  #octagon
                  's',  #square
                  'p',  #pentagon
                  '*',  #star
                  'h',  #hexagon1
                  'H',  #hexagon2
                  '+',  #plus
                  'x',  #x
                  'D',  #diamond
                  'd',  #thin_diamond
                  '|',  #vline
                  '_']  #hline

    MARKER_VEC_STR = ['None',
                  'Point',
                  'Pixel',
                  'Circle',
                  'Triangle Down',
                  'Triangle Up',
                  'Triangle Left',
                  'Triangle Right',
                  'Octagon',
                  'Square',
                  'Pentagon',
                  'Star',
                  'Hexagon 1',
                  'Hexagon 2',
                  'Plus',
                  'X',
                  'Diamond',
                  'Thin Diamondd',
                  'Vert Line',
                  'Horiz Line']

    MARKERSIZE=5.0
    LINESTYLE_VEC = ['-', '--', '-.', ':', 'None']
    LINESTYLE_VEC_STR = ['Solid','Dashed','Dash-Dot','Dotted','None']

    def __init__(self, num_current_plots=0):

        color, linestyle, marker = self.getLineStyle(num_current_plots=num_current_plots)

        self.color = color
        self.linewidth = self.LINEWIDTH
        self.linestyle = linestyle
        self.marker = marker
        self.markersize = self.MARKERSIZE

    @property
    def linestyle_str(self):
        index = self.LINESTYLE_VEC.index(self.linestyle)
        return self.LINESTYLE_VEC_STR[index]

    @property
    def qcolor(self):
        color = self.color
        color_256 = [color[0]*255, color[1]*255, color[2]*255]
        return _QColor(color_256[0], color_256[1], color_256[2])

    @property
    def marker_str(self):
        index = self.MARKER_VEC.index(self.marker)
        return self.MARKER_VEC_STR[index]

    def getLineStyle(self, num_current_plots = 0):
        num_colors = len(self.COLOR_VEC)
        num_linestyles = len(self.LINESTYLE_VEC)
        num_markers = len(self.MARKER_VEC)

        max_styles = num_colors*num_linestyles*num_markers

        if num_current_plots > max_styles:
            num_current_plots = num_current_plots - max_styles

        color_iter = num_current_plots%num_colors
        style_iter = int(_np.floor(num_current_plots/num_colors))%num_linestyles
        marker_iter = int(_np.floor(num_current_plots/(num_colors*num_linestyles)))%num_markers

        color = self.COLOR_DICT[self.COLOR_VEC[color_iter]]
        #print(style_iter)
        linestyle = self.LINESTYLE_VEC[style_iter]
        marker = self.MARKER_VEC[marker_iter]

        return (color, linestyle, marker)
