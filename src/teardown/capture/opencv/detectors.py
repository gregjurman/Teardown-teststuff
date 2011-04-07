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
        self.found_data = False
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
            
        self.data = cv.HoughLines2(edges, cv.CreateMemStorage(), #image, storage
                       cv.CV_HOUGH_PROBABILISTIC, 1, cv.CV_PI/180.0, # method, rho, theta
                       self.tolerance, self.min_length, self.max_gap) #threshold, param1, param2
        
        if len(self.data):
            self.found_data = True
        else:
            self.found_data = False
        
        for point in self.data:
            if settings.OPENCV_INTERACTIVE:
                cv.Line(tmp_image,point[0], point[1], (0,255,0))
                
            print point
        
        if settings.OPENCV_INTERACTIVE:
            cv.ShowImage("fiducialdetect", tmp_image)
            cv.WaitKey()
            
        return self.found_data
        
    def classify(self):
        '''
        This is implemented for specific line type detectors like
        LinearLineFiducial or a special case
        '''
        raise NotImplementedError()
    
    def transform(self):
        raise NotImplementedError()
    
class LinearLineFiducial(LineFiducial):
    def __init__(self, approx_angle=0, approx_length=1, *args, **kwargs):
        LineFiducial.__init__(self, *args, **kwargs)
        
    def classify(self):
        if not hasattr(self, "data"):
            raise CaptureEngineError("Missing detected data! You need to run detect() first")
        
        # Probablistic HoughLines returns a list of tuples of tuples ((x1, y1),(x2, y2))
        # Extract them to a list of single points
        point_cloud = []
        for a, b in self.data:
            point_cloud.extend([a, b])
            
        cloud_rect = self._cloud_boundary(point_cloud)
        center_x, center_y = self._center(cloud_rect)
        slope, offset = self._get_slope_offset(point_cloud)
        
        theta = math.atan(slope)
        #Finish this
        
    def _cloud_boundary(self, point_cloud):
        xl = []
        yl = []
        for x, y in point_cloud:
            xl.append(x)
            yl.append(y)

        xl.sort()    
        yl.sort()
        x1, y1 = xl[0], yl[0]
        x2, y2 = xl[-1], yl[-1]
        return (x1, y1), (x2, y2)
    
    def _center(self, points):
        (x1, y1), (x2,y2) = points
        return ( ((x2 - x1) / 2.0) + x1, ((y2 - y1) / 2.0) + y1)
    
    def _get_slope_offset(self, point_cloud):
        n = len(point_cloud)
        sum_x=0
        sum_y=0
        sum_xx=0
        sum_xy=0
        for x, y in point_cloud:
            sum_x=sum_x+x
            sum_y=sum_y+y
            xx=math.pow(x,2)
            sum_xx=sum_xx+xx
            xy=x*y
            sum_xy=sum_xy+xy
            
        a=(-sum_x*sum_xy+sum_xx*sum_y)/(n*sum_xx-sum_x*sum_x)
        b=(-sum_x*sum_y+n*sum_xy)/(n*sum_xx-sum_x*sum_x)
        
        return (a, b)