"""
This is a pure python implementation of the merge sort algorithm
For doctests run following command:
python -m doctest -v merge_sort.py
or
python3 -m doctest -v merge_sort.py
For manual testing run:
python merge_sort.py
"""
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

def task():
    print("hello")


originalLength = 0

def merge_sorter(root, collection, canvas, kIndex, leftIndex, rightIndex, left_half, right_half, callBackFunction, timeLapse):
    global originalLength
    left_length = len(left_half)
    right_length = len(right_half)
    print("collection = {}".format([element.value for element in collection]))
    print("left = {}".format([element.value for element in left_half]))
    print("right = {}".format([element.value for element in right_half]))
    print("in merger sorter inner method")
    reset_colors(canvas, collection)
    if leftIndex < len(left_half) and rightIndex < len(right_half):
        canvas.itemconfig(left_half[leftIndex].rectangle, fill='blue')        
        canvas.itemconfig(right_half[rightIndex].rectangle, fill='blue')        
        if left_half[leftIndex].value < right_half[rightIndex].value:  
#            swap_xCoordinates(collection[kIndex], left_half[leftIndex])
#            oldCoordinates = []
#            oldCoordinates =  [left_half[leftIndex].coordinates[1], left_half[leftIndex].coordinates[3]]
            collection[kIndex].value= left_half[leftIndex].value
            collection[kIndex].coordinates[1], collection[kIndex].coordinates[3] =  left_half[leftIndex].coordinates[1], left_half[leftIndex].coordinates[3]
#            collection[kIndex].coordinates[2], collection[kIndex].coordinates[3] =  left_half[leftIndex].coordinates[2], left_half[leftIndex].coordinates[3]  
#            canvas.coords(left_half[leftIndex].rectangle,left_half[leftIndex].coordinates[0], left_half[leftIndex].coordinates[1],left_half[leftIndex].coordinates[2], left_half[leftIndex].coordinates[3])
            canvas.coords(collection[kIndex].rectangle,collection[kIndex].coordinates[0], collection[kIndex].coordinates[1], collection[kIndex].coordinates[2],  collection[kIndex].coordinates[3])           

            leftIndex += 1
        else:
            print("right is smaller than left")
#            print("before change, left_half = {}".format([element.value for element in left_half]))
#            oldCoordinates = []
#            oldCoordinates =  [right_half[leftIndex].coordinates[2], right_half[leftIndex].coordinates[3]]
#            swap_xCoordinates(collection[kIndex], right_half[rightIndex])
#            canvas.coords(right_half[rightIndex].rectangle,right_half[rightIndex].coordinates[0], right_half[rightIndex].coordinates[1],right_half[rightIndex].coordinates[2], right_half[rightIndex].coordinates[3])
            collection[kIndex].value = right_half[rightIndex].value
            collection[kIndex].coordinates[1], collection[kIndex].coordinates[3] =  right_half[rightIndex].coordinates[1], right_half[rightIndex].coordinates[3]
            canvas.coords(collection[kIndex].rectangle,collection[kIndex].coordinates[0], collection[kIndex].coordinates[1], collection[kIndex].coordinates[2],  collection[kIndex].coordinates[3])     
#            print("after change, left_half = {}".format([element.value for element in left_half]))         
            rightIndex += 1
        kIndex += 1
#        print("before calling merge sorter again,collection = {}".format([element.value for element in collection]))
#        print("left = {}".format([element.value for element in left_half]))
#        print("right = {}".format([element.value for element in right_half]))
        root.after(timeLapse, merge_sorter,  root, collection, canvas,  kIndex, leftIndex, rightIndex, left_half, right_half, callBackFunction, timeLapse)        
    elif leftIndex < left_length:
        canvas.itemconfig(left_half[leftIndex].rectangle, fill='blue')   
#        oldCoordinates = []
#        oldCoordinates =  [left_half[leftIndex].coordinates[1], left_half[leftIndex].coordinates[3]]
#        print("copy left over, ild y = {}".format(oldCoordinates))
 #       swap_xCoordinates(collection[kIndex], left_half[leftIndex])
 #       canvas.coords(left_half[leftIndex].rectangle,left_half[leftIndex].coordinates[0], left_half[leftIndex].coordinates[1],left_half[leftIndex].coordinates[2], left_half[leftIndex].coordinates[3])
 #       canvas.coords(collection[kIndex].rectangle,collection[kIndex].coordinates[0], collection[kIndex].coordinates[1], collection[kIndex].coordinates[2],  collection[kIndex].coordinates[3])                
        collection[kIndex].value = left_half[leftIndex].value
        collection[kIndex].coordinates[1], collection[kIndex].coordinates[3] =  left_half[leftIndex].coordinates[1], left_half[leftIndex].coordinates[3]
        #            canvas.coords(left_half[leftIndex].rectangle,left_half[leftIndex].coordinates[0], left_half[leftIndex].coordinates[1],left_half[leftIndex].coordinates[2], left_half[leftIndex].coordinates[3])
        canvas.coords(collection[kIndex].rectangle,collection[kIndex].coordinates[0], collection[kIndex].coordinates[1], collection[kIndex].coordinates[2],  collection[kIndex].coordinates[3])           
        leftIndex += 1
        kIndex += 1
