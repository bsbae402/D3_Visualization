# gen_mds_points.py
# target file name: NBA_shot_logs_10attr.csv
# output file name: mds_points.csv

# list of 10 attributes used for mds plot
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

# the target file has 945 data oints

# "genDatasetOfConvertedW()" will handle conversion of categorical "W" to number data 

import os
import csv
import numpy
import math
from sklearn import manifold

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


# since each axis has different scales, we need to normalize the data.
# "column_vector" has all data of the axis
def vectorNormalization(column_vector):
	normalized_vector = []
	minVal = min(column_vector)
	maxVal = max(column_vector)
	for i in range(len(column_vector)):
		normedVal_i = (column_vector[i] - minVal) / (maxVal - minVal)
		normalized_vector.append(normedVal_i)
	return normalized_vector

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

# generate normalized version of the dataset
# first, seperate each column(axis) vectors
columnVecList = []
for i in range(numOfAttr):
	columnVecList.append( [] )

for record in floatifiedDataset:
	for columnIdx in range(numOfAttr):
		columnVecList[columnIdx].append(record[columnIdx])

# normalize each column vector
normed_col_vec_list = []
for col_vec in columnVecList:
	normed_col_vec = vectorNormalization(col_vec)
	normed_col_vec_list.append(normed_col_vec)

# create new dataset with normalized data
normed_dataset = []
for i in range(numOfRecords):
	normed_dataset.append([])

for normedColVec in normed_col_vec_list:
	for record_idx in range(len(normedColVec)):
		normed_dataset[record_idx].append(normedColVec[record_idx])

# generate N x N distance matrix (euclidean)
# N = numOfRecords
distMat = []
for i in range(numOfRecords):
	dist_ith_row = []
	vec_i = normed_dataset[i]
	for j in range(numOfRecords):
		vec_j = normed_dataset[j]
		vec_sub = numpy.subtract(vec_i, vec_j)
		dist_i_j = math.sqrt( sum(vec_sub**2) )
		dist_ith_row.append(dist_i_j)
	distMat.append(dist_ith_row)
# this is 945 X 945 matrix

# now do mds
mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
results = mds.fit(distMat)
coords = results.embedding_
print(coords)

# for my style of handling csv files, it is better to set all the data format as string
exportingFormatDataset = []
exportingFormatDataset.append(["x", "y"])
for row in coords:
	for element in row:
		element = str(element)		# actually this is shallow copy, so "distMat" also will change
	exportingFormatDataset.append(row)
# since first row is ["x" "y"], first MDS point is on second row

numpy.savetxt("mds_points.csv", exportingFormatDataset, fmt='"%s"', delimiter=",")
