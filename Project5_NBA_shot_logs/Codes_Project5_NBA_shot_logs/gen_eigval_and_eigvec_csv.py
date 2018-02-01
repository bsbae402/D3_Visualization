# gen_eigval_and_eigvec.py
# target file name: NBA_shot_logs_used.csv
# output file name: eig_value.csv AND eig_vector.csv

# list of 5 attributes in the csv file
# DRIBBLES		
# TOUCH_TIME	
# SHOT_DIST(ft)	
# CLOSE_DEF_DIST(ft)	
# FGM

# only FGM will not be used for eigval creation.
# FGM, in the visualization, will be represented by color

# so, the PCA's target attributes are 4 of them: DRIBLES, TOUCH_TIME, SHOT_DIST, CLOSE_DEF_DIST

# the target file has 945 data points

import os
import csv
import numpy
import math

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
fileName = "NBA_shot_logs_used.csv"	# numOfCol: 21, numOfRow: 945
filePath = workDirPath + "\\" + fileName
csvf = open(filePath, "r", newline='')		# csv file

csvFReader = csv.reader(csvf)
nbaDatasetUsed = []
i=0
for row in csvFReader:
	if i == 0:
		attributes = row		# assign the first row (array of strings:attrs) to "attributes"
	else:
		nbaDatasetUsed.append(row)
	i += 1
# nbaDatasetUsed doesn't have attribute row

numOfRows = i	# include Attribute row
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

# datasets so far have string only. make them float
floatifiedDataset = floatifyDataset(trueDataset)

# generate 4 x 4 covariance matrix 
# attrAsRow is the matrix that has "DRIBBLES" value list for the first row, "TOUCH_TIME" value list for the 2nd row, ...
# in other words, it is transpose matrix of nbaDataset10
attrAsRow = numpy.array(floatifiedDataset).T
print(len(attrAsRow))

covMat = numpy.cov(attrAsRow)
print(covMat)

# let's get eig vec and eig val
eig_val_list, eig_vec_list = numpy.linalg.eig(covMat)

# for my style of handling csv files, it is better to set all the data format as string
exportingFormatDataset = []
exportingFormatDataset.append("eig_val")
for eig_val in eig_val_list:
	exportingFormatDataset.append(str(eig_val))
numpy.savetxt("eig_value.csv", exportingFormatDataset, fmt='"%s"', delimiter=",")

vec_expo_dataset = []
numOfDim = len(eig_vec_list[0])
firstRow = []
for i in range(numOfDim):
	firstRow.append("dim" + str(i+1))
vec_expo_dataset.append(firstRow)

for eig_vec in eig_vec_list:
	formated_vec = [] 
	for element in eig_vec:
		formated_vec.append(str(element))
	vec_expo_dataset.append(formated_vec)
numpy.savetxt("eig_vector.csv", vec_expo_dataset, fmt='"%s"', delimiter=",")