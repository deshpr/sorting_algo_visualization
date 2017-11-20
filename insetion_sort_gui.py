"""
This is a pure python implementation of the insertion sort algorithm
For doctests run following command:
python -m doctest -v insertion_sort.py
or
python3 -m doctest -v insertion_sort.py
For manual testing run:
python insertion_sort.py
"""
from __future__ import print_function
from tkinter import *
import time
import math
import functools

def insertion_sort(collection, canvas, timeLapse = 1000):
    """Pure implementation of the insertion sort algorithm in Python
    :param collection: some mutable ordered collection with heterogeneous
    comparable items inside
    :return: the same collection ordered by ascending
    Examples:
    >>> insertion_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> insertion_sort([])
    []
    >>> insertion_sort([-2, -5, -45])
    [-45, -5, -2]
    """
    print("begin insertion sort....")
    for index in range(1, len(collection)):
        while 0 < index and collection[index].value < collection[index - 1].value:
            collection[index], collection[
                index - 1] = collection[index - 1], collection[index]
            draw_collection(collection,canvas)
            index -= 1
            time.sleep(5000)
        draw_collection(collection, canvas)    
        time.sleep(5000)
    return collection


class Rectangle():
    def __init__(self, color, origin, width, height):
        self.color = color
        self.origin = origin
        self.coordinates = [self.origin[0], self.origin[1],self.origin[0]+width,self.origin[1]+height]        

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
            coordinates[1] = 500  - coordinates[1] #canvasToDrawOn.winfo_height()
            coordinates[3] = 500  - coordinates[3] #- 500#canvasToDrawOn.winfo_height()
        canvasToDrawOn.create_rectangle(tuple(coordinates), fill = self.color, outline = 'black')
 
class DataRectangle(Rectangle):
    def __init__(self, value, color, origin, width, height):
        super(DataRectangle, self).__init__(color, origin, width, height)
        self.value = value
        self.normalized_value = 0


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
#    root.after(2000, task)


def setup():
    global root, canvas
    root = Tk()
    canvas = Canvas(root, width = 1000, height = 500)
    canvas.configure(background = 'black')
    canvas.pack()
    root.resizable(width=False, height=False)
    root.title('Sorting techniques!')
    root.geometry('1000x500')


if __name__ == '__main__':
    import sys

    # For python 2.x and 3.x compatibility: 3.x has no raw_input builtin
    # otherwise 2.x's input builtin function is too "smart"
    if sys.version_info.major < 3:
        input_function = raw_input
    else:
        input_function = input

    user_input = input_function('Enter numbers separated by a comma:\n')
    setup()
    startx = 0
    stary = 0
    i = 0
    width = 100
    height = 100
    unsorted = []
    for item in user_input.split(','):
        startx = (i * width)
        starty = 0
        dr = DataRectangle(item,'gray', [startx, starty], width, height)
        unsorted.append(dr)
        i = i + 1
    
    #unsorted = [DataRectangle(item, 'red',[0,0], 50,50) for item in user_input.split(',')]
    i = 0
    unsorted = assign_colors(unsorted)
    unsorted = normalize_collection(unsorted)
    unsorted = assign_heights(unsorted, 300)
    draw_collection(unsorted, canvas) 
    print("start the loop")
    insertion_sort(unsorted, canvas)
    #root.after(1, insertion_sort,  unsorted, canvas)
#    draw_collection(sorted, canvas)
    

"""    for rect in unsorted:
        print("value is  = {}".format(rect.value))
        rect.coordinates[0]  = i * 50
        rect.coordinates[2] += i * 50 + 50
        rect.draw(canvas)
        i = i + 1
"""


    #print(insertion_sort(unsorted))