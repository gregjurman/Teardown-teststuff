'''
Created on Apr 4, 2011

@author: PCADMIN
'''
import teardown as td

if __name__ == '__main__':
    # Rectangle Testing
    r1 = td.bounding.BoundingRect(x=0, y=0, h=909, w=1284, 
                               name="Image Box")
    
#    rr1 = td.bounding.HorizontalRect(y=40, h=10, 
#                                  parent=r1, 
#                                  name="Top Border")
    
    rr2 = td.bounding.HorizontalRect(y=800, h=10, 
                                  parent=r1, 
                                  name="Bottom Fiducial Box")
    
#    cr1 = td.bounding.VerticalRect(x=10, w=10,
#                                parent=r1,
#                                name="Left Border")
#    
#    cr2 = td.bounding.VerticalRect(x=50, w=10,
#                                parent=r1,
#                                name="Right Border")
#    print cr1
    
#    # Group Testing
#    grp = td.bounding.RectGroup(name="Rect Group 1")
#    grp.append(rr1)
#    grp.append(rr2)
#    grp.append(cr1)
#    grp.append(cr2)
#    
#    print grp.GetBoundaryRect().Rect
#    print grp.GetNearestBoundaryRect((30,65))
    
    
    
    # Fiducial Testing
    capt = td.capture.CaptureHandler()
    capt.load_image("testpage.png")
    fid = capt.detectors.LineFiducial(bounding_rect=rr2,
                                      tolerance=80,
                                      min_length=50, max_gap=50)
    
    fid.acquire(capt.image)
    fid.detect()
    
    if td.settings.OPENCV_INTERACTIVE:
        dump = raw_input() #hold on, i need to inspect the window
    
    print "Done"