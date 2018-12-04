# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:45:38 2018

@author: heier
"""

from abc import ABC, abstractmethod

# Abstract class meant for any kind of image comparison tasks
class ImgComp(ABC):
    
    # Method for compare what has been drawn.
    @abstractmethod
    def compare(self, img1, img2):
        