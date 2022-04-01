# Here is the code for the BASELINE approach. Please note that it is assumed that this code
# is currently in the Documents directory and dpinger is in the home directory. In the case
# that the codes are in other directories, please update the file paths. Moreover, for
# simplicity there is no password set on our router. In the case that your router has a
# password, please update ssh script with the password.

# author: Baharin A. Jodat - University of Ottawa
# last update: 2022 - 03 - 31

import time
import random
import pandas as pd
import numpy as np
from sklearn import tree
from configparser import ConfigParser
import matplotlib.pyplot as plt
import os

np.set_printoptions(threshold=np.inf)

file = 'config.ini'
config = ConfigParser()
config.read(file)

OpenWrtIp = config['routVM']['IP']
OpenWrtUser = config['routVM']['User']
CakeBandwidth = config['routVM']['CAKEbandwidth']

LinuxMachineIp = config['userVM']['IP']
LinuxMachineUser = config['userVM']['User']
LinuxMachinePass = config['userVM']['Password']

ServerIp1 = config['destVM']['IP1']
ServerIp2 = config['destVM']['IP2']
ServerIp3 = config['destVM']['IP3']
ServerIp4 = config['destVM']['IP4']
ServerIp5 = config['destVM']['IP5']
ServerIp6 = config['destVM']['IP6']
ServerIp7 = config['destVM']['IP7']
ServerIp8 = config['destVM']['IP8']

PathReport1 = config['Dpinger']['PathToReport1']
PathReport2 = config['Dpinger']['PathToReport2']
PathReport3 = config['Dpinger']['PathToReport3']
PathReport4 = config['Dpinger']['PathToReport4']
PathReport5 = config['Dpinger']['PathToReport5']
PathReport6 = config['Dpinger']['PathToReport6']
PathReport7 = config['Dpinger']['PathToReport7']
PathReport8 = config['Dpinger']['PathToReport8']
Report1Name = config['Dpinger']['Report1Name']
Report2Name = config['Dpinger']['Report2Name']
Report3Name = config['Dpinger']['Report3Name']
Report4Name = config['Dpinger']['Report4Name']
Report5Name = config['Dpinger']['Report5Name']
Report6Name = config['Dpinger']['Report6Name']
Report7Name = config['Dpinger']['Report7Name']
Report8Name = config['Dpinger']['Report8Name']

def yclasses(data):
    ylatency = []

    for i in data.columns[24:25]:
        yl = data.loc[:, f"{i}"].to_numpy()
        ylatency.append(yl)

    return ylatency


def xfeatures(data):
    x = []

    for i in range(len(data.index)):
        lisst = []
        lisst.append(data.loc[i, "TIN 0 Req-BW"])
        lisst.append(data.loc[i, "TIN 1 Req-BW"])
        lisst.append(data.loc[i, "TIN 2 Req-BW"])
        lisst.append(data.loc[i, "TIN 3 Req-BW"])
        lisst.append(data.loc[i, "TIN 4 Req-BW"])
        lisst.append(data.loc[i, "TIN 5 Req-BW"])
        lisst.append(data.loc[i, "TIN 6 Req-BW"])
        lisst.append(data.loc[i, "TIN 7 Req-BW"])

        x.append(lisst)

    x = np.array(x)

    return x

def DecisionTree(x, yclass, index, mosorlatency, data):

    clf = tree.DecisionTreeRegressor()

    clf = clf.fit(x, yclass, sample_weight=None)

    plt.figure(figsize=(200, 200))

    _ = tree.plot_tree(clf,
                           filled=True, fontsize=20, rounded=True)

    filename = "mos" + str(index) + '.png'
    plt.savefig(filename)
    plt.close('all')
    # plt.show()

    dot_data = tree.export_graphviz(clf, out_file='tree' + mosorlatency + str(index),
                                        feature_names=data.columns[0:8],
                                        filled=True, rounded=True)

    # graph = graphviz.Source(dot_data)
    return clf

