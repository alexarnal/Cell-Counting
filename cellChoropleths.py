#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 18:46:02 2021

@author: latente
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import re
from glob import glob
from os import listdir
from os.path import isfile, join
from natsort import natsorted

def getCoordsFromSVG(fileName):
    file = open(fileName,'r')
    fileContent = file.readline()
    file.close()
    fileContent = fileContent.split('>')
    X=[]
    Y=[]
    viewBox = 0
    for i,line in enumerate(fileContent): 
        coord = 0

        if 'viewBox=' in line:
            viewBox = re.search('viewBox="(.*)"', line)
            
        if 'circle' in line:
            x = re.search('cx="(.*)" cy', line)
            y = re.search('cy="(.*)" r', line)
            coord = [x.group(1),y.group(1)] 
        elif 'ellipse' in line:
            x = re.search('cx="(.*)" cy', line)
            y = re.search('cy="(.*)" rx', line)
            coord = [x.group(1),y.group(1)]
        else: continue
        X.append(float(coord[0]))
        Y.append(-float(coord[1]))
    
    coords = np.vstack((np.array(X), np.array(Y))).T
    return coords, np.array(viewBox[1].split(' '), dtype='float')

def cellLocations(coordinates,viewBox, scaleFactor):
    #first remove duplicates
    coords = [tuple(row) for row in coordinates]
    coords = np.unique(coords,axis=0)
    canvas = np.zeros((int(viewBox[3]*scaleFactor),int(viewBox[2]*scaleFactor))).astype(np.float32)
    
    if len(coordinates)==0: return canvas
    x=-coords[:,1]
    y=coords[:,0]
    for i in range(len(x)):
        try:
            # print(int(x[i]),int(y[i]))
            canvas[int(x[i]*scaleFactor),int(y[i]*scaleFactor)] += 1
        except: 
            print('Cell out of frame - Skipping')
            continue
    return canvas

def choropleth(regionShapes, fibers, scale, normalized_by_region_area=False):
    vals = np.zeros(len(regionShapes))
    areas = np.zeros(len(regionShapes))
    mapa = np.zeros(regionShapes[0].shape[0:2])
    if normalized_by_region_area:
        for i in range(len(regionShapes)):
            vals[i] = np.sum(fibers[regionShapes[i]])/np.sum(regionShapes[i])
            areas[i] = np.sum(regionShapes[i])*scale
            mapa[regionShapes[i]] = vals[i]
    else:
        for i in range(len(regionShapes)):
            vals[i] = np.sum(fibers[regionShapes[i]])
            areas[i] = np.sum(regionShapes[i])*scale
            mapa[regionShapes[i]] = vals[i]
    return mapa, vals, areas

#write(outDir,level,case,marker,vals,areas,brainRegionNames,replicate, metric_scale):
def write(outDir,vals,brainRegionNames,metricScale,br_wordbank,l,i,information,n):
    outFileName=outDir+f'{information}.csv'
    if n == 0: 
        f = open(outFileName, "w")
        f.writelines(['fileName,peptide,',','.join(br_wordbank), '\n'])
    #else:
    newVals=[]
    for br in br_wordbank: 
        if br in brainRegionNames:
            newVals.append(vals[brainRegionNames.index(br)].astype('str'))
        else:
            newVals.append('-')
    f = open(outFileName, "a")
    line = [f'{i},{l},',','.join(newVals),'\n'] #vals.astype('str').tolist()), '\n']
    f.writelines(line)
    f.close()

def getRegions(id, regionType):
    directory = f'../cell counting/{regionType}/'
    names=os.listdir(directory)
    regionShapes = []
    regionSizes = []
    regionNames = []
    for name in names:
        if id not in name: continue
        try:
            x = plt.imread(directory+name)[:,:,0]<0.5
        except: continue
        regionShapes.append(x)
        regionSizes.append(np.sum(x))
        regionNames.append(name[len(id)+1:-4]) #remove id and .png
    indxs = np.argsort(np.array(regionSizes))
    sortedNames = []
    sortedShape = []
    for indx in indxs[::-1]:
        sortedNames.append(regionNames[indx])
        sortedShape.append(regionShapes[indx])
    return sortedShape, sortedNames 

def getProjectDetails(path):
    myDictionary = {}
    file = open(path,"r")
    for line in file:
        fields = [x.replace(' ','').replace('\n','') for x in line.split(",")]
        myDictionary[fields[0]]=fields[1:]
    file.close()
    print("\nProject Details:")
    for i in myDictionary:
        print("  ",i, myDictionary[i])
    return myDictionary

#Project's Experimental Set Up
projectDetails = getProjectDetails("projectDetails.csv")
cell_layers = projectDetails['cell_layers']
br_wordbank = [br.lower() for br in projectDetails['brainregions']]
scaleFactor = 1
metricScale = (0.1/116)**2 # based on scale bar, 100µm = 116pixels and 100µm = 0.1 mm

#Directory to Fiber Data Set Up
dataDir='../cell counting/cells/'
outDir ='../cell counting/tables/'

#Generate brain-region-wise count tables and choropleth maps for each SVG file
print('\nGenerating brain-region-wise count tables and choropleth maps for each SVG file.')
ids = natsorted([os.path.splitext(f)[0][:f.index('10x')+3] for f in listdir(dataDir) if isfile(join(dataDir, f)) and '.svg' in f])

n = 0
for iD in ids:  
    print(f'Analyzing {iD}')
    brainRegionShapes, brainRegionNames = getRegions(iD,"brainregionsfinal")
    for l in cell_layers:
        #for br in brainRegionNames:
        fileName = f'{dataDir}{iD}_{l}-01.svg'
        try:
            coordinates, viewBox = getCoordsFromSVG(fileName)
        except Exception as e: print(e); break
        cells = cellLocations(coordinates,viewBox,scaleFactor)
        mapa, vals, areas = choropleth(brainRegionShapes, cells, metricScale)
        write(outDir,vals,brainRegionNames,metricScale,br_wordbank,l,iD,'counts',n)
        write(outDir,areas,brainRegionNames,metricScale,br_wordbank,l,iD,'areas(mm)',n)
        n += 1
        print(f'Found a total of {len(coordinates)} {l} cells\n')
print('Finished generating brain-region-wise count tables and choropleth maps for %d SVG individual files.'%n) 
