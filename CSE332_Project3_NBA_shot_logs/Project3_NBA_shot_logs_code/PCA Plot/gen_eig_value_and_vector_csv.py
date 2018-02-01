# gen_eig_value_and_vector_csv.py
# target file name: NBA_shot_logs_10attr.csv
# output file name: eig_value.csv AND eig_vector.csv

# list of 10 attributes used for pca plot
# W				4	0
# FINAL_MARGIN	5	1
# SHOT_NUMBER	6	2
# PERIOD		7	3	
# SHOT_CLOCK	9	4
# DRIBBLES		10	5
# TOUCH_TIME	11	6
# SHOT_DIST(ft)	12	7
# PTS_TYPE		13	8
# CLOSE_DEF_DIST(ft)	16	9

# the target file has 945 data points

# "genDatasetOfConvertedW()" will handle conversion of categorical "W" to number data 

import os
import csv
import numpy
import math

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
fileName = "NBA_shot_logs_10attr.csv"	# numOfCol: 21, numOfRow: 945
filePath = workDirPath + "\\" + fileName
csvf = open(filePath, "r", newline='')		# csv file

csvFReader = csv.reader(csvf)
nbaDataset10 = []
i=0
for row in csvFReader:
	if i == 0:
		attributes10 = row		# assign the first row (array of strings:attrs) to "attributes""
	else:
		nbaDataset10.append(row)
	i += 1
# nbaDataset10 doesn't have attribute row

numOfRows = i	# include Attribute row
numOfRecords = i-1
numOfAttr = len(attributes10)

# convert "W" to number value
numOnlyDataset = genDatasetOfConvertedW(attributes10, nbaDataset10)
# CAUTION: since I didn't do the deep copy in the genDatasetOfConvertedW function, nbaDataset10 also converted.

# datasets so far have string only. make them float
floatifiedDataset = floatifyDataset(numOnlyDataset)

# generate 10 x 10 covariance matrix 
# attrAsRow is the matrix that has "W" value list for the first row, "FINAL_MARGIN" value list for the 2nd row, ...
# in other words, it is transpose matrix of nbaDataset10
attrAsRow = numpy.array(floatifiedDataset).T
#print(attrAsRow[0])

covMat = numpy.cov(attrAsRow)
#print(covMat)

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