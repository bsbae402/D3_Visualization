# gen_2d_projected_points_csv.py
# target file name: eig_vector.csv AND NBA_shot_logs_10attr.csv
# output file name: 2d_projected_points.csv 

import os
import csv
import numpy
import math

top2eigVecIndex = [0, 1]

# this function will handle all string to number conversion and return the new dataset
# suppose programmer already know the string data attributes ("W")
# W -> 0, L -> 1
def genDatasetOfConvertedW(attributes, nbaDataset):
	convertedDataset = []
	# we already know
	idxOfW = attributes.index("W")
	for record in nbaDataset:
		convertedRecord = record
		if record[idxOfW] == "W":
			convertedRecord[idxOfW] = "0"
		else:
			convertedRecord[idxOfW] = "1"
		convertedDataset.append(convertedRecord)
	return convertedDataset

# make sure you only have number data in the dataset before call this function
def floatifyDataset(nbaDataset):
	floatifiedDataset = []
	for record in nbaDataset:
		floatifiedRecord = []
		for data in record:
			floatifiedRecord.append(float(data))
		floatifiedDataset.append(floatifiedRecord)
	return floatifiedDataset

# --- main program starts here ---
numpy.set_printoptions(threshold=numpy.nan)

workDirPath = os.getcwd()

# read 10-dimensional data points
fileName_data = "NBA_shot_logs_10attr.csv"	# numOfCol: 21, numOfRow: 945
filePath_data = workDirPath + "\\" + fileName_data
csvf_data = open(filePath_data, "r", newline='')		# csv file

csvFReader_data = csv.reader(csvf_data)
nbaDataset10 = []
i=0
for row in csvFReader_data:
	if i == 0:
		attributes10 = row		# assign the first row (names of attributes)
	else:
		nbaDataset10.append(row)
	i += 1
# nbaDataset10 doesn't have attribute row
numOfRecords = i-1

numOnlyDataset = genDatasetOfConvertedW(attributes10, nbaDataset10)
floatifiedDataset = floatifyDataset(numOnlyDataset)


# read eigenvectors
fileName_eigvec = "eig_vector.csv"	
filePath_eigvec = workDirPath + "\\" + fileName_eigvec
csvf_eigvec = open(filePath_eigvec, "r", newline='')		# csv file

csvFReader_eigvec = csv.reader(csvf_eigvec)
eigenvectorsDataset = []
i=0
for row in csvFReader_eigvec:
	if i == 0:
		eigvecNames = row		# assign the first row ("dim1", "dim2", ... )
	else:
		eigenvectorsDataset.append(row)
	i += 1

# datasets so far have string only. make them float
eigenvectors = floatifyDataset(eigenvectorsDataset)

top2eigenvectors = []
for i in range(len(top2eigVecIndex)):
	top2eigenvectors.append( eigenvectors[top2eigVecIndex[i]] )
print(top2eigenvectors)

# build projection matrix
projMat = numpy.array(top2eigenvectors).T
print(projMat)

# build 2d projected dataset out of 10d dataset
projectedDataset = []
for row in floatifiedDataset:
	projectedPoint = numpy.dot(row, projMat)
	projectedDataset.append(projectedPoint)
	print(projectedPoint)

expo_fmt_dataset = []
expo_fmt_dataset.append(["x", "y"])
for row in projectedDataset:
	expo_row = []
	for element in row:
		expo_row.append(str(element))
	expo_fmt_dataset.append(expo_row)

numpy.savetxt("2d_projected_points.csv", expo_fmt_dataset, fmt='"%s"', delimiter=",")

