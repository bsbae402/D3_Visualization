# print_console_abs_corr_sum.py
# target file name: NBA_shot_10by10CorrMat.csv

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

# check the console for the output

import os
import csv
import numpy
import math

# --- main program starts here ---
numpy.set_printoptions(threshold=numpy.nan)

workDirPath = os.getcwd()
fileName = "NBA_shot_10by10CorrMat.csv"	
filePath = workDirPath + "\\" + fileName
csvf = open(filePath, "r", newline='')		# csv file

csvFReader = csv.reader(csvf)
corrMat = []
i=0
for row in csvFReader:
	if i == 0:
		attributes = row		# assign the first row (array of strings:attrs) to "attributes""
	else:
		corrMat.append(row)
	i += 1

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

absCorrSumList = []
for row in corrMat:
	sum = 0
	for corr_i_j in row:
		sum += abs(float(corr_i_j))
	absCorrSumList.append(sum)

for i in range(len(absCorrSumList)):
	print(attributes[i] + " : " + str(absCorrSumList[i]))
