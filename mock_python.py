# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 15:26:48 2023

@author: ezw19
"""

import os
from abc import ABC,abstractmethod

GLOBAL_VAR = 'NEVER DO THIS SMH'

class Shape(ABC):
    def __init__(self,name):
        self.name = name
        self.facts = []
        self.measure = []

    @abstractmethod
    def get_measure(self):
        pass

    def prompt_user(self,arg1,arg2=None):
        user_input = str(input('Enter in some facts about {}s!\n'.format(self.name)))


class Polygon(Shape):

    def get_measure(self):
        area = self.get_area()

    @abstractmethod
    def get_area(self):
        pass

    @abstractmethod
    def get_perimiter(self):
        pass

class NonPolygon(Shape):

    def get_measure(self):
        area = self.get_area()

    @abstractmethod
    def get_perimiter(self):
        pass


subtract = lambda x,y: x-y


def add(x,y):
    return x + y