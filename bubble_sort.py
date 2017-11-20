

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
        
	myDistribution = Distribution.Poisson
    with open("probdist.csv") as csvfile:  
		readCSV = csv.reader(csvfile, delimiter=',')
		myData = []
		next(readCSV)
		for row in readCSV:
			data = row[9]
			myData.append(data)
		
    start_time = time.time()
    unsorted = [float(item) for item in myData]
    print(bubble_sort(unsorted))
    print("--- %s seconds ---" % (time.time() - start_time))