#        print("before calling merge sorter again,collection = {}".format([element.value for element in collection]))
#        print("left = {}".format([element.value for element in left_half]))
#        print("right = {}".format([element.value for element in right_half]))
        root.after(timeLapse, merge_sorter,  root, collection, canvas,  kIndex, leftIndex, rightIndex, left_half, right_half, callBackFunction, timeLapse)        
    elif rightIndex < right_length:
        print("copy right ober")
        canvas.itemconfig(right_half[rightIndex].rectangle, fill='blue')        
#        oldCoordinates = []
#        oldCoordinates =  [right_half[leftIndex].coordinates[2], right_half[leftIndex].coordinates[3]]
 #       swap_xCoordinates(collection[kIndex], right_half[rightIndex])
 #       canvas.coords(right_half[rightIndex].rectangle,right_half[rightIndex].coordinates[0], right_half[rightIndex].coordinates[1],right_half[rightIndex].coordinates[2], right_half[rightIndex].coordinates[3])
 #       canvas.coords(collection[kIndex].rectangle,collection[kIndex].coordinates[0], collection[kIndex].coordinates[1], collection[kIndex].coordinates[2],  collection[kIndex].coordinates[3])                
        collection[kIndex].value = right_half[rightIndex].value
        collection[kIndex].coordinates[1], collection[kIndex].coordinates[3] =right_half[rightIndex].coordinates[1], right_half[rightIndex].coordinates[3]
        canvas.coords(collection[kIndex].rectangle,collection[kIndex].coordinates[0], collection[kIndex].coordinates[1], collection[kIndex].coordinates[2],  collection[kIndex].coordinates[3])                
        rightIndex += 1
        kIndex += 1
#        print("before calling merge sorter again,collection = {}".format([element.value for element in collection]))
#        print("left = {}".format([element.value for element in left_half]))
#        print("right = {}".format([element.value for element in right_half]))
        root.after(timeLapse, merge_sorter,  root, collection, canvas,  kIndex, leftIndex, rightIndex, left_half, right_half, callBackFunction, timeLapse)
    else:
        # merging is complete.
        if(len(collection) == originalLength):
            print("merging is complete...")
        callBackFunction(collection)

def merge_outer(root, collection, canvas, startIndex,  callBackFunction, timeLapse):
    print("in merge outer")
    if len(collection) <= 1:
        print("outer merge is complete, call the merge sorting callback registered.")
        callBackFunction(collection)
    else:
        leftIndex = 0
        rightIndex = 0
        kIndex = 0
        print("continue to divide the list")
        length = len(collection)
        midpoint = length // 2
        left_half = copy.deepcopy(collection[:midpoint])
        right_half = copy.deepcopy(collection[midpoint:])
        print(id(collection[0]))
        print(id(left_half[0]))

        merge_outer(root, left_half, canvas, startIndex, lambda data : merge_outer(root, right_half, canvas, startIndex + midpoint, lambda data1 : merge_sorter(root, collection, canvas, kIndex, leftIndex, rightIndex, data, data1, callBackFunction, timeLapse), timeLapse), timeLapse)
        
