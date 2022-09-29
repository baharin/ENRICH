# Below is the code for getting accuracy and recall for 20 perturbations of the results

# author : Baharin A. Jodat - University of Ottawa
# Last Update: 2022 - 09 - 29

import random
import pandas as pd
import numpy as np

np.set_printoptions(threshold=np.inf)

def LabelData(olddata, chosenruns):

    for i in range(len(olddata.index)):
        labelsofruns = []
        for j in range(len(chosenruns)):
            labelsofruns.append(olddata.loc[i, '#Var Covered' + str(chosenruns[j])])

        if max(labelsofruns) == 8: #if any of the labels is non robust
            olddata.loc[i, 'Final Enrich Label (OR)'] = 'Non Robust' #replace with 'Final Baseline Label (OR)' for BASELINE
        else:
            olddata.loc[i, 'Final Enrich Label (OR)'] = 'Robust' #replace with 'Final Baseline Label (OR)' for BASELINE

    return olddata

def CalculateRobustnessRecall(olddata):

    #calculate Recall
    truelylabeled = 0
    for i in range(len(olddata.index)):
        #total number of true robust labels
        if olddata.loc[i, 'Final Enrich Label (OR)'] == 'Robust' and olddata.loc[i, 'Real Label'] == 'Robust': #replace with 'Final Baseline Label (OR)' for BASELINE
            truelylabeled = truelylabeled + 1

    c = 0
    for i in range(len(olddata.index)):
        if olddata.loc[i, 'Real Label'] == 'Robust':
            c = c + 1 #total number of real robust labels

    r = truelylabeled / c

    return r

def CalculateNonRobustnessRecall(olddata):

    #calculate Recall
    truelylabeled = 0
    for i in range(len(olddata.index)):
        #total number of true non-robust labels
        if olddata.loc[i, 'Final Enrich Label (OR)'] == 'Non Robust' and olddata.loc[i, 'Real Label'] == 'Non Robust': #replace with 'Final Baseline Label (OR)' for BASELINE
            truelylabeled = truelylabeled + 1

    c = 0
    for i in range(len(olddata.index)):
        if olddata.loc[i, 'Real Label'] == 'Non Robust':
            c = c + 1 #total number of real non robust labels

    r = truelylabeled / c

    return r

def CalculateAccuracy(olddata):

    #accuracy = (TP + TN) / (TP + TN + FP + FN)
    trues = 0

    for i in range(len(olddata.index)):
        if olddata.loc[i, 'Final Enrich Label (OR)'] == olddata.loc[i, 'Real Label']: #replace with 'Final Baseline Label (OR)' for BASELINE
            trues = trues + 1

    accuracy = trues / len(olddata.index)

    return accuracy

def UpdateFinalData(finaldata, r, accuracy, chosenruns, numberofruns):

    runs = ['No' for i in range(15)]

    for i in range(len(chosenruns)):
        runs[chosenruns[i]] = 'Yes'

    finaldata.loc[finaldata.shape[0]] = [numberofruns, r, accuracy, runs[0], runs[1], runs[2], runs[3], runs[4], runs[5], runs[6], runs[7], runs[8], runs[9], runs[10], runs[11], runs[12], runs[13], runs[14]]

    return finaldata


olddata = pd.read_excel("data.xlsx", header=0) #read the data for the desired epsilon

finaldata = pd.DataFrame(columns=['NumofRuns', 'Recall', 'Accuracy', 'Run 0', 'Run 1', 'Run 2', 'Run 3', 'Run 4', 'Run 5', 'Run 6', 'Run 7', 'Run 8', 'Run 9', 'Run 10', 'Run 11', 'Run 12', 'Run 13', 'Run 14'])

for numberofruns in range(1,16):
    pr = []
    for i in range(20):
        chosenruns = []
        for k in range(numberofruns):
            a = random.randint(0, 14)
            while a in chosenruns:
                a = random.randint(0, 14)

            chosenruns.append(a)

        olddata = LabelData(olddata, chosenruns)
        recall = CalculateRobustnessRecall(olddata)  #replace with CalculateNonRobustnessRecall(olddata) for getting the non-robustness recall
        accuracy = CalculateAccuracy(olddata)
        finaldata = UpdateFinalData(finaldata, recall, accuracy, chosenruns, numberofruns)

finaldata.to_excel('finaldata20times.xlsx')
