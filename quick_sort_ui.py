"""
This is a pure python implementation of the quick sort algorithm
For doctests run following command:
python -m doctest -v quick_sort.py
or
python3 -m doctest -v quick_sort.py
For manual testing run:
python quick_sort.py
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


def quick_sort_implementation(root, canvas, collection, leftIndex, rightIndex,  pivotElement, callback, timeLapse):
    print("{}, {}".format(leftIndex, rightIndex))
    if len(collection) > 1:
        if leftIndex <= rightIndex:        
            if collection[leftIndex] < pivotElement:
                print("left index lesser")
                root.after(timeLapse, quick_sort_implementation, root, canvas, collection, leftIndex + 1, rightIndex, pivotElement, callback, timeLapse)
            elif collection[rightIndex] > pivotElement:
                print("right index greater")
                root.after(timeLapse, quick_sort_implementation, root, canvas, collection, leftIndex, rightIndex - 1, pivotElement, callback,  timeLapse)
            elif leftIndex <= rightIndex:
                print("comparison")
                collection[leftIndex], collection[rightIndex] = collection[rightIndex], collection[leftIndex]
                leftIndex = leftIndex + 1
                rightIndex = rightIndex - 1
                root.after(timeLapse,quick_sort_implementation,  root, canvas, collection, leftIndex, rightIndex,  pivotElement, callback, timeLapse)
            else: 
                print("nothing")
        else:
            pivotElementRight = collection[rightIndex]
            pivotElementLeft = collection[len(collection) - 1]
            quick_sort_implementation(root, canvas, collection, 0, rightIndex, pivotElementRight, callback, timeLapse)
            quick_sort_implementation(root, canvas, collection, leftIndex, len(collection) - 1, pivotElementLeft, callback, timeLapse)
        print(collection)    


"""
def quick_sort_swapper(root, canvas, collection, pivotElementIndex, currentIndex, maxIndex, lessThan, callBack,  timeLapse):
    if currentIndex <= maxIndex:
        pivotElement = collection[pivotElementIndex] # usually the end of the array.
        element = collection[currentIndex]
        if(element > pivotElement):
            if(len(collection)> 2):
                elementBefore = collection[pivotElementIndex - 1]
                collection[currentIndex], collection[pivotElementIndex - 1] = collection[pivotElementIndex - 1], collection[currentIndex]
                collection[pivotElementIndex - 1], collection[pivotElementIndex] = collection[pivotElementIndex], collection[pivotElementIndex - 1]
                pivotElementIndex  = pivotElementIndex - 1
                root.after(timeLapse, quick_sort_swapper, root, canvas, collection, pivotElementIndex, currentIndex, maxIndex, lessThan, timeLapse)
            else:
                collection[pivotElementIndex - 1], collection[pivotElementIndex] = collection[pivotElementIndex], collection[pivotElementIndex - 1]
                pivotElementIndex = pivotElementIndex - 1
                # we are done already
        else:
            currentIndex = currentIndex + 1
            root.after(timeLapse, quick_sort_swapper, root, canvas, collection, pivotElementIndex, currentIndex, maxIndex, lessThan, timeLapse)
           if(lessThan):
                condition = element < pivotElement and currentIndex > pivotElementIndex
            else
                condition = pivotElement <= element and pivotElementIndex >= currentIndex
            if condition:
                collection[currentIndex], collection[pivotElementIndex] = collection[pivotElementIndex], collection[currentIndex]
                pivotElementIndex = currentIndex
            currentIndex = currentIndex + 1
"""


def quick_sort(ARRAY):
    """Pure implementation of quick sort algorithm in Python
    :param collection: some mutable ordered collection with heterogeneous
    comparable items inside
    :return: the same collection ordered by ascending
    Examples:
    >>> quick_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> quick_sort([])
    []
    >>> quick_sort([-2, -5, -45])
    [-45, -5, -2]
    """
    ARRAY_LENGTH = len(ARRAY)
    if( ARRAY_LENGTH <= 1):
        return ARRAY
    else:
        PIVOT = ARRAY[0]
        GREATER = [ element for element in ARRAY[1:] if element > PIVOT ]
        LESSER = [ element for element in ARRAY[1:] if element <= PIVOT ]
        return quick_sort(LESSER) + [PIVOT] + quick_sort(GREATER)

if __name__ == '__main__':
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
    unsorted = [ int(item) for item in user_input.split(',') ]
    pivotElement = unsorted[-1]
    timeLapse = 1000
    root.after(timeLapse, quick_sort_implementation, root, canvas, unsorted, 0, len(unsorted) - 1,  pivotElement, None, timeLapse)

    root.mainloop()


    """
    user_input = input_function('Enter numbers separated by a comma:\n')
    myData = [int(item) for item in user_input.split(',')]

    unsorted_data = [float(item) for item in myData]
    unsorted_copy = copy.copy(unsorted_data)
    
    # data file for sorting algoritm
    dataFile = "sierra1.csv"
    data_size = 1000 #set to -1 for all data
    sortedness = 0
    with open(dataFile) as csvfile:  
            readCSV = csv.reader(csvfile, delimiter=',')
            myData = []
            count = 0
            next(readCSV)
            for row in readCSV:
                count += 1
                if count == data_size:
                    break
                else:
                    data = row[3]
                    myData.append(data)
        
    start_time = time.time()
    unsorted_data = [float(item) for item in myData]
    unsorted_copy = copy.copy(unsorted_data)

#    unsorted_copy = reversed(list(range(1,100)))
#    count = int(len(list(range(1,100))))
    count = len(unsorted_copy)
    width = window_width/int(count)
    values = unsorted_copy
    originalLength = len(values)
    count = len(unsorted_copy)
    timeLapse = 1
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


    root.after(2000, lambda: merge_outer(root,  unsorted, canvas, 0, lambda x: [print("value = {}, coordinates = {}".format(element.value, element.coordinates)) for element in x], timeLapse))
    """