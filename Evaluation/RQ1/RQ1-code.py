# Here is the code for calculating RangeSwing from ranges of ENRICH.

# author: Baharin A. Jodat - University of Ottawa
# last update: 2022 - 04 - 13

import pandas as pd
import numpy as np
import ast

def WriteToExcel(data):

    data.to_excel("RangeSwing.xlsx")

def AddToDataFrame(res, dis, row, col):

    res.loc[row, "RangeSwing Class "+str(k)] = dis

    return res

def Distance(old, new, thresh):
  if len(old) == 1:
    old1 = old
    old2 = [(-1,-1)]
  else:
    old1 = [old[0]]
    old2 = [old[1]]

  if len(new) == 1:
    new1 = new
    new2 = [(-3,-3)]
  else:
    new1 = [new[0]]
    new2 = [new[1]]

  #one old and one new
  if old2[0][0] == -1 and new2[0][0] == -3:
    d1 = abs(old1[0][0] - new1[0][0]) / max(abs(0 - old1[0][0]), abs(old1[0][0] - thresh))
    #print("a - c", abs(old1[0][0] - new1[0][0]))
    return d1
  #one old and two news
  elif old2[0][0] == -1 and new2[0][0] != -1:
    d1 = min(abs(old1[0][0] - new1[0][0])/max(abs(0 - old1[0][0]), abs(old1[0][0] - thresh)) , abs(old1[0][0] - new2[0][0])/max(abs(0 -old1[0][0]), abs(old1[0][0] - thresh)))
    #print("a - c", abs(old1[0][0] - new1[0][0]))
    return d1
  #two old and one new
  elif old2[0][0] != -1 and new2[0][0] == -1:
    d1 = min(abs(old1[0][0] - new1[0][0])/max(abs(0 - old1[0][0]), abs(old1[0][0] - thresh)),abs(old2[0][0] - new1[0][0])/max(abs(0 - old2[0][0]), abs(old2[0][0] - thresh)))
    return d1
  #two old and two new
  elif old2[0][0] != -1 and new2[0][0] != -1:
    d1 = min(abs(old1[0][0] - new1[0][0])/max(abs(0 - old1[0][0]), abs(old1[0][0] - thresh)),abs(old2[0][0] - new1[0][0])/max(abs(0 - old2[0][0]), abs(old2[0][0] - thresh)))
    d2 = min(abs(old1[0][0] - new2[0][0])/max(abs(0 - old1[0][0]), abs(old1[0][0] - thresh)),abs(old2[0][0] - new2[0][0])/max(abs(0 - old2[0][0]), abs(old2[0][0] - thresh)))
    return (d1 + d2)/2


olddata = pd.read_excel("Ranges - ENRICH.xlsx", header=0)

ranges = [[[] for j in range(8)] for i in range(10)]
l = 0
for i in range(10):
    for j in range(i+10*l,i+10*l + 11):
        ranges[i][0].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 0"]))
        ranges[i][1].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 1"]))
        ranges[i][2].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 2"]))
        ranges[i][3].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 3"]))
        ranges[i][4].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 4"]))
        ranges[i][5].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 5"]))
        ranges[i][6].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 6"]))
        ranges[i][7].append(ast.literal_eval(olddata.loc[j, "Selected Bounds TIN 7"]))

    l = l + 1

threshold = [400, 350, 306, 267, 234, 205, 179, 157]

res = pd.DataFrame(columns=['RangeSwing Class 0', 'RangeSwing Class 1', 'RangeSwing Class 2', 'RangeSwing Class 3', 'RangeSwing Class 4', 'RangeSwing Class 5',
                            'RangeSwing Class 6', 'RangeSwing Class 7'])

for j in range(len(ranges)):
    for k in range(len(ranges[j])):
        for i in range(len(ranges[j][k]) - 1):
            dis = Distance(ranges[j][k][i], ranges[j][k][i+1], threshold[k])
            res = AddToDataFrame(res, dis, j*10+i, k)

WriteToExcel(res)

