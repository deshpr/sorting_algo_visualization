"""
This is a pure python implementation of the selection sort algorithm
For doctests run following command:
python -m doctest -v selection_sort.py
or
python3 -m doctest -v selection_sort.py
For manual testing run:
python selection_sort.py
"""
from __future__ import print_function
from __future__ import print_function
from tkinter import *
import time
import math
import functools
import csv
import time
import enum
import psutil
import os
import copy

sorted_results = False


def swap_xCoordinates(rectOne, rectTwo):
#    print("before: rect one = {} and rect two = {}".format(rectOne.coordinates, rectTwo.coordinates))
    tempXOne = rectOne.coordinates[0]
    rectOne.coordinates[0] = rectTwo.coordinates[0]
    rectTwo.coordinates[0] = tempXOne
    tempXTwo = rectOne.coordinates[2]
    rectOne.coordinates[2] = rectTwo.coordinates[2]
    rectTwo.coordinates[2] = tempXTwo
#    print("before: rect one = {} and rect two = {}".format(rectOne.coordinates, rectTwo.coordinates))

def swap_rectangles(rectOne, rectTwo):
    temp = rectOne.rectangle
    rectOne.rectangle = rectTwo.rectangle
    rectTwo.rectangle = temp

def swap_coordinates(rectOne, rectTwo):
    temp = rectOne.coordinatesInfo
    rectOne.coordinatesInfo = rectTwo.coordinatesInfo
    rectTwo.coordinatesInfo = temp

def move_rectangle(root, canvas, rectangleId, coordinates):
#    print("move rectangle")
    coordinates[0] = coordinates[0] + 25
    coordinates[2] = coordinates[2] + 25    
#    print("new coords = {}".format(coordinates))
    canvas.coords(rectangleId,coordinates[0], coordinates[1], coordinates[2], coordinates[3])
    root.after(2000, lambda:move_rectangle(root, canvas, rectangleId, coordinates))


def reset_colors(canvas, collection):
    for element in collection:
        canvas.itemconfig(element.rectangle, fill='gray')
    return collection

def selection_sort_inner(root, collection, currentIndex, least, outerIndex,  canvas, timeLapse = 1000):
    reset_colors(canvas, collection)    
    if(currentIndex < len(collection)):
        canvas.itemconfig(collection[outerIndex].rectangle, fill='blue')        
        canvas.itemconfig(collection[currentIndex].rectangle, fill='yellow')
        print("inner loop running.")
        if collection[currentIndex].value < collection[least].value:
            least = currentIndex
        currentIndex = currentIndex + 1
        root.after(timeLapse, selection_sort_inner, root, collection, currentIndex, least, outerIndex, canvas, timeLapse)
    else:
        # Inner for loop is complete.
        print("perform swap")
        canvas.itemconfig(collection[outerIndex].rectangle, fill='blue')        
        canvas.itemconfig(collection[least].rectangle, fill='green')
        collection[least], collection[outerIndex] = (
            collection[outerIndex], collection[least]
            )
        swap_xCoordinates(collection[least], collection[outerIndex])
        canvas.coords(collection[least].rectangle,collection[least].coordinates[0], collection[least].coordinates[1],collection[least].coordinates[2], collection[least].coordinates[3])
        canvas.coords(collection[outerIndex].rectangle,collection[outerIndex].coordinates[0], collection[outerIndex].coordinates[1], collection[outerIndex].coordinates[2],  collection[outerIndex].coordinates[3])                
        root.after(timeLapse, selection_sort_outer, root,collection, canvas, outerIndex, timeLapse)                         



def selection_sort_outer(root, collection, canvas, index, timeLapse = 1000):
    index = index + 1
    if index < len(collection):
        print("outer calling innner")
        root.after(timeLapse, selection_sort_inner, root, collection, index + 1, index, index, canvas, timeLapse)
    else:
        print("selection sort complete.")
        print("results are..")
        reset_colors(canvas, collection)
        for i in collection:
            print(i.value)

def selection_sort(collection):
    """Pure implementation of the selection sort algorithm in Python
    :param collection: some mutable ordered collection with heterogeneous
    comparable items inside
    :return: the same collection ordered by ascending
    Examples:
    >>> selection_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> selection_sort([])
    []
    >>> selection_sort([-2, -5, -45])
    [-45, -5, -2]
    """

    length = len(collection)
    for i in range(length):
        least = i
        for k in range(i + 1, length):
            if collection[k] < collection[least]:
                least = k
        collection[least], collection[i] = (
            collection[i], collection[least]
        )
    return collection


