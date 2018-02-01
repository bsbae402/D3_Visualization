# gen_10x10correlation_mat_csv.py
# target file name: NBA_shot_logs_2014_2015_reduced_at1.csv

# the nba shot dataset (reduced edition) will have 945 records (except the first row of attribute names)

# <attribute	index>
# shot_id	0
# GAME_ID	1
# MATCHUP	2
# LOCATION	3
# W	4
# FINAL_MARGIN	5
# SHOT_NUMBER	6
# PERIOD	7
# GAME_CLOCK	8	
# SHOT_CLOCK	9
# DRIBBLES	10
# TOUCH_TIME	11
# SHOT_DIST(ft)	12
# PTS_TYPE	13
# CLOSEST_DEFENDER	14
# CLOSEST_DEFENDER_PLAYER_ID	15
# CLOSE_DEF_DIST(ft)	16
# FGM	17
# PTS	18
# player_name	19
# player_id	20

# list of 10 attributes used for correlation matrix
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

# Among them, categorical attributes are:
# W 4 [0] , PERIOD 7 [3] , PTS_TYPE 13 [8]
# BUT the only thing causes problem is "W" because it is string data 
# And the types of values that each variable can have are:
# W -> ["W", "L"]
# ...

# output csv will look like this:
#	10 by 10 corr	W		FINAL_MARGIN	SHOT_NUMBER	...
#	W				1		0.2				0.5
#	FINAL_MARGIN	0.2		1				-0.8
#	SHOT_NUMBER		0.5		-0.8				1
#	...

import os
import csv
import numpy
import math

def extract10DesiredColumns(columnIdxList, nbaDataset):
	nbaDataset_10 = []
	for record in nbaDataset:
		record_10 = []
		for idx in columnIdxList:
			record_10.append(record[idx])
		nbaDataset_10.append(record_10)
	
	return nbaDataset_10

# ex) "W" attribute array: ["W", "W", "L", "W", ...] -> [0, 0, 1, 0, ...]
# also do the "float-ifiy" for the strings from csv
def modifyNBADataset_10_Categoricals(attributes_10, nbaDataset_10, cateAttrValueDic):
	modifiedNBADataset_10 = []

	cateAttrArray = list(cateAttrValueDic.keys())
	cateAttrColuIndice = []
	for cateAttr in cateAttrArray:
		idx = attributes_10.index(cateAttr)
		cateAttrColuIndice.append(idx)

	# skip first row because it is attribute names
	for record in nbaDataset_10[1:]:
		for i in range(len(cateAttrArray)):
			cateAttrColIdx = cateAttrColuIndice[i]
			i_thCateVal = record[cateAttrColIdx]
			dicElem = cateAttrValueDic[cateAttrArray[i]]	# array
			numValOfCate = dicElem.index(i_thCateVal)
			record[cateAttrColIdx] = numValOfCate
		
		for i in range(len(record)):
			record[i] = float(record[i])

		modifiedNBADataset_10.append(record)
	return modifiedNBADataset_10

def calculateCorrelation(xlist, ylist):
	# formula of correlation calcultation:
	# r(x,y) = sigma((xi-xavg)*(yi-yavg)) / sqrt(sigma((xi-xavg)^2)*sigma((yi-yavg)^2))
	xavg = sum(xlist) / len(xlist)
	yavg = sum(ylist) / len(ylist)

	# numerator
	numerator = 0.0
	for i in range(len(xlist)):
		numerator += (xlist[i]-xavg) * (ylist[i]-yavg)

	# denominator
	x_part_sigma = 0.0
	for i in range(len(xlist)):
		xi_xavg_2 = (xlist[i] - xavg) ** 2
		x_part_sigma += xi_xavg_2

	y_part_sigma = 0.0
	for i in range(len(ylist)):
		yi_yavg_2 = (ylist[i] - yavg) ** 2
		y_part_sigma += yi_yavg_2

	denominator = math.sqrt( x_part_sigma * y_part_sigma )

	corr = numerator / denominator

	return corr

def gen10x10CorrMat(attributes_10, m_nbaDataset_10):
	corrMat10x10 = []
	
	# i-th row
	for i in range(len(attributes_10)):
		xlist = []
		for record in m_nbaDataset_10:
			xlist.append(record[i])
		
		# j-th column 
		i_corr_list = []
		for j in range(len(attributes_10)):
			ylist = []
			for record in m_nbaDataset_10:
				ylist.append(record[j])
			# calculate [i, j] of corr math
			corr_i_j = calculateCorrelation(xlist, ylist)
			i_corr_list.append(corr_i_j)
		
		print(i_corr_list)
		corrMat10x10.append(i_corr_list)
	
	return corrMat10x10

# --- main program starts here ---
numpy.set_printoptions(threshold=numpy.nan)

workDirPath = os.getcwd()
fileName = "NBA_shot_logs_2014_2015_reduced_at1.csv"	# numOfCol: 21, numOfRow: 945
filePath = workDirPath + "\\" + fileName
csvf = open(filePath, "r", newline='')		# csv file

csvFReader = csv.reader(csvf)
nbaDataset = []
i=0
for row in csvFReader:
	if i == 0:
		attributes = row		# assign the first row (array of strings:attrs) to "attributes""
	else:
		nbaDataset.append(row)
	i += 1

numOfRows = i	# include Attribute row
numOfRecords = i-1
numOfAttr = len(attributes)

# list of 10 attributes used for correlation matrix
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
desiredColumnIndice = [4, 5, 6, 7, 9, 10, 11, 12, 13, 16]
attributes_10 = []
for colIdx in desiredColumnIndice:
	attributes_10.append(attributes[colIdx])

# dictionary - key: cateAttr, value: array of value types of the categorical variable
cateAttrValueDic = { 
	'W': ['W', 'L']
	}

nbaDataset_10 = extract10DesiredColumns(desiredColumnIndice, nbaDataset)

# following modified dataset now doesn't have attribute names.
m_nbaDataset_10 = modifyNBADataset_10_Categoricals(attributes_10, nbaDataset_10, cateAttrValueDic)

corrMat10x10 = gen10x10CorrMat(attributes_10, m_nbaDataset_10)

# let's add attribute names for corr mat at 0-th row
firstRow = []
for attr in attributes_10:
	firstRow.append(attr)

# for my style of handling csv files, it is better to set all the data format as string
# note: I don't know why but d3's reading of csv file is weird when using 2dimentional matrix format
# that means I should not put attr names on the first column, only on first row.
exportingFormatDataset = [firstRow]
i=0
for row in corrMat10x10:
	for element in row:
		element = str(element)
	exportingFormatDataset.append(row)
	i += 1
print(exportingFormatDataset)

numpy.savetxt("NBA_shot_10by10CorrMat.csv", exportingFormatDataset, fmt='"%s"', delimiter=",")
