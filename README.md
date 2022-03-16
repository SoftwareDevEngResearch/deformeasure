[![Build Status](https://app.travis-ci.com/SatyamBhawsinghka/deformeasure.svg?branch=main)](https://app.travis-ci.com/SatyamBhawsinghka/deformeasure)


# deformeasure

## About
This is a software package to measure deformation from images or frames from videos using Digital Image Correlation(DIC). 
Another capability is to create deformed images and videos using cairo. 
The package provides a command line interface which demonstrates the capabilities of measuring deformation from either images or videos and creating visualisations and storing the output in a csv file.

## Installation
The deformeasure package relies on the following packages:
- Pillow 
- numpy
- pycairo
- imageio
- matplotlib 
- scipy 
- pytest(**optional**)

To use the CLI provided with the package
  - Clone from GitHub:
  
  `$ git clone https://github.com/SoftwareDevEngResearch/deformeasure`
  - Install the required version of dependencies:
  
  `$ pip install -r requirements.txt`
  
  - To install the package locally,
  
  `$ pip install /<PathToPackage>/deformeasure`
  
OR


Install the package directly from GitHub via pip:
 
 `$ python -m pip install git+https://github.com/SoftwareDevEngResearch/deformeasure`


### Creating Deformation

To use the capability of creating deformed images or videos, run the creatng_deformation.py script in Functions directory:

- Run with default values:

`$ python3 /<PathToPackage>/deformeasure/Functions/creating_deformation.py`

- To get help with input parameters:

`$ python3 /<PathToPackage>/deformeasure/Functions/creating_deformation.py --help`

Details of the functions can be accessed [here](deformeasure/docs/build/html/index.html#)








