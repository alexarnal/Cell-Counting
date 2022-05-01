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

With an Adobe Illustrator file open, select File > Scripts > Other Script... and select `Cell Export.js`. The program will iterate through all first-order layers looking for the cell layer names specified in `projectDetails.csv`. Once a match is found, it will isolate the layer and save it as an SVG file to the folder `cells/`.  

In the same Adobe Illustrator file, unlock and select the layer named *brainregions*. Then select File > Scripts > Other Script... and select `Region Export.js`. This will isolate the layer, and iterate through the individual shapes in the layer. For each shape, the program will set the fill to black and stroke to none and export it as a PNG file to the folder `brainregions/`. 

Repeat for all Illustrator files.

### Verify Exporting Process

To make sure all files have been exported, navigate to `scripts/` in the terminal and run `didYourExportEverything.py`.

```
cd scripts
python didYouExportEverything.py
```

This program will compare the Illustrator file names and the exported file names. It will then print out the file names that did not get exported for both SVG (cells) and PNG (brain regions) files. It will also print out if there were any brain regions without a name. Using this as a guide, return to the Adobe Illustrator files, correct any issues, and export again. Most of the time this involves correcting any mispelings of the Illustrator layers or missing brain region names (i.e. `<Path>` versus `nts-l`).
  
### Count Cells
  
Finally, navigate to `scripts/` in the terminal and run `cellCounts.py`.
  
```
cd scripts (if not already in scripts/)
python cellCounts.py
```

This program will obtain the Illustrator file names and use the list of names to search for files in the *cells/* and *brainregions/* folders. For each Illustrator file name, the program will load the corresponding SVG and PNG files and create a list of cell centroids from the SVG and a list of masks (2D arrays) for each of the brain regions in that Illustrator file. It will then bin the coordinates to a 2D array with equal height and width as the brain region masks so that we have a new 2D array where each pixel serves as a counter of cells that are binned to it. Then, the program will iterate through the brain region arrays, mask the new counter grid, and sum the pixel values in the masked counter grid. The sum is then recorded on a table as the number of cells in that brain region. At the same time, the number of pixels that make up the brain region is obtained and converted to a metric equivalent value and recorded on a separate table. This is repeated for all brain regions per Illustrator file name. The output is two tables saved in *tables/*. 


Note: The conversion of pixels to millimeters is possible by finding the length of pixels that make up the scale bar in one of the images. Since all images share the same resolution and scale, we can use this value to convert all pixel counts to areas. Specifically, based on the scale bar, 100 µm = 116 pixel lengths and 100 µm = 0.1 mm. Thus, every pixel has an area of `$(\frac{0.01}{116})^2$` mm^2.
  