def ReadTree(file):
    f = open(file, "r")

    datafromtree = f.read().split('\n')

    datafromtree = datafromtree[3:]

    arrows = []
    nodes = []

    for i in range(len(datafromtree)):

        if '->' in datafromtree[i]:
            arrows.append(datafromtree[i])

        else:
            nodes.append(datafromtree[i])

    nodes = nodes[:-1]
    for i in range(len(arrows)):
        if ' [' in arrows[i]:
            ind = arrows[i].index(' [')
            arrows[i] = arrows[i][:ind]
        if ' ;' in arrows[i]:
            ind = arrows[i].index(' ;')
            arrows[i] = arrows[i][:ind]

    f.close()
    return arrows, nodes


def convertoint(arrows):
    for i in range(len(arrows)):
        if ' ' in arrows[i]:
            arrows[i] = arrows[i].replace(' ', '')

    return arrows

def extractpath(root, arrows):
    path = []
    i = 0
    while i < len(arrows):
        firstpart = int(arrows[i][0])
        ind = arrows[i].index('>')
        secondpart = int(arrows[i][ind + 1:])
        if int(root) == firstpart:
            path.append(arrows[i])
            root = secondpart
            i = 0
        i = i + 1

    return path

def checkforchild(node, arrows):
    ind = node.index('>')
    child = node[ind + 1:]
    children = []
    for i in range(len(arrows)):
        ind = arrows[i].index('-')
        if child == arrows[i][:ind]:
            children.append(arrows[i])

    return children

def FindListofPaths(listofallpaths, path, arrows):
    removed = []
    path.insert(0, '0->0')
    while (len(path) != 0):
        last = path[-1]
        b = checkforchild(last, arrows)
        if len(b) == 0:
            listofallpaths.append(path[:])
            path.remove(last)
            removed.append(last)
        else:
            i = 0
            while i < len(b):
                if b[i] in removed:
                    b.remove(b[i])
                    i = -1
                elif b[i] not in removed:
                    path.append(b[i])
                    break
                if len(b) == 0:
                    path.remove(last)
                    removed.append(last)
                    break
                i = i + 1

    listofallpaths = listofallpaths[1:]

    for i in range(len(listofallpaths)):
        listofallpaths[i].remove('0->0')

    return listofallpaths

def extractlabel(node, arrows):
    ind = node.index('-')
    first = node[:ind]
    ind = node.index('>')
    second = node[ind + 1:]
    for i in range(len(arrows)):
        ind = arrows[i].index('-')
        if first == arrows[i][:ind] and node != arrows[i]:
            if int(second) < int(arrows[i][ind + 2:]):
                return True
            else:
                return False

def FindRules(listofallpaths, arrows, nodes):
    rules = []
    for i in range(len(listofallpaths)):
        rule = []
        for j in range(len(listofallpaths[i])):
            a = extractlabel(listofallpaths[i][j], arrows)
            ind = listofallpaths[i][j].index('-')
            first = listofallpaths[i][j][:ind]
            for k in range(len(nodes)):
                listt = []
                ind = nodes[k].index(' [')
                if first == nodes[k][:ind]:
                    ind = nodes[k].index('"')
                    ind2 = nodes[k].index('\\')
                    listt.append(nodes[k][ind + 1:ind2])
                    listt.append(a)
                    ind = nodes[k].index('value')
                    ind2 = nodes[k].index('", fillcolor')
                    listt.append(nodes[k][ind:ind2])
                    rule.append(listt)

        ind = listofallpaths[i][len(listofallpaths[i]) - 1].index('>')
        second = listofallpaths[i][j][ind + 1:]
        for k in range(len(nodes)):
            listt = []
            ind = nodes[k].index(' [')
            if second == nodes[k][:ind]:
                ind = nodes[k].index('value')
                ind2 = nodes[k].index('", fillcolor')
                listt.append(nodes[k][ind:ind2])
                rule.append(listt)

        rules.append(rule)

    return rules

