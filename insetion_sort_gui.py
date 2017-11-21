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

def insertion_sort_inner(root, collection, canvas, indexPosition, timeLapse = 1000):
    reset_colors(canvas, collection)
    canvas.itemconfig(collection[indexPosition].rectangle, fill='yellow')
#    print("index = {}, pre value ={} and other value ={}".format(index, collection[index-1].value, collection[index].value))
    if 0 < indexPosition and collection[indexPosition].value < collection[indexPosition - 1].value: 
#        print("next inner iteration with index = {}".format(str(index)))
        canvas.itemconfig(collection[indexPosition - 1].rectangle, fill='blue')
        canvas.itemconfig(collection[indexPosition].rectangle, fill='green')
        collection[indexPosition], collection[
            indexPosition - 1] = collection[indexPosition - 1], collection[indexPosition]
        #            print(collection[index - 1])
        #            print(type(collection[index - 1]))
        swap_xCoordinates(collection[indexPosition - 1], collection[indexPosition])
        #            swap_rectangles(collection[index - 1], collection[index])
        canvas.coords(collection[indexPosition - 1].rectangle,collection[indexPosition-1].coordinates[0], collection[indexPosition-1].coordinates[1],collection[indexPosition-1].coordinates[2], collection[indexPosition-1].coordinates[3])
        canvas.coords(collection[indexPosition].rectangle,collection[indexPosition].coordinates[0], collection[indexPosition].coordinates[1], collection[indexPosition].coordinates[2],  collection[indexPosition].coordinates[3])                
        #            draw_collection(collection,canvas)
        #            break
        indexPosition -= 1      
#        print("call inner loop again...")      
        root.after(timeLapse, insertion_sort_inner, root, collection, canvas, indexPosition, timeLapse)
    else:
#        print("inner for loop complete.")
        root.after(timeLapse, insertion_sort_outer, root, collection, canvas, timeLapse)



index = 0
def insertion_sort_outer(root, collection, canvas, timeLapse = 1000):
    global index
    index = index + 1
    if(index < len(collection)):
#        print("next outer loop iteration")
        root.after(timeLapse, insertion_sort_inner, root, collection, canvas, index, timeLapse)
    else:
        print("Inertion sort complete.")
    reset_colors(canvas, collection)


def insertion_sort(collection, canvas, timeLapse = 1000):
    sorted_results = False
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
    for dr in collection:
        print("coordinates - {}".format(str(dr.coordinates)))
    for index in range(1, len(collection)):
        while 0 < index and collection[index].value < collection[index - 1].value:            
            print("next while loop iteration")
            collection[index], collection[
                index - 1] = collection[index - 1], collection[index]
#            print(collection[index - 1])
#            print(type(collection[index - 1]))
            swap_xCoordinates(collection[index - 1], collection[index])
#            swap_rectangles(collection[index - 1], collection[index])
            canvas.coords(collection[index - 1].rectangle,collection[index-1].coordinates[0], collection[index-1].coordinates[1],collection[index-1].coordinates[2], collection[index-1].coordinates[3])
            canvas.coords(collection[index].rectangle,collection[index].coordinates[0], collection[index].coordinates[1], collection[index].coordinates[2],  collection[index].coordinates[3])                
#            draw_collection(collection,canvas)
#            break
            index -= 1            
            time.sleep(timeLapse/1000)
#        draw_collection(collection, canvas)    
        print("next for loop iteration")
#        break
        time.sleep(timeLapse/1000)
    print("sorting is complete..")
    sorted_results = True
    print("sorted results")
    for dr in unsorted:
        print("value = {}, coordinates = {}, id = {}".format(dr.value, dr.coordinates, dr.rectangle))
    canvas.update()
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
#    root.after(2000, task)

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
    
  
# data file for sorting algoritm
    dataFile = "sierra1.csv"
    data_size = 1500 #set to -1 for all data
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
    values = unsorted_copy
    count = int(len(unsorted_copy))
    width = window_width/int(count)



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
    root.after(2000, lambda: insertion_sort_outer(root, unsorted, canvas, 5))
#    root.after(2000, insertion_sort, unsorted, canvas) 
    root.mainloop()
    
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