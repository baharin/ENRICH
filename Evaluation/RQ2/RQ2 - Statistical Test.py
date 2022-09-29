# Below is the code for applying Mann-Whitney U test

# author: Baharin A. Jodat
# Last Update: 2022 - 09 - 29

from scipy.stats import mannwhitneyu
import pandas as pd

data = pd.read_excel('SOHOSim VS SOHOHW.xlsx', header = 0)

sohosim = []
sohohw = []

for i in range(len(data.index)):
  sohosim.append(data.loc[i, 'SOHOSIM Robustness Measure'])
  sohohw.append(data.loc[i, 'SOHOHW Robustness Measure'])


U1, pvalue  = mannwhitneyu(sohosim,sohohw)

print(pvalue)
