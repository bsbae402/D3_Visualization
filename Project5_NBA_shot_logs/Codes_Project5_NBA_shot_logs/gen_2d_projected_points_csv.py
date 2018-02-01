# gen_2d_projected_points_csv.py
# target file name: eig_vector.csv AND NBA_shot_logs_used.csv
# output file name: 2d_projected_points.csv 

# remember: we are not using "FGM" attribute as dimension.
# except "FGM", we have 4 attributes to be projected to 2d

import os
import csv
import numpy
import math

# top 2 eigVec are determined by manually look-up the eig_value.csv
top2eigVecIndex = [0, 1]

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

# read NBA dataset we are using
fileName_data = "NBA_shot_logs_used.csv"
filePath_data = workDirPath + "\\" + fileName_data
csvf_data = open(filePath_data, "r", newline='')		# csv file

csvFReader_data = csv.reader(csvf_data)
nbaDatasetUsed = []
i=0
for row in csvFReader_data:
	if i == 0:
		attributes = row		# assign the first row (names of attributes)
	else:
		nbaDatasetUsed.append(row)
	i += 1
# nbaDatasetUsed doesn't have attribute row
numOfRecords = i-1

# find "FGM" attribute index
fgmidx = attributes.index("FGM")

# let's start forming datasets that doesn't have FGM
trueAttrs = attributes[:]
del trueAttrs[fgmidx]

trueDataset = []
for row in nbaDatasetUsed:
    trueRow = row[:]
    del trueRow[fgmidx]
    trueDataset.append(trueRow)

floatifiedDataset = floatifyDataset(trueDataset)

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
# projMat dimension: 4 row, 2 column

# build 2d projected dataset out of 10d dataset
projectedDataset = []
for row in floatifiedDataset:
	projectedPoint = numpy.dot(row, projMat)	# each row is length 4 array
	projectedDataset.append(projectedPoint)
	#print(projectedPoint)

expo_fmt_dataset = []
expo_fmt_dataset.append(["x", "y"])
for row in projectedDataset:
	expo_row = []
	for element in row:
		expo_row.append(str(element))
	expo_fmt_dataset.append(expo_row)

numpy.savetxt("2d_projected_points.csv", expo_fmt_dataset, fmt='"%s"', delimiter=",")

