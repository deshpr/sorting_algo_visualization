

"""
This is a implementation of 
bubble sort algorithm
quick sort algorithm
merge sort algorithm
insertion sort alogorithm
selection sort algorithm
"""

from __future__ import print_function
import csv
import time
import enum
import psutil
import os
import copy
from guppy import hpy


# data file for sorting algoritm
dataFile = "sierra1.csv"
data_size = 1500 #set to -1 for all data
sortedness = 0


def bubble_sort(collection):
    
    global sortedness
    length = len(collection)
    for i in range(length-1, -1, -1):#range(length-1, -1, -1)
        for j in range(i):#range(1, i)
            if collection[j] > collection[j+1]:
                collection[j], collection[j+1] = collection[j+1], collection[j]
                sortedness += 1
                
    return collection
    
def selection_sort(collection):

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

def quick_sort(ARRAY):

    ARRAY_LENGTH = len(ARRAY)
    if( ARRAY_LENGTH <= 1):
        return ARRAY
    else:
        PIVOT = ARRAY[0]
        GREATER = [ element for element in ARRAY[1:] if element > PIVOT ]
        LESSER = [ element for element in ARRAY[1:] if element <= PIVOT ]
        return quick_sort(LESSER) + [PIVOT] + quick_sort(GREATER)
   
def merge_sort(collection):

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

def insertion_sort(collection):

    for index in range(1, len(collection)):
        while 0 < index and collection[index] < collection[index - 1]:
            collection[index], collection[
                index - 1] = collection[index - 1], collection[index]
            index -= 1

    return collection
    
    
    
def csv_data_output_create(data_size):

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
	unsorted = [float(item) for item in myData]
	unsorted_copy = copy.copy(unsorted)
#	print(bubble_sort(unsorted))
#	print(selection_sort(unsorted))
#	print(quick_sort(unsorted))
#	print(merge_sort(unsorted))
	print(insertion_sort(unsorted))
	print("seconds..", (time.time() - start_time))
	h = hpy()
	print (h.heap())
	print("number of data points", data_size)
	print(bubble_sort(unsorted_copy))
	print ("sortedness " , sortedness) 


	
 
if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
        input_function = raw_input
    else:
        input_function = input
        
    csv_data_output_create(data_size)

