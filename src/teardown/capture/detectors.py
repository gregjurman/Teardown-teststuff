'''
Created on Apr 6, 2011

@author: PCADMIN
'''

class Fiducial(object):
    """
    This is the base Fiducial detector. Subclass this to the engine and specialized
    Fiducials (LineFiducial, LinearLineFiducial)
    
    TODO: Depending on how generic this gets it maybe moved to a
    more generalized class.
    """
    def __init__(self, name=None, bounding_rect=None, tolerance=80, deviation=0.2, *args, **kwargs):
        self.rect = bounding_rect
        self.tolerance = tolerance
        self.deviation = deviation
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
    
    def transform(self):
        """
        If classification isn't satisfied with the result from detection
        running transform() should take the current result and apply 
        rotation, scaling, and shifting. If the Bounding Box needs changing,
        transform should return a None so that Acquire is rerun by the
        Capture Engine.
        """
        raise NotImplementedError()
