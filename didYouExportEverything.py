#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 20:06:21 2022

@author: latente
"""

# Python program to check if two
# to get unique values from list
# using traversal
from glob import glob

def missing(aiNames, fileNames):
    missing = []
    for n in aiNames:
        if n in fileNames: continue
        else: missing.append(n)
    return missing
    
ext = '../cell counting/ai files/*.ai'
aiNames = [f[26:-3].replace('.','') for f in glob(ext)]

ext = '../cell counting/cells/*.svg'
svgNames = [f[23:-4] for f in glob(ext)]

ext = '../cell counting/brainregions/*.png'
pngNames = [f[30:-4] for f in glob(ext)]

regionNames = [f.split('_')[-1] for f in pngNames]
filesWUnamedRegions = [f for f in pngNames if f.split('_')[-1]=='']

missingPNGNames = missing(aiNames, ['_'.join(f.split('_')[0:-1]) for f in pngNames])
missingSVGNames = missing(aiNames, ['_'.join(f.split('_')[0:-2]) for f in svgNames])

missingPNGonly = missing(missingPNGNames,missingSVGNames)
missingSVGonly = missing(missingSVGNames,missingPNGNames)

print('\nMissing PNG')
for n in sorted(missingPNGNames): print(n)
print('\nMissing SVG')
for n in sorted(missingSVGNames): print(n)
print('\nMissing Region Names')
for n in sorted(filesWUnamedRegions): print(n)