def FindLogicalRules(rules, data):
    logicalrules = []
    for i in range(len(rules)):
        s = ''
        for j in range(len(rules[i]) - 1):
            if rules[i][j][1] == True:
                s = s + rules[i][j][0] + ' ^ '
            else:
                s = s + 'Not( ' + rules[i][j][0] + ' )' + ' ^ '
        s = s[:-3]
        s = s + ' ' + rules[i][-1][0]  # class
        logicalrules.append(s)

    return logicalrules

def NumberofDistincTins(b, a):

    tinsa = [0 for i in range(8)]
    tinsb = [0 for i in range(8)]

    for i in range(len(b)):
        for j in range(len(tinsb)):
            if 'TIN ' + str(j) in b[i]:
                tinsb[j] = 1

    for i in range(len(a)):
        for j in range(len(tinsa)):
            if 'TIN ' + str(j) in a[i]:
                tinsa[j] = 1

    if sum(tinsb) > sum(tinsa):
        return True

    return False

def SeparateGoodandBad():
    f = open("logicalrulesoftress.txt", "r")
    datafromrules = f.read().split("***")
    for i in range(len(datafromrules)):
        datafromrules[i] = datafromrules[i][:-1]
        datafromrules[i] = datafromrules[i].split('\n')

    datafromrules = datafromrules[:-1]

    for i in range(len(datafromrules)):
        datafromrules[i].sort(key=lambda x: float(x.split()[-1]))

    separatedclasses = []

    i = 0
    for j in range(len(datafromrules[i])):
        lisst = []
        if float(datafromrules[i][j].split()[-1]) >= 3.6:  # threshold
            h = j + 1
            longer = datafromrules[i][j]
            while (h < len(datafromrules[i]) and datafromrules[i][j].split()[-1] == datafromrules[i][h].split()[
                -1]):
                b = datafromrules[i][h].split(" ^ ")
                if len(longer.split(" ^ ")) <= len(b):
                    if len(longer.split(" ^ ")) == len(b):
                        if NumberofDistincTins(b, longer.split(" ^ ")) == True:
                            longer = datafromrules[i][h]
                    else:
                        longer = datafromrules[i][h]

                h = h + 1
            rule1 = longer
            rule2 = datafromrules[i][j - 1]
            h = j - 2
            longer = datafromrules[i][j - 1]
            while (h > 0) and datafromrules[i][j - 1].split()[-1] == datafromrules[i][h].split()[-1]:
                b = datafromrules[i][h].split(" ^ ")
                if len(longer.split(" ^ ")) <= len(b):
                    if len(longer.split(" ^ ")) == len(b):
                        if NumberofDistincTins(b, longer.split(" ^ ")) == True:
                            longer = datafromrules[i][h]
                    else:
                        longer = datafromrules[i][h]
                h = h - 1
            rule2 = longer
            lisst.append(rule1)
            lisst.append(rule2)
            separatedclasses.append(lisst)
            break

    return separatedclasses

def CheckForValidSplit(condition):
    thresh = 3.6

    f = open("treeMOS0", "r")
    f = f.read().split("\n")
    label = condition[:condition.index('-')]
    arrows, nodes = ReadTree("treeMOS0")

    # find labels of children
    children = []
    for j in range(len(arrows)):
        ind = arrows[j].index("-")
        if label == arrows[j][:ind - 1]:
            children.append(arrows[j][ind + 3:])
    # find values of children
    values = []
    for j in range(len(f)):
        if children[0] + " [" == f[j][:len(children[0]) + 2]:
            ind = f[j].index("value")
            ind2 = f[j].index('", fillcolor')
            values.append(float(f[j][ind + 8:ind2]))
        if children[1] + " [" == f[j][:len(children[1]) + 2]:
            ind = f[j].index("value")
            ind2 = f[j].index('", fillcolor')
            values.append(float(f[j][ind + 8:ind2]))

    if values[0] >= thresh and values[1] >= thresh:
        return False
    elif values[0] < thresh and values[1] < thresh:
        return False
    else:
        return True

