import time
import random
import pandas as pd
import numpy as np
from configparser import ConfigParser
import os
import ast

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

    data.to_excel("results" + s + ".xlsx")

def AddToDataFrame(olddata, selectedpoint, alldpinger, f):
    print(alldpinger)
    for i in range(len(alldpinger)):
        if type(alldpinger[i][0]) != str and (alldpinger[i][0] == -1 or alldpinger[i][3] == -1):
            return olddata, True

    olddata.loc[olddata.shape[0]] = [int(selectedpoint[0]), int(selectedpoint[1]), int(selectedpoint[2]),
                                     int(selectedpoint[3]), int(selectedpoint[4]), int(selectedpoint[5]),
                                     int(selectedpoint[6]), int(selectedpoint[7]), float(f),
                                     int(alldpinger[0][0]), int(alldpinger[1][0]), int(alldpinger[2][0]),
                                     int(alldpinger[3][0]), int(alldpinger[4][0]), int(alldpinger[5][0]),
                                     int(alldpinger[6][0]), int(alldpinger[7][0]),
                                     float(alldpinger[0][3]), float(alldpinger[1][3]), float(alldpinger[2][3]),
                                     float(alldpinger[3][3]), float(alldpinger[4][3]), float(alldpinger[5][3]),
                                     float(alldpinger[6][3]), float(alldpinger[7][3]),
                                     400, 350, 306, 267, 234, 205, 179, 157]


    return olddata, False

def Preprocess(alldpinger):

    for i in range(len(alldpinger)):
        alldpinger[i][3] = alldpinger[i][3] / (alldpinger[i][3] + 1)

    return alldpinger

def CalculateRobustnessMeasure(alldpinger):

    for i in range(len(alldpinger)):
        if alldpinger[i][0] == -1 or alldpinger[i][3] == -1:
            return -1, True

    if alldpinger[4][3] < 0.8:
        return alldpinger[4][3], False
    elif alldpinger[4][3] >= 0.8 and alldpinger[3][3] < 0.8:
        return 1 + alldpinger[3][3], False
    elif alldpinger[4][3] >= 0.8 and alldpinger[3][3] >= 0.8 and alldpinger[2][3] < 0.8:
        return 2 + alldpinger[2][3], False
    elif alldpinger[4][3] >= 0.8 and alldpinger[3][3] >= 0.8 and alldpinger[2][3] >= 0.8 and alldpinger[1][3] < 0.75:
        return 3 + alldpinger[1][3], False
    elif alldpinger[4][3] >= 0.8 and alldpinger[3][3] >= 0.8 and alldpinger[2][3] >= 0.8 and alldpinger[1][3] >= 0.75 and alldpinger[0][3] < 0.66:
        return 4 + alldpinger[0][3], False
    elif alldpinger[4][3] >= 0.8 and alldpinger[3][3] >= 0.8 and alldpinger[2][3] >= 0.8 and alldpinger[1][3] >= 0.75 and alldpinger[0][3] >= 0.66:
        return 5, False

def decrement(newarray, res):

    ress = []

    for j in range(len(newarray)):
        newarray[j] = newarray[j] - 5
        if newarray[j] < 0:
            newarray[j] = 0
        if newarray[j] > thresh[j]:
            newarray[j] = thresh[j]
    i = 0
    while len(ress) < 5:

        DeleteRandomTrafficFiles()
        GenerateTraffic(newarray, i)
        time.sleep(10)
        RunDpinger()
        time.sleep(41)
        KillDpinger()
        time.sleep(90)
        alldpinger = ReadDpinger()  
        alldpinger.reverse()
        if CheckDpinger(alldpinger) == False:
            alldpinger = Preprocess(alldpinger)
            f , _ = CalculateRobustnessMeasure(alldpinger)

        else:
            f = -1

        res, flag = AddToDataFrame(res,newarray,alldpinger, f)

        if flag == False:
            for j in range(len(newarray)):
                newarray[j] = newarray[j] - 5
                if newarray[j] < 0:
                    newarray[j] = 0
                if newarray[j] > thresh[j]:
                    newarray[j] = thresh[j]
            ress.append(newarray)
        i= i + 1
    return res

def increment(newarray, res):

    ress = []
    i = 0
    for j in range(len(newarray)):
        newarray[j] = newarray[j] + 5
        if newarray[j] < 0:
            newarray[j] = 0
        if newarray[j] > thresh[j]:
            newarray[j] = thresh[j]

    while len(ress) < 5:

        DeleteRandomTrafficFiles()
        GenerateTraffic(newarray, i)
        time.sleep(10)
        RunDpinger()
        time.sleep(41)
        KillDpinger()
        time.sleep(90)
        alldpinger = ReadDpinger() 
        alldpinger.reverse()
        if CheckDpinger(alldpinger) == False:
            alldpinger = Preprocess(alldpinger)
            f , _ = CalculateRobustnessMeasure(alldpinger)
        else:
            f = -1
        res, flag = AddToDataFrame(res,newarray,alldpinger, f)

        if flag == False:
            for j in range(len(newarray)):
                newarray[j] = newarray[j] + 5
                if newarray[j] < 0:
                    newarray[j] = 0
                if newarray[j] > thresh[j]:
                    newarray[j] = thresh[j]
            ress.append(newarray)

        i= i + 1
    return res

