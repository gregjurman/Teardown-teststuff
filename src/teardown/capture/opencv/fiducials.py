'''
Created on Apr 6, 2011

@author: PCADMIN
'''
import cv

import teardown.bounding as bounding
import teardown.capture.detectors as detectors

class opencvFiducial(detectors.Fiducial):
    def __init__(self, *args, **kwargs):
        detectors.Fiducial.__init__(*args, **kwargs)

class opencvLineFiducial(opencvFiducial):
    
    def opencv_acquire(self, img):
        raise NotImplementedError("herp Derp")
    
    def opencv_detect(self):
        raise NotImplementedError()
    
    def opencv_classify(self):
        raise NotImplementedError()