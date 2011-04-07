'''
Created on Apr 6, 2011

@author: PCADMIN
'''
import teardown.capture.opencv.detectors as detectors
import teardown.capture.opencv.util as util
import cv

def load_image(file_name):
    return cv.LoadImage(file_name, cv.CV_LOAD_IMAGE_GRAYSCALE)