def ExtractBounds(finalboundaries, listofallpaths):
    tinthresholds = [400, 350, 306, 267, 234, 205, 179, 157]

    bounds = [[] for i in range(8)]
    f = open("logicalrulesoftress.txt", "r")
    f = f.read().split("\n")
    i = 0

    intersections = [[] for i in range(8)]
    rule1 = finalboundaries[i][0].split(' ^ ')
    rule2 = finalboundaries[i][1].split(' ^ ')

    for kk in range(len(f)):
        if finalboundaries[i][0] == f[kk]:
            rule1index = listofallpaths[kk]

    for kk in range(len(f)):
        if finalboundaries[i][1] == f[kk]:
            rule2index = listofallpaths[kk]

    ind = rule1[-1].index(' value')
    rule1[-1] = rule1[-1][:ind]
    ind = rule2[-1].index(' value')
    rule2[-1] = rule2[-1][:ind]
    copyrule1 = rule1
    minn = min(len(rule1), len(rule2))
    j = 0

    while j < minn and rule1[j] == rule2[j]:  # common part
        flag = False
        tinflag = False
        if rule1[j][0] != 'N':
            flag = False
        else:
            rule1[j] = rule1[j][:-2]
            flag = True
        try:
            ind = rule1[j].index('TIN')
        except ValueError:
            ind = rule1[j].index('sum')
            tinflag = True
        if tinflag == False:
            tin = int(rule1[j][ind + 4])
        else:
            tin = 8
        ind = rule1[j].index('<=')
        threshold = int(float(rule1[j][ind + 3:]))
        intersections[tin].append((threshold, flag))
        j = j + 1

    ##Path reduction
    k = j
    l = len(rule1) - 1
    a = rule1index[l]

    while l > k and CheckForValidSplit(a) == False:
        rule1.remove(rule1[l])
        l = l - 1
        a = rule1index[l]

    l = len(rule2) - 1
    a = rule2index[l]

    while l > k and CheckForValidSplit(a) == False:
        rule2.remove(rule2[l])
        l = l - 1
        a = rule2index[l]

    h = j
    while j < len(rule1):  # non-common part
        flag = False
        tinflag = False
        if rule1[j][0] != 'N':
            flag = False
        else:
            rule1[j] = rule1[j][:-2]
            flag = True
        try:
            ind = rule1[j].index('TIN')
        except ValueError:
            ind = rule1[j].index("sum")
            tinflag = True
        if tinflag == False:
            tin = int(rule1[j][ind + 4])
        else:
            tin = 8
        ind = rule1[j].index('<=')
        threshold = int(float(rule1[j][ind + 3:]))
        intersections[tin].append((threshold, flag))
        j = j + 1

    while h < len(rule2):
        flag = False
        tinflag = False
        if rule2[h][0] != 'N':
            flag = False
        else:
            rule2[h] = rule2[h][:-2]
            flag = True
        try:
            ind = rule2[h].index('TIN')
        except ValueError:
            ind = rule2[h].index('sum')
            tinflag = True
        if tinflag == False:
            tin = int(rule2[h][ind + 4])
        else:
            tin = 8
        ind = rule2[h].index('<=')
        threshold = int(float(rule2[h][ind + 3:]))
        intersections[tin].append((threshold, flag))
        h = h + 1

    for j in range(len(intersections)):
        if len(intersections[j]) > 0:
            falses = []
            trues = []
            for h in range(len(intersections[j])):
                if intersections[j][h][1] == False:  # no Not
                    falses.append(intersections[j][h][0])
                else:  # Not
                    trues.append(intersections[j][h][0])

            flagthreshold = False
            try:
                up = min(falses)
            except ValueError:
                up = tinthresholds[j]
                flagthreshold = True
            try:
                down = max(trues)
            except ValueError:
                down = 0

            if down != 0:
                bounds[j].append((max(int(down - 20), 0), min(int(down + 20), tinthresholds[j]), 'lower'))

            if flagthreshold == False:
                bounds[j].append((max(int(up - 20), 0), min(int(up + 20), tinthresholds[j]), 'upper'))

    for i in range(len(bounds)):
        bounds[i] = list(set(bounds[i]))

    for i in range(len(bounds)):
        if len(bounds[i]) == 0:
            bounds[i].append((0, tinthresholds[i], 'upper'))

    array = [0 for i in range(8)]
    for i in range(len(bounds)):
        rand = random.randint(0, len(bounds[i]) - 1)
        chosen = bounds[i][rand]
        array[i] = random.randint(bounds[i][rand][0], bounds[i][rand][1])

    return array, bounds

