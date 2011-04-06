'''
Created on Apr 6, 2011

@author: PCADMIN
'''

from teardown import *



class Fiducial(object):
    """
    This is the base Fiducial detector. Subclass this to the engine and specialized
    Fiducials 
    
    TODO: Depending on how generic this gets it maybe moved to a
    more generalized class.
    """
    def __init__(self, bounding_rect=None, tolerance=None, *args, **kwargs):
        clsname = "%s.%sFiducial" % (settings.CAPTURE_ENGINE, settings.CAPTURE_ENGINE)
        if hasattr(capture, clsname):
            cls = getattr(capture, clsname)
        else:
            cls = None
            raise capture.CaptureEngineError("Capture Engine '%s' does not declared." % settings.CAPTURE_ENGINE)
        
        self.__class__ = cls
        self.rect = bounding_rect
        self.tolerance = tolerance
    
    def acquire(self, img):
        """
        Acquires the image matrix inside the area for processing.
            
        This expects the engine name to be prefixed (Ex. 'engine_acquire')
        """
        if callable(self, "%s_acquire" % settings.CAPTURE_ENGINE):
            acquire_call = getattr(self, "%s_acquire" % settings.CAPTURE_ENGINE)
            return acquire_call(img)
        else:
            raise NotImplementedError()
        
    
    def detect(self):
        """
        Detects the Fiducial feature and records location, rotation info
            
        This expects the engine name to be prefixed (Ex. 'engine_detect')
        """
        if callable(self, "%s_detect" % settings.CAPTURE_ENGINE):
            detect_call = getattr(self, "%s_detect" % settings.CAPTURE_ENGINE)
            return detect_call()
        else:
            raise NotImplementedError()
    
    def classify(self):
        """
        Classifies the Fiducial and generate a confidence index
            
        This expects the engine name to be prefixed (Ex. 'engine_classify')
        """
        if callable(self, "%s_classify" % settings.CAPTURE_ENGINE):
            classify_call = getattr(self, "%s_classify" % settings.CAPTURE_ENGINE)
            return classify_call()
        else:
            raise NotImplementedError()