'''
Created on Apr 6, 2011

@author: PCADMIN
'''
import teardown.core.bounding as bounding
import teardown.settings as settings
class InspectionArea(bounding.BoundingRect):
    def __init__(self, *args, **kwargs):
        bounding.BoundingRect.__init__(self, *args, **kwargs)

class Fiducial(object):
    """
    This is the base Fiducial detector. 
    
    TODO: Depending on how generic this gets it maybe moved to a
    more generalized class.
    
    FIX: The  isnt setting up properly. This needs to be fixed!!!!
    """
    def __init__(self, bounding_rect=None, tolerance=None, *args, **kwargs):
        self.rect = bounding_rect
        self.tolerance = tolerance
    
    def acquire(self, img):
        """
          Acquires the image matrix inside the area for processing.
            
          This expects the engine name is prefixed (Ex. 'engine_acquire')
        """
        if callable(self, settings.CAPTURE_ENGINE+"_acquire"): # fix this ugly
            acqcall = getattr(self, settings.CAPTURE_ENGINE+"_acquire")
            return acqcall(img)
        else:
            raise NotImplementedError()
        
    
    def detect(self):
        pass
    
    def classify(self):
        pass