class DataRectangle():
    def __init__(self, value, color, origin, width, height):
        self.color = color
        self.origin = origin
        self.coordinates = [self.origin[0], self.origin[1],self.origin[0]+width,self.origin[1]+height]    
        self.rectangle = None    
        self.value = int(value)
        self.normalized_value = 0

    @property
    def coordinatesInfo(self):
        return self.coordinates

    @coordinatesInfo.setter
    def coordinatesInfo(self, value):
        self.coordinates = value

    @property
    def height(self):
        return math.abs(self.coordinates[3] - self.coordinates[1])

    @height.setter
    def height(self, value):
        if(self.coordinates[1] >= 0):
            self.coordinates[3] = self.coordinates[1] + value
        else:
            print("error....")
            raise Exception('do not support setting a height for negative starting coordinate')

    def draw(self, canvasToDrawOn, invertY = False):
        coordinates  = self.coordinates[:]
        if(invertY):
            self.coordinates[1] = 500  - coordinates[1] #canvasToDrawOn.winfo_height()
            self.coordinates[3] = 500  - coordinates[3] #- 500#canvasToDrawOn.winfo_height()
        self.rectangle = canvasToDrawOn.create_rectangle(tuple(self.coordinates), fill = self.color, outline = 'black')

def normalize_collection(collection):
    values_original = [int(dr.value) for dr in collection] # make a copy
    values = values_original[:]
    max_value =  max(values)
    min_value = min(values)
    range_value = max_value - min_value
    # normalize
    i = 0
    for strValue in values:
        value = int(strValue)
        normalized_value = (value - min_value)/(range_value)
        print("for {} normalized value  = {}".format(strValue, str(normalized_value)))
        collection[i].normalized_value = normalized_value
        i = i + 1
    return collection

def assign_heights(collection, max_height, uniformValue = 50):
    for dr in collection:
        print("normalized value = {}".format(str(dr.normalized_value)))
        dr.height = (dr.normalized_value * max_height) + uniformValue
    return collection

def assign_colors(collection):
    for rectangle in collection:
        rectangle.color = 'gray'
    return collection

def print_results(collection):
    for dr in collection:
        print(dr.value)
        print(dr.normalized_value)

def draw_collection(collection, canvas):
    for dr in collection:
        dr.draw(canvas, invertY = True)

root = None
canvas = None



if __name__ == '__main__':
    import sys
    import sys

    root = Tk()
    window_width = 2000
    window_height = 1000
    canvas = Canvas(root, width = window_width, height = window_height)
    canvas.configure(background = 'black')
    canvas.pack()
    root.resizable(width=False, height=False)
    root.title('Sorting techniques!')
    root.geometry('{}x{}'.format(window_width, window_height))

    # For python 2.x and 3.x compatibility: 3.x has no raw_input builtin
    # otherwise 2.x's input builtin function is too "smart"
    if sys.version_info.major < 3:
        input_function = raw_input
    else:
        input_function = input

    startx = 0
    stary = 0
    i = 0
    width = 100
    height = 100
    unsorted = []
    # For python 2.x and 3.x compatibility: 3.x has no raw_input builtin
    # otherwise 2.x's input builtin function is too "smart"
    if sys.version_info.major < 3:
        input_function = raw_input
    else:
        input_function = input

    user_input = input_function('Enter numbers separated by a comma:\n')
    unsorted_data = [int(item) for item in user_input.split(',')]

    unsorted_data = [float(item) for item in unsorted_data]
    unsorted_copy = copy.copy(unsorted_data)

    #    unsorted_copy = reversed(list(range(1,100)))
    #    count = int(len(list(range(1,100))))
    count = len(unsorted_copy)
    timeLapse = 500
    width = window_width/int(count)
    values = unsorted_copy
    for item in values:
        startx = (i * width)
        starty = 0
        dr = DataRectangle(item,'gray', [startx, starty], width, height)
#        print("value = {}, coordinates = {}, id = {}".format(dr.value, dr.coordinates, dr.rectangle))
        unsorted.append(dr)
        i = i + 1
        
    #unsorted = [DataRectangle(item, 'red',[0,0], 50,50) for item in user_input.split(',')]
    i = 0
    unsorted = assign_colors(unsorted)
    unsorted = normalize_collection(unsorted)
    unsorted = assign_heights(unsorted, 300)
    draw_collection(unsorted, canvas)
#    for dr in unsorted:
#        print("value = {}, coordinates = {}, id = {}".format(dr.value, dr.coordinates, dr.rectangle))
    
#    print("start the loop")
    #rectangle = canvas.create_rectangle(tuple([0,0, 100, 100]), fill ='red', outline = 'black')
    #root.after(2000, lambda:move_rectangle(root, canvas, rectangle,[0,0, 100, 100]))
    root.after(2000, lambda: selection_sort_outer(root, unsorted, canvas, -1, timeLapse))
#    root.after(2000, insertion_sort, unsorted, canvas) 
    root.mainloop()
#    print(selection_sort(unsorted))
