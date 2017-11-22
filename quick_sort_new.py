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




def quick_sort_implementation(root, canvas, collection, timeLapse):
   quick_sort_caller(root, canvas, collection,0,len(collection)-1, lambda: [print(element.value) for element in collection], timeLapse)

def quick_sort_caller(root, canvas, collection,firstIndex,lastIndex, callback, timeLapse):
    if firstIndex<lastIndex:
        print("call partitioning")
#        print(collection)
        initialPivotIndex = firstIndex    
        pivotValue = collection[initialPivotIndex].value   
        leftIndex = firstIndex+1
        rightIndex = lastIndex
#        print("call method with {}".format(collection[firstIndex:lastIndex + 1]))
        root.after(timeLapse, quick_sort_partitioning_implementation, root, canvas, collection, initialPivotIndex, pivotValue, firstIndex, lastIndex, leftIndex, rightIndex,  
                    lambda pivotLocation: quick_sort_caller(root, canvas, collection,firstIndex,pivotLocation-1, 
                        lambda: quick_sort_caller(root, canvas, collection,pivotLocation+1,lastIndex, callback, timeLapse), timeLapse), timeLapse)
    else:
        print("caller is finishing.")
        callback()

def quick_sort_partitioning_implementation(root, canvas, collection, initialPivotIndex, pivotValue,  firstIndex,lastIndex, leftIndex, rightIndex,  callback, timeLapse):
    print("right = {}, left = {}".format(rightIndex, leftIndex))
    if rightIndex >= leftIndex:
        if leftIndex <= rightIndex and collection[leftIndex].value <= pivotValue:
            leftIndex = leftIndex + 1
            root.after(timeLapse, quick_sort_partitioning_implementation, root, canvas, collection, initialPivotIndex,  pivotValue, firstIndex, lastIndex, leftIndex, rightIndex,  callback, timeLapse)
        elif collection[rightIndex].value >= pivotValue and rightIndex >= leftIndex:
            rightIndex = rightIndex -1
            root.after(timeLapse, quick_sort_partitioning_implementation, root, canvas, collection, initialPivotIndex, pivotValue,  firstIndex, lastIndex, leftIndex, rightIndex,  callback, timeLapse)
        else:
            collection[leftIndex], collection[rightIndex] = collection[rightIndex], collection[leftIndex]
#            temp = collection[leftIndex].value
#            collection[leftIndex].value = collection[rightIndex].value
#            collection[rightIndex].value = temp
            swap_xCoordinates(collection[leftIndex], collection[rightIndex])
            canvas.coords(collection[leftIndex].rectangle,collection[leftIndex].coordinates[0], collection[leftIndex].coordinates[1],collection[leftIndex].coordinates[2], collection[leftIndex].coordinates[3])
            canvas.coords(collection[rightIndex].rectangle,collection[rightIndex].coordinates[0], collection[rightIndex].coordinates[1], collection[rightIndex].coordinates[2],  collection[rightIndex].coordinates[3])                
            root.after(timeLapse, quick_sort_partitioning_implementation, root, canvas, collection, initialPivotIndex, pivotValue, firstIndex, lastIndex, leftIndex, rightIndex,  callback, timeLapse)
    else:
        collection[initialPivotIndex], collection[rightIndex] = collection[rightIndex], collection[initialPivotIndex]
        swap_xCoordinates(collection[initialPivotIndex], collection[rightIndex])
        canvas.coords(collection[initialPivotIndex].rectangle,collection[initialPivotIndex].coordinates[0], collection[initialPivotIndex].coordinates[1],collection[initialPivotIndex].coordinates[2], collection[initialPivotIndex].coordinates[3])
        canvas.coords(collection[rightIndex].rectangle,collection[rightIndex].coordinates[0], collection[rightIndex].coordinates[1], collection[rightIndex].coordinates[2],  collection[rightIndex].coordinates[3])                
#        temp = collection[initialPivotIndex].value
#        collection[initialPivotIndex].value = collection[rightIndex].value
#        collection[rightIndex].value = temp
        # rightIndex is the new pivot index.
        callback(rightIndex) # pass pivot location to the callback


"""
def quick_sort_partitioning_implementation(collection,firstIndex,lastIndex, callback):
   pivotvalue = collection[firstIndex]

   leftIndex = firstIndex+1
   rightIndex = lastIndex

   done = False
   while not done:

       while leftIndex <= rightIndex and collection[leftIndex] <= pivotvalue:
           leftIndex = leftIndex + 1

       while collection[rightIndex] >= pivotvalue and rightIndex >= leftIndex:
           rightIndex = rightIndex -1

       if rightIndex < leftIndex:
           done = True
       else:
           temp = collection[leftIndex]
           collection[leftIndex] = collection[rightIndex]
           collection[rightIndex] = temp

   temp = collection[firstIndex]
   collection[firstIndex] = collection[rightIndex]
   collection[rightIndex] = temp


   return rightIndex
"""

if __name__ == '__main__':
    import sys
    root = Tk()
    window_width = 500
    window_height = 500
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
    import random
#    unsorted=[random.randrange(1,150,1) for _ in range (5)]
    user_input = input_function('Enter numbers separated by a comma:\n')
    unsorted_data = [ int(item) for item in user_input.split(',') ]
    unsorted_data = [float(item) for item in unsorted_data]
    unsorted_copy = copy.copy(unsorted_data)

    print(unsorted_copy)
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
    i = 0
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



    quick_sort_implementation(root, canvas, unsorted, 1000)
    root.mainloop()
    print(unsorted)