def MainProduceDecisionTree(data):
    ylatency = yclasses(data)
    xfeaturess = xfeatures(data)

    clf = DecisionTree(xfeaturess, ylatency[0], 0, data)

    f = open("logicalrulesoftress.txt", "w")

    arrows, nodes = ReadTree('tree' + 'MOS0')
    arrows = convertoint(arrows)
    listofallpaths = []
    path = extractpath(0, arrows)
    listofallpaths.append(path)
    listofallpaths = FindListofPaths(listofallpaths, path, arrows)

    rules = FindRules(listofallpaths, arrows, nodes)
    logicalrules = FindLogicalRules(rules, data)
    for i in range(len(logicalrules)):
        f.write(logicalrules[i])
        f.write('\n')
    f.write('***')

    f.close()
    return listofallpaths

def ComputeDistance(point, selectedpoints):
    distances = []
    for i in range(len(selectedpoints)):
        d = np.linalg.norm(np.array(point) - np.array(selectedpoints[i]))
        distances.append(d)

    return min(distances)

def GeneratePoints(finalboundaries):
    selectedpoints = []
    newarray = ExtractBounds(finalboundaries)
    selectedpoints.append(newarray)

    while len(selectedpoints) < 20:
        distancesofallpoints = []
        randompoints = []
        for i in range(10):
            randompoints.append(ExtractBounds(finalboundaries))

        for i in range(len(randompoints)):
            minn = ComputeDistance(randompoints[i], selectedpoints)
            distancesofallpoints.append(minn)

        newselectedpoint = randompoints[distancesofallpoints.index(max(distancesofallpoints))]
        selectedpoints.append(newselectedpoint)

    return selectedpoints

def GeneratePointsNaiveAdaptiveSearch():

    selectedpoints = []
    newarray = InitialGeneratePoint()
    selectedpoints.append(newarray)

    while len(selectedpoints) < 20:
        distancesofallpoints = []
        randompoints = []
        for i in range(10):
            randompoints.append(InitialGeneratePoint())

        for i in range(len(randompoints)):
            minn = ComputeDistance(randompoints[i], selectedpoints)
            distancesofallpoints.append(minn)

        newselectedpoint = randompoints[distancesofallpoints.index(max(distancesofallpoints))]
        selectedpoints.append(newselectedpoint)

    return selectedpoints

def InitialGeneratePoint():

    randomnuttcparray = [0 for i in range(8)]

    randomnuttcparray[0] = random.randint(0,400)
    randomnuttcparray[1] = random.randint(0,350)
    randomnuttcparray[2] = random.randint(0,306)
    randomnuttcparray[3] = random.randint(0,267)
    randomnuttcparray[4] = random.randint(0,234)
    randomnuttcparray[5] = random.randint(0,205)
    randomnuttcparray[6] = random.randint(0,179)
    randomnuttcparray[7] = random.randint(0,157)

    total = 0
    for i in range(8):
        total = total + randomnuttcparray[i]

    dif = 1
    if total > 600:
        dif = 600/total

    for i in range(8):
        randomnuttcparray[i] = int(randomnuttcparray[i] * dif)
        if randomnuttcparray[i] < 1:
            randomnuttcparray[i] = 0

    return randomnuttcparray

