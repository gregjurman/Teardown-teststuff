'''
Created on Apr 6, 2011

@author: PCADMIN
'''
import cv
import math

from teardown.capture import CaptureEngineError
import teardown.capture.detectors as base
import teardown.settings as settings

class Fiducial(base.Fiducial):
    def __init__(self, *args, **kwargs):
        base.Fiducial.__init__(self, *args, **kwargs)
        # OpenCV Init code goes here

class LineFiducial(Fiducial):
    def __init__(self, min_length=0, max_gap=0, *args, **kwargs):
        Fiducial.__init__(self, *args, **kwargs)
        self.min_length = min_length
        self.max_gap = max_gap
    
    def acquire(self, img):
        cv.SetImageROI(img, self.rect.ToCvRect())
        self.internal_img = cv.CreateImage(cv.GetSize(img), img.depth, img.nChannels)
        cv.Copy(img, self.internal_img)
        cv.ResetImageROI(img)
    
    def detect(self):
        if not hasattr(self, "internal_img"):
            raise CaptureEngineError("Acquisition has not been run. acquire() should be run first.")
        if settings.OPENCV_INTERACTIVE:
            cv.namedWindow("fiducialdetect")
            tmp_image = cv.CreateImage(cv.GetSize(self.internal_img),cv.IPL_DEPTH_32F, 3)

        edges = cv.CreateImage(cv.GetSize(self.internal_img),cv.IPL_DEPTH_8U, 1)
        cv.Canny(self.internal_img, edges, 120, 120*2, 3)
            
        self.lines = cv.HoughLines2(edges, cv.CreateMemStorage(), #image, storage
                       cv.CV_HOUGH_PROBABILISTIC, 1, cv.CV_PI/180.0, # method, rho, theta
                       self.tolerance, self.min_length, self.max_gap) #threshold, param1, param2
        
        for point in self.lines:
            if settings.CAPTURE_ENGINE:
                cv.Line(tmp_image,point[0], point[1], (0,255,0))
                
            print point
        
        if settings.CAPTURE_ENGINE:
            cv.ShowImage("fiducialdetect", tmp_image)
            cv.WaitKey()
        
    def classify(self):
        raise NotImplementedError()