"""

def merge_sort_single_left(root, collection, canvas, left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse = 1000):
    left_length = len(left_half)
    if leftIndex < left_length:
        collection[kIndex] = left_half[leftIndex]
        leftIndex += 1
        kIndex += 1
        root.after(timeLapse, merge_sort_single_left,  root, collection, canvas, left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse)
    else:
        root.after(timeLapse, merge_sort_single_right, root, collection, canvas,  left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse)
        

def merge_sort_single_right(root, collection, canvas,  left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse = 1000):
    right_length = len(right_half)
    if rightIndex < right_length:
        collection[kIndex] = right_half[rightIndex]
        rightIndex += 1
        kIndex += 1
        root.after(timeLapse, merge_sort_single_right,  root, collection, canvas, left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse)
    else:
        root.after(timeLapse, merge_sort_outer, root, collection, timeLapse)
        


def merge_sort_inner_both(root, collection, canvas, left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse = 1000):
    if i < len(left_half) and j < len(right_half):
        if left_half[leftIndex] < right_half[rightIndex]:
            collection[kIndex] = left_half[leftIndex]
            leftIndex += 1
        else:
            collection[kIndex] = right_half[rightIndex]
            rightIndex += 1
        kIndex += 1
        root.after(timeLapse, merge_sort_inner_both, root, collection, canvas, left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse)
    else:
        root.after(timeLapse, merge_sort_single_left, root, collection, canvas, left_half, right_half, leftIndex, rightIndex, kIndex, timeLapse)



def merge_sort_outer(root, collection, canvas, sortingComplete = False, timeLapse = 1000):
    length = len(collection)
    if length > 1:
        midpoint = length // 2
        root.after(timeLapse, merge_sort_outer, collection[:midpoint], canvas, timeLapse)
        root.after(timeLapse, merge_sort_outer, collection[midpoint:], canvas, timeLapse)        
#        left_half = merge_sort_outer(root, collection[:midpoint], canvas, timeLapse)
#        right_half = merge_sort_outer(root, collection[midpoint:], canvas, timeLapse)
        i = 0
        j = 0
        k = 0
        left_length = len(left_half)
        right_length = len(right_half)
        if i < left_length and j < right_length:
            root.after(timeLapse, merge_sort_inner_both, root, collection, left_half, right_half, i, j, k, timeLapse)

    else:
        print("collection limit reached.")
        return collection
"""

def merge_sort(collection):
    """Pure implementation of the merge sort algorithm in Python
    :param collection: some mutable ordered collection with heterogeneous
    comparable items inside
    :return: the same collection ordered by ascending
    Examples:
    >>> merge_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_sort([])
    []
    >>> merge_sort([-2, -5, -45])
    [-45, -5, -2]
    """
    length = len(collection)
    if length > 1:
        midpoint = length // 2
        left_half = merge_sort(collection[:midpoint])
        right_half = merge_sort(collection[midpoint:])
        i = 0
        j = 0
        k = 0
        left_length = len(left_half)
        right_length = len(right_half)
        while i < left_length and j < right_length:
            if left_half[i] < right_half[j]:
                collection[k] = left_half[i]
                i += 1
            else:
                collection[k] = right_half[j]
                j += 1
            k += 1

        while i < left_length:
            collection[k] = left_half[i]
            i += 1
            k += 1

        while j < right_length:
            collection[k] = right_half[j]
            j += 1
            k += 1

    return collection


if __name__ == '__main__':
    import sys

    # For python 2.x and 3.x compatibility: 3.x has no raw_input builtin
    # otherwise 2.x's input builtin function is too "smart"
    if sys.version_info.major < 3:
        input_function = raw_input
    else:
        input_function = input
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
    user_input = input_function('Enter numbers separated by a comma:\n')
    myData = [int(item) for item in user_input.split(',')]

    unsorted_data = [float(item) for item in myData]
    unsorted_copy = copy.copy(unsorted_data)
    """
#    unsorted_copy = reversed(list(range(1,100)))
#    count = int(len(list(range(1,100))))
    count = len(unsorted_copy)
    timeLapse = 10
    width = window_width/int(count)
    values = unsorted_copy
    originalLength = len(values)


    root.after(2000, lambda: merge_outer(root,  values, canvas, 0, lambda x: [print(element) for element in x], timeLapse))
    #    root.after(2000, insertion_sort, unsorted, canvas) 
    print("results are")
    for i in values:
        print(i)

    """
    count = len(unsorted_copy)
    timeLapse = 100
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
    for dr in unsorted:
        print("value = {}. coordinates = {}".format(dr.value, dr.coordinates))
    unsorted = assign_colors(unsorted)
    unsorted = normalize_collection(unsorted)
    unsorted = assign_heights(unsorted, 300)
    draw_collection(unsorted, canvas)
#    for dr in unsorted:
#        print("value = {}, coordinates = {}, id = {}".format(dr.value, dr.coordinates, dr.rectangle))
    
#    print("start the loop")
    #rectangle = canvas.create_rectangle(tuple([0,0, 100, 100]), fill ='red', outline = 'black')
    #root.after(2000, lambda:move_rectangle(root, canvas, rectangle,[0,0, 100, 100]))
    root.after(2000, lambda: merge_outer(root,  unsorted, canvas, 0, lambda x: [print("value = {}, coordinates = {}".format(element.value, element.coordinates)) for element in x], timeLapse))
#    root.after(2000, insertion_sort, unsorted, canvas) 
    root.mainloop()
#    print(selection_sort(unsorted))

    root.mainloop()