def AddToDataFrame(olddata, selectedpoint, alldpinger):
    for i in range(len(alldpinger)):
        if alldpinger[i][0] == -1 or alldpinger[i][3] == -1:
            return olddata, True

    olddata.loc[olddata.shape[0]] = [int(selectedpoint[0]), int(selectedpoint[1]), int(selectedpoint[2]),
                                     int(selectedpoint[3]), int(selectedpoint[4]), int(selectedpoint[5]),
                                     int(selectedpoint[6]), int(selectedpoint[7]),
                                     int(alldpinger[0][0]), int(alldpinger[1][0]), int(alldpinger[2][0]),
                                     int(alldpinger[3][0]), int(alldpinger[4][0]), int(alldpinger[5][0]),
                                     int(alldpinger[6][0]), int(alldpinger[7][0]),
                                     float(alldpinger[0][3]), float(alldpinger[1][3]), float(alldpinger[2][3]),
                                     float(alldpinger[3][3]), float(alldpinger[4][3]), float(alldpinger[5][3]),
                                     float(alldpinger[6][3]), float(alldpinger[7][3]),
                                     400, 350, 306, 267, 234, 205, 179, 157]

    return olddata, False

def DeleteFiles():

    file1 = 'MOS0' + '.png'
    file2 = 'tree' + 'MOS0'
    try:
        f = open(file1)
        f = open(file2)
    except OSError:
        return

    os.system("gnome-terminal -- bash -c 'rm " + file1 + "; exit; exec bash'")
    os.system("gnome-terminal -- bash -c 'rm " + file2 + "; exit; exec bash'")

    os.system("gnome-terminal -- bash -c 'rm logicalrulesoftrees.txt ; exit; exec bash'")

def GenerateTraffic(randomnuttcparray, l):

    ports = ['5101', '5102', '5103', '5104', '5105', '5106', '5107', '5108']

    servers = [ServerIp1, ServerIp2, ServerIp3, ServerIp4, ServerIp5, ServerIp6, ServerIp7, ServerIp8]
    for i in range(len(randomnuttcparray)):
        if randomnuttcparray[i] != 0:
            os.system("gnome-terminal -- bash -c 'nuttcp -b -N1 -p" + str(ports[i]) + " -T60s -R" + str(
                randomnuttcparray[i]) + "M " + servers[i] + " >> randomtraffic" + str(l) + str(
                i) + ".txt; exit; exec bash'")

def RunDpinger():
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link11.pid -u /var/run/link11.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport1 + " " + ServerIp1 + "; sleep 0; exit; exec bash'")
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link12.pid -u /var/run/link12.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport2 + " " + ServerIp2 + "; sleep 0; exit; exec bash'")
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link13.pid -u /var/run/link13.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport3 + " " + ServerIp3 + "; sleep 0; exit; exec bash'")
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link14.pid -u /var/run/link14.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport4 + " " + ServerIp4 + "; sleep 0; exit; exec bash'")
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link15.pid -u /var/run/link15.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport5 + " " + ServerIp5 + "; sleep 0; exit; exec bash'")
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link16.pid -u /var/run/link16.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport6 + " " + ServerIp6 + "; sleep 0; exit; exec bash'")
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link17.pid -u /var/run/link17.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport7 + " " + ServerIp7 + "; sleep 0; exit; exec bash'")
    os.system(
        "gnome-terminal -- bash -c 'cd ..; cd dpinger; sudo ./dpinger -S -i link1 -B " + LinuxMachineIp + " -p /var/run/dpinger_link18.pid -u /var/run/link18.sock -C /etc/rc.failover -s 100 -l 400 -t 40s -r 40s -A 1s -D 900 -L 22 -d 256 -R -o " + PathReport8 + " " + ServerIp8 + "; sleep 0; exit; exec bash'")

def KillDpinger():
    for j in range(8):
        os.system("gnome-terminal -- bash -c 'pgrep dpinger | tail -1 |sudo xargs kill -9; exit; exec bash'")

def ReadDpinger():
    #################Read Dpinger####################
    valueofdpingers = []

    files = [Report8Name, Report7Name, Report6Name, Report5Name, Report4Name, Report3Name, Report2Name, Report1Name]
    for j in range(8):
        with open(files[j]) as f:
            data = f.read()

        comp = data.split(" ")
        comp = comp[1:]
        try:
            comp[-1] = comp[-1][:-1]
        except IndexError:
            comp= [-1]

        for i in range(len(comp)):
            comp[i] = float(comp[i])

        valueofdpingers.append(comp)

    return valueofdpingers

