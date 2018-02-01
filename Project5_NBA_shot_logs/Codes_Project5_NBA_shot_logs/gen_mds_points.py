# gen_mds_points.py
# target file name: NBA_shot_logs_used.csv
# output file name: mds_points.csv

# list of 4 attributes used for mds plot
# DRIBBLES, TOUCH_TIME, SHOT_DIST(ft), CLOSE_DEF_DIST(ft)

# NBA_shot_logs_used.csv file has FGM too. So it has 5 attributes.
# but we only need the 4 attributes above. We will ignore FGM.

import os
import csv
import numpy
import math
from sklearn import manifold

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
fileName = "NBA_shot_logs_used.csv"	# numOfCol: 21, numOfRow: 945
filePath = workDirPath + "\\" + fileName
csvf = open(filePath, "r", newline='')		# csv file

csvFReader = csv.reader(csvf)
nbaDatasetUsed = []
i=0
for row in csvFReader:
	if i == 0:
		attributes = row		# assign the first row (array of strings:attrs) to "attributes""
	else:
		nbaDatasetUsed.append(row)
	i += 1
# nbaDataset doesn't have attribute row
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

# generate normalized version of the dataset
# first, seperate each column(axis) vectors
columnVecList = []
for i in range(len(trueAttrs)):
	columnVecList.append([])

for record in floatifiedDataset:
    for columnIdx in range(len(trueAttrs)):
        columnVecList[columnIdx].append(record[columnIdx])
        #columnVecList[columnIdx].append(record[columnIdx])

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
