'''
Created on Apr 6, 2011

@author: PCADMIN
'''

class Fiducial(object):
    """
    This is the base Fiducial detector. Subclass this to the engine and specialized
    Fiducials 
    
    TODO: Depending on how generic this gets it maybe moved to a
    more generalized class.
    """
    def __init__(self, name=None, bounding_rect=None, tolerance=10, *args, **kwargs):
        self.rect = bounding_rect
        self.tolerance = tolerance
        self.name = name
    
    def acquire(self, img):
        """
        Acquires the image matrix inside the area for processing.
        """
        raise NotImplementedError()   
    
    def detect(self):
        """
        Detects the Fiducial feature and records location, rotation info
        """
        raise NotImplementedError()
    
    def classify(self):
        """
        Classifies the Fiducial and generate a confidence index
        """
        raise NotImplementedError()