def DeleteRandomTrafficFiles():
    for i in range(100):
        for j in range(8):
            if i == 0 and j == 0:
                continue
            else:
                file = 'randomtraffic' + str(i) + str(j) + '.txt'

                try:
                    f = open(file)
                except OSError:
                    continue

                os.system("gnome-terminal -- bash -c 'rm " + file + "; exit; exec bash'")

def WriteToExcel(data, s):

    data.to_excel("allthegenerateddata" + s + ".xlsx")

def AddBoundstoDataFrame(allbounds, newbounds):
  allbounds.loc[allbounds.shape[0]] = [newbounds[0], newbounds[1],newbounds[2],newbounds[3],newbounds[4],newbounds[5],newbounds[6],newbounds[7]]

  return allbounds

def AdaptiveRandomSearch():

    olddata = pd.DataFrame(columns=['TIN 0 Req-BW', 'TIN 1 Req-BW', 'TIN 2 Req-BW', 'TIN 3 Req-BW', 'TIN 4 Req-BW', 'TIN 5 Req-BW',
                                    'TIN 6 Req-BW', 'TIN 7 Req-BW', 'TIN 0 Latency', 'TIN 1 Latency', 'TIN 2 Latency',
                                    'TIN 3 Latency', 'TIN 4 Latency', 'TIN 5 Latency', 'TIN 6 Latency', 'TIN 7 Latency',
                                    'TIN 0 MOS', 'TIN 1 MOS', 'TIN 2 MOS', 'TIN 3 MOS', 'TIN 4 MOS', 'TIN 5 MOS',
                                    'TIN 6 MOS', 'TIN 7 MOS', 'TIN 0 Thresh', 'TIN 1 Thresh', 'TIN 2 Thresh',
                                    'TIN 3 Thresh', 'TIN 4 Thresh', 'TIN 5 Thresh', 'TIN 6 Thresh', 'TIN 7 Thresh'])

    i = 0
    while len(olddata.index) < 301:
        newarray = GeneratePointsNaiveAdaptiveSearch() #20 arrays
        DeleteFiles()
        DeleteRandomTrafficFiles()
        for j in range(len(newarray)):
            GenerateTraffic(newarray[j], j)
            time.sleep(10)
            RunDpinger()
            time.sleep(41)
            KillDpinger()
            time.sleep(90)
            alldpinger = ReadDpinger()
            alldpinger.reverse()
            olddata, flag = AddToDataFrame(olddata,newarray[j],alldpinger)

        WriteToExcel(olddata, str(i))
        i = i + 1

    WriteToExcel(olddata, "end")
    return olddata

os.system(
    "gnome-terminal -- bash -c 'ssh " + OpenWrtUser + "@" + OpenWrtIp + " -yes tc qdisc del dev eth1 root; exit; exit; exec bash'")
os.system(
    "gnome-terminal -- bash -c 'ssh " + OpenWrtUser + "@" + OpenWrtIp + " -yes tc qdisc replace dev eth1 root handle 1: cake ether-vlan nat diffserv8 bandwidth " + CakeBandwidth + "mbit flowblind ack-filter-aggressive no-split-gso; exit; exit; exec bash'")

time.sleep(2)

olddata = AdaptiveRandomSearch()

allbounds = pd.DataFrame(columns=['TIN 0 Range', 'TIN 1 Range', 'TIN 2 Range', 'TIN 3 Range', 'TIN 4 Range', 'TIN 5 Range',
                                    'TIN 6 Range', 'TIN 7 Range'])

listofallpaths = MainProduceDecisionTree(olddata)
separatedclasses = SeparateGoodandBad()
_, newbounds = ExtractBounds(separatedclasses, listofallpaths)
allbounds = AddBoundstoDataFrame(allbounds,newbounds)
WriteToExcel(allbounds,"allbounds", " ")
