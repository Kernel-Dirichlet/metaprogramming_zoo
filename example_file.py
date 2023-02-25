# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 18:56:55 2023

@author: ezw19
"""
from abc import ABC, abstractmethod

class Blah():
    def __init__(self,arg1:int,arg2:float):
        self.arg1 = arg1
        self.arg2 = arg2
    
    def method_one(self,method_arg,default_arg=1):
        '''
        arguments
        '''
        pass
    
    def method_two(self):
        pass
    
    @abstractmethod
    def abst_method(self,arg3):
        self.arg3 = str(arg3)
        return self.arg3

class Rectangle():
    def __init__(self,length,width):
        self.length = length 
        self.width = width 
    
    def compute_area(self):
        return self.length * self.width 
    
    def compute_perimeter(self):
        return (2*self.length) + (2*self.width)

class Square(Rectangle):
    pass


class Triangle():
    def __init__(self,base,height):
        self.base = base
        self.height = height
    
    def compute_area(self):
        return 0.5*self.base*self.height
    
    