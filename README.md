# Cell Counting

This repository contains the JavaScript files that run inside Adobe Illustrator to export the desired data with the correct file format and file name conventions. It also contains the Python programs to verify all data was exported as well as the program to count cell annotations that fall inside brain regions.

## Project Structure
```
Cell-Counting
│
└─── data
│   │
│   └─── ai_files
│       │   *.ai (example: slide3.2sec3_10x.ai)
│       │   ...
│   │
│   └─── cells
│       │   *_<cell layer>-01.svg (example: slide32sec3_10x_pERKcells_RV-01.svg)
│       │   ...
│   │
│   └─── brainregions
│       │   *_<region name>.png (example: slide32sec3_10x_nts-l.png)
│       │   ...
│   │
│   └─── tables
│       │   areas(mm).csv
│       │   counts.csv
│
└─── scripts
|   |   requirements.txt
|   |   projectDetails.csv
│   │   Cell Export.js
│   │   Region Export.js
│   │   didYouExportEverything.py
│   │   prepareBrainRegions.py
│   │   cellChoropleths.py
```

## Usage

### Project Details & File Structure

The CSV file that contains the project details should have a row for the brain region names and another for cell layers. These names should match the names in the Adobe Illustrator files for successful export. Also make sure to arrange/create folders according to the folder set up in *Project Structure*. 

### Exporting

In order to count cells using the Python script, we first need to export the necessary information from the Adobe Illustrator files. In this case, we need to export the cell annotations in SVG format and the brain regions in PNG format with the naming convention specified in *Project Structure*. 

With an Adobe Illustrator file open, select File > Scripts > Other Script... and select *Cell Export.js*. This will iterate through all first-order layers looking for the layer names specified in *projectDetails.csv*. Once a match is found, it will isolate the layer and save it as an SVG file to the folder *cells/*.  

In the same Adobe Illustrator file, unlock and select the layer named *brainregions*. Then select File > Scripts > Other Script... and select *Region Export.js*. This will isolate the layer, and iterate through the individual shapes in the layer. For each shape, the program will set the fill to black and stroke to none and export it as a PNG file to the folder *brainregions*. 

Repeat for all Illustrator files.

### Verify Exporting Process

To make sure all files have been exported, navigate to *scripts/* in the terminal and run *didYourExportEverything.py*.

```
cd scripts
python didYouExportEverything.py
```

This program will compare the Illustrator file names and the exported file names. It will then print out the file names that did not get exported for both SVG (cells) and PNG (brain regions) files. It will also print out if there were any brain regions without a name. Using this as a guide, return to the Adobe Illustrator files, correct any issues, and export again. Most of the time this involves correcting any mispelings of the Illustrator layers or missing brain region names (i.e. "<Path>" versus "nts-l").
  
### Count Cells
  
Finally, navigate to *scripts/* in the terminal and run *cellCounts.py*.
  
```
cd scripts
python cellCounts.py
```
  
