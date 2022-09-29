# Below is the code for applying Mann-Whitney U test

# author: Baharin A. Jodat
# Last Update: 2022 - 09 - 29

from scipy.stats import mannwhitneyu
import pandas as pd

sohosim = pd.read_excel('sohosim.xlsx')
sohohw = pd.read_excel('sohohw.xlsx')


U1, pvalue  = mannwhitneyu(sohosim,sohohw)

print(pvalue)
