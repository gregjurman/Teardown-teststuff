'''
Created on Apr 4, 2011

@author: PCADMIN
'''

class RectangleError(Exception):
    pass


class BaseRect(object):
    '''
    A Base rectangle class. 
    '''
  
    def __init__(self, x=0, y=0, h=0, w=0, name=None):
        self._x = x
        self._y = y
        self._h = h
        self._w = w
        self.name = name
        
    @property
    def X(self):
        return self._x
        
    @X.getter
    def X(self):
        return self._x
    
    @X.setter
    def X(self, val):
        if val < 0:
            raise ValueError("X can not be less than 0.")
        else:
            self._x = val
    
    @property
    def Y(self):
        return self._y
        
    @Y.getter
    def Y(self):
        return self._y
    
    @Y.setter
    def Y(self, val):
        if val < 0:
            raise ValueError("Y can not be less than 0.")
        else:
            self._y = val
            
    @property
    def H(self):
        return self._h
        
    @H.getter
    def H(self):
        return self._h
    
    @H.setter
    def H(self, val):
        if val < 0:
            raise ValueError("Height can not be less than 0.")
        else:
            self._h = val
            
    @property
    def W(self):
        return self._w
        
    @W.getter
    def W(self):
        return self._w
    
    @W.setter
    def W(self, val):
        if val < 0:
            raise ValueError("Width can not be less than 0.")
        else:
            self._w = val
    
    @property
    def Rect(self):
        return (self._x,self._y), (self._x+self._w, self._y+self._h)
    
    def ToCvRect(self):
        return (self._x, self._y, self._w, self._h)
    
    def IsInRect(self, point):
        return (point[0] >= self._x) and (point[0] <= (self._x + self._w)) and (
            point[1] >= self._y) and (point[1] <= (self._y + self._h))
        
    def InRect(self, point):
        if self.IsInRect(point):
            return self
        else:
            return None
    
    @property
    def CenterPoint(self):
        return ((self.W / 2) + self.X, (self.H / 2) + self.Y )
    
    @property
    def Area(self):
        return self.W * self.H
    
    def __repr__(self):
        return "<%s %s at (%d,%d) %d x %d>" % (
            self.__class__.__name__,(("'%s'" % self.name) if self.name is not None else ''),
            self._x, self._y,
            self._w, self._h)
 
     
class BoundingRect(BaseRect):
    def __init__(self, *args, **kargs):
        BaseRect.__init__(self, *args, **kargs)
 
   
class InsetRect(BaseRect):
    def __init__(self, parent=None, *args, **kargs):
        BaseRect.__init__(self, *args, **kargs)
        self.parent = parent
        
    def InRect(self, point):
        if not self.IsInRect(point):
            return self.parent if isinstance(self.parent, BaseRect) and self.parent.IsInRect(point) else None
        else:
            return self


class HorizontalRect(InsetRect):
    def __init__(self, *args, **kargs):
        InsetRect.__init__(self, *args, **kargs)
        self._w = self.parent._w
        self._x = self.parent._x
        
    @property
    def X(self):
        return self.parent._x
        
    @X.getter
    def X(self):
        return self.parent._x
    
    @X.setter
    def X(self, val):
        raise RectangleError("X can not be edited in a HorizontalRect.")

    @property
    def W(self):
        return self.parent._w
        
    @W.getter
    def W(self):
        return self.parent._w
    
    @W.setter
    def W(self, val):
        raise RectangleError("Width can not be edited in a HorizontalRect.")
    
    @property
    def Rect(self):
        return (self.parent._x,self._y), (self.parent._x+self.parent._w, self._y + self._h)
    
    def ToCvRect(self):
        return (self.parent._x, self._y, self.parent._w, self._h)
    
    def IsInRect(self, point):
        return (point[0] >= self.parent._x) and (point[0] <= (self.parent._x + self.parent._w)) and (
            point[1] >= self._y) and (point[1] <= (self._y + self._h))
    
    @property
    def Area(self):
        return self.parent._w * self._h
        
    def __repr__(self):
        return "<%s %s at (%d,%d) %d x %d>" % (
            self.__class__.__name__,
             (("'%s'" % self.name) if self.name is not None else ''),
            self.parent._x, self._y,
            self.parent._w, self._h)
        
        
class VerticalRect(InsetRect):
    def __init__(self, *args, **kargs):
        InsetRect.__init__(self, *args, **kargs)
        self._h = self.parent._h
        self._y = self.parent._y
        
    @property
    def Y(self):
        return self.parent._y
        
    @Y.getter
    def Y(self):
        return self.parent._y
    
    @Y.setter
    def Y(self, val):
        raise RectangleError("Y can not be edited in a VerticalRect.")

    @property
    def H(self):
        return self.parent._h
        
    @H.getter
    def H(self):
        return self.parent._h
    
    @H.setter
    def H(self, val):
        raise RectangleError("Height can not be edited in a VerticalRect.")
    
    @property
    def Rect(self):
        return (self._x,self.parent._y), (self._x+self._w, self.parent._y+self.parent._h)
    
    def ToCvRect(self):
        return (self._x, self.parent._y, self._w, self.parent._h)
    
    def IsInRect(self, point):
        return (point[0] >= self._x) and (point[0] <= (self._x + self._w)) and (
            point[1] >= self.parent._y) and (point[1] <= (self.parent._y + self.parent._h))
    
    @property
    def Area(self):
        return self._w * self.parent._h
        
    def __repr__(self):
        return "<%s %s at (%d,%d) %d x %d>" % (
            self.__class__.__name__,(("'%s'" % self.name) if self.name is not None else ''),
            self._x, self.parent._y,
            self._w, self.parent._h)
        

class RectGroup(list):
    def __init__(self, *args, **kargs):
        if 'name' in kargs:
            self.name = kargs['name']
            del kargs['name']
        else:
            self.name = None
        
        list.__init__(self, *args, **kargs)

    def append(self, item):
        list.append(self, item)
        self.__addParent(item)
    
    def insert(self, index, object):
        list.insert(self, index, object)
        self.__addParent(object)
    
    def __addParent(self, rect):
        last = rect
        while hasattr(last, 'parent') and last.parent is not None and last.parent not in self:
            self.append(rect.parent)
            last = rect.parent
        
    def InRect(self, point):
        minRect = None
        for r in self:
            if r.IsInRect(point):
                if minRect is None or r.Area <= minRect.Area:
                    minRect = r
        
        return minRect
    
    def GetBoundaryRect(self):
        ll = []
        rl = []
        tl = []
        bl = []
        for r in self:
            rect = r.Rect
            ll.append(rect[0][0])
            rl.append(rect[1][0])
            tl.append(rect[0][1])
            bl.append(rect[1][1])
            
        _x = sorted(ll)[0]
        _w = sorted(rl, reverse=True)[0] - _x
        _y = sorted(tl)[0]
        _h = sorted(bl, reverse=True)[0] - _y
        return BoundingRect(x=_x, y=_y, w=_w, h=_h)
        
    def GetNearestBoundaryRect(self, point):
        (left, top), (right, bottom) = self.GetBoundaryRect().Rect
        
        for r in self:
            rect = r.Rect
            for l in (rect[0][0], rect[1][0]):
                if l <= point[0] and l >= left:
                    left = l
                if l >= point[0] and l <= right:
                    right = l
                    
            for t in (rect[0][1], rect[1][1]):
                if t <= point[1] and t >= top:
                    top = t          
                if t >= point[1] and t <= bottom:
                    bottom = t
                    
        return BoundingRect(x=left, y=top, w=right-left, h=bottom-top)