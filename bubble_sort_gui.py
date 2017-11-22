"""
This is pure python implementation of bubble sort algorithm
For doctests run following command:
python -m doctest -v bubble_sort.py
or
python3 -m doctest -v bubble_sort.py
For manual testing run:
python bubble_sort.py
"""

from __future__ import print_function
import csv
import time
import enum
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

def bubble_sort_inner(root, outerIndex, innerIndex, collection, canvas, timeLapse = 1000):
#    print("inner bubble sort call")
    reset_colors(canvas, collection)
    canvas.itemconfig(collection[outerIndex].rectangle, fill='yellow')
    canvas.itemconfig(collection[innerIndex].rectangle, fill='blue')
    if innerIndex < outerIndex:
#       canvas.itemconfig(collection[innerIndex + 1].rectangle, fill='blue')
        canvas.itemconfig(collection[innerIndex + 1].rectangle, fill='green')
        if collection[innerIndex].value > collection[innerIndex+1].value:
            collection[innerIndex], collection[innerIndex+1] = collection[innerIndex+1], collection[innerIndex]
            swap_xCoordinates(collection[innerIndex + 1], collection[innerIndex])
            #            swap_rectangles(collection[index - 1], collection[index])
            canvas.coords(collection[innerIndex + 1].rectangle,collection[innerIndex+1].coordinates[0], collection[innerIndex+1].coordinates[1],collection[innerIndex+1].coordinates[2], collection[innerIndex+1].coordinates[3])
            canvas.coords(collection[innerIndex].rectangle,collection[innerIndex].coordinates[0], collection[innerIndex].coordinates[1], collection[innerIndex].coordinates[2],  collection[innerIndex].coordinates[3])                
#            root.after(timeLapse, bubble_sort_inner, root, outerIndex, innerIndex + 1, collection, canvas, timeLapse)
        root.after(timeLapse, bubble_sort_inner, root, outerIndex, innerIndex + 1, collection, canvas, timeLapse)
    else:
        root.after(timeLapse, bubble_sort_outer, root, outerIndex, innerIndex, collection, canvas, timeLapse)

def bubble_sort_outer(root, outerIndex, innerIndex,  collection, canvas, timeLapse = 1000):
#    print("outer bubble sort call")
    outerIndex = outerIndex - 1
    reset_colors(canvas, collection)
    if outerIndex >= 0:
        root.after(timeLapse, bubble_sort_inner, root, outerIndex, 0, collection, canvas, timeLapse)
    else:
        print("Bubble sort complete.")

def bubble_sort(collection):
	
    length = len(collection)
    for i in range(length-1, -1, -1):#range(length-1, -1, -1)
        for j in range(i):#range(1, i)
            if collection[j] > collection[j+1]:
                collection[j], collection[j+1] = collection[j+1], collection[j]

    return collection

if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
        input_function = raw_input
    else:
        input_function = input
    
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
    data_size = 100 #set to -1 for all data
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
   
#    unsorted_copy = reversed(list(range(1,10)))
#    count = int(len(list(range(1,10))))
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
    unsorted = assign_colors(unsorted)
    unsorted = normalize_collection(unsorted)
    unsorted = assign_heights(unsorted, 300)
    draw_collection(unsorted, canvas)
#    for dr in unsorted:
#        print("value = {}, coordinates = {}, id = {}".format(dr.value, dr.coordinates, dr.rectangle))
    
#    print("start the loop")
    outerIndex = len(unsorted)
    timeLapse = 10
    print("start bubble sort")
    root.after(2000, lambda: bubble_sort_outer(root, outerIndex, 0,  unsorted, canvas, timeLapse))
    root.mainloop()
"""
    start_time = time.time()
    user_input = input_function('Enter numbers separated by a comma:\n')
    unsorted = [int(item) for item in user_input.split(',')]
#    unsorted = [float(item) for item in myData]
    print(bubble_sort(unsorted))
    print("--- %s seconds ---" % (time.time() - start_time))
"""

"""
    #print(insertion_sort(unsorted))
    with open("probdist.csv") as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            myData = []
            next(readCSV)
            for row in readCSV:
                data = row[9]
                myData.append(data)
		
    start_time = time.time()
    user_input = input_function('Enter numbers separated by a comma:\n')
    unsorted = [int(item) for item in user_input.split(',')]
#    unsorted = [float(item) for item in myData]
    print(bubble_sort(unsorted))
    print("--- %s seconds ---" % (time.time() - start_time))
"""

