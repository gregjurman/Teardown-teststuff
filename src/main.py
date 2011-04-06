'''
Created on Apr 4, 2011

@author: PCADMIN
'''
import teardown as td

if __name__ == '__main__':
    # Rectangle Testing
    r1 = td.bounding.BoundingRect(x=0, y=0, h=100, w=100, 
                               name="OuterRect")
    
    rr1 = td.bounding.HorizontalRect(y=40, h=10, 
                                  parent=r1, 
                                  name="Top Border")
    
    rr2 = td.bounding.HorizontalRect(y=70, h=10, 
                                  parent=r1, 
                                  name="Bottom Border")
    
    cr1 = td.bounding.VerticalRect(x=10, w=10,
                                parent=r1,
                                name="Left Border")
    
    cr2 = td.bounding.VerticalRect(x=50, w=10,
                                parent=r1,
                                name="Right Border")
    print cr1
    
    # Group Testing
    grp = td.bounding.RectGroup(name="Rect Group 1")
    grp.append(rr1)
    grp.append(rr2)
    grp.append(cr1)
    grp.append(cr2)
    
    print grp.GetBoundaryRect().Rect
    print grp.GetNearestBoundaryRect((30,65))
    
    # Fiducial Testing
    fid = td.detectors.Fiducial(y=0,h=12, parent=r1, box_model=td.bounding.HorizontalRect)
    
    print fid.__class__.__name__
    
    print "Done"