def CheckDpinger(alldpinger):
    for i in range(len(alldpinger)):
        if type(alldpinger[i][0]) != str and (alldpinger[i][0] == -1 or alldpinger[i][3] == -1):
            return True

    return False


os.system(
    "gnome-terminal -- bash -c 'ssh " + OpenWrtUser + "@" + OpenWrtIp + " -yes tc qdisc del dev eth1 root; exit; exit; exec bash'")
os.system(
    "gnome-terminal -- bash -c 'ssh " + OpenWrtUser + "@" + OpenWrtIp + " -yes tc qdisc replace dev eth1 root handle 1: cake ether-vlan nat diffserv8 bandwidth " + CakeBandwidth + "mbit flowblind ack-filter-aggressive no-split-gso; exit; exit; exec bash'")

time.sleep(2)

thresh = [400, 350, 306, 267, 234, 205, 179, 157]
i = 0

alldpinger = [[0,0,0,0] for j in range(8)]
oldalldpinger = alldpinger

newarray = [0 for j in range(8)]

olddata = pd.read_excel("Ranges - BASELINE.xlsx", header=0) #change the file name to "Ranges - ENRICH.xlsx" for ENRICH.

ranges = [[[] for j in range(8)] for i in range(10)]

for i in range(len(olddata.index)):
    ranges[i][0] = ast.literal_eval(olddata.loc[i, "Bounds TIN 0"])
    ranges[i][1] = ast.literal_eval(olddata.loc[i, "Bounds TIN 1"])
    ranges[i][2] = ast.literal_eval(olddata.loc[i, "Bounds TIN 2"])
    ranges[i][3] = ast.literal_eval(olddata.loc[i, "Bounds TIN 3"])
    ranges[i][4] = ast.literal_eval(olddata.loc[i, "Bounds TIN 4"])
    ranges[i][5] = ast.literal_eval(olddata.loc[i, "Bounds TIN 5"])
    ranges[i][6] = ast.literal_eval(olddata.loc[i, "Bounds TIN 6"])
    ranges[i][7] = ast.literal_eval(olddata.loc[i, "Bounds TIN 7"])

for j in range(len(ranges)):# given a range of input variables for one run of an algorithm (BASELINE or ENRICH), we generate 10 scenarios and modify
                            # (incremenet/decremenet) them.
    res = pd.DataFrame(columns=['TIN 0 Req-BW', 'TIN 1 Req-BW', 'TIN 2 Req-BW', 'TIN 3 Req-BW', 'TIN 4 Req-BW', 'TIN 5 Req-BW',
                                    'TIN 6 Req-BW', 'TIN 7 Req-BW', 'newfitness', 'TIN 0 Latency', 'TIN 1 Latency', 'TIN 2 Latency',
                                    'TIN 3 Latency', 'TIN 4 Latency', 'TIN 5 Latency', 'TIN 6 Latency', 'TIN 7 Latency',
                                    'TIN 0 MOS', 'TIN 1 MOS', 'TIN 2 MOS', 'TIN 3 MOS', 'TIN 4 MOS', 'TIN 5 MOS',
                                    'TIN 6 MOS', 'TIN 7 MOS', 'TIN 0 Thresh', 'TIN 1 Thresh', 'TIN 2 Thresh',
                                    'TIN 3 Thresh', 'TIN 4 Thresh', 'TIN 5 Thresh', 'TIN 6 Thresh', 'TIN 7 Thresh'])
    while len(res) < 60:
        for k in range(len(newarray)):
            if len(ranges[j][k]) > 1:
                a = random.randint(0,1)
                if a == 0:
                    newarray[k] = random.randint(ranges[j][k][0][0],ranges[j][k][0][1])
                else:
                    newarray[k] = random.randint(ranges[j][k][1][0],ranges[j][k][1][1])
            elif len(ranges[j][k]) == 1:
                newarray[k] = random.randint(ranges[j][k][0][0],ranges[j][k][0][1])
            else:
                newarray[k] = random.randint(0,thresh[k])

        DeleteRandomTrafficFiles()
        GenerateTraffic(newarray, i)
        time.sleep(10)
        RunDpinger()
        time.sleep(41)
        KillDpinger()
        time.sleep(90)
        alldpinger = ReadDpinger()
        alldpinger.reverse()
        if CheckDpinger(alldpinger) == False:
            alldpinger = Preprocess(alldpinger)
            f , flag = CalculateRobustnessMeasure(alldpinger)
            if flag == False:
                res, flag = AddToDataFrame(res,newarray,alldpinger, f)

                if f < 3.6:
                    res = decrement(newarray, res)
                else:
                    res = increment(newarray, res)

                i = i + 1

    WriteToExcel(res, "scenarios of run" + str(j))
