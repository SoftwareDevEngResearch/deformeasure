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

 `$ cd /<PathToPackage>/deformeasure/Functions/`

 `$ python3 creating_deformation.py`

- To get help with input parameters:

 `$ cd /<PathToPackage>/deformeasure/Functions/`

 `$ python3 creating_deformation.py --help`

The transfromation matrix used to create deformed images:

a1 | c3 | e5
--- | --- | ---
**b2** | **d4** | **f6**
**0** | **0** | **1** 

Parameter description:

parameter | type | description
--- | --- | ---
image_size | int  | Size of the generated reference and deformed images and videos
seed | int | Seed value for random generator
a1 | float | Scale in x direction
b2 | float | Shear in y direction
c3 | float | Shear in x direction
d4 | float | Scale in y direction
e5 | float | Translation in x direction
f6 | float | Translation in y direction
filename | string | name of the file with which the results will be stored in generated directory
mode | string | Option to generate deformed image or video

Details of the functions can be accessed at `/<PathtoPackage>/deformeasure/docs/build/html/index.html`

#### Example
Creating a video of deformation with 10% translation in x: 

`$ cd /<PathToPackage>/deformeasure/Functions/`

`$ python3 creating_deformation.py 50 19 1.0 0.1 0.0 1.0 0.0 0.0 example video`

will create three files in /deformeasure/generated/video/def/
- *def_example.gif* (the deformation video)
- *def_example_x.csv* (deformations in pixels in x)
- *def_example_y.csv* (deformations in pixels in y)

and a refrence image in /deformeasure/generated/video/ref/ *ref_example.bmp*

### Measuring Deformation

To measure deformation from images or videos, run the measuring_deformation.py script in Functions directory. This provides a CLI to use classes in Lib directory. To get help with the parameters:

 `$ cd /<PathToPackage>/deformeasure/Functions/`

 `$ python3 measuring_deformation.py --help`
 
The details of the parameters in CLI are:


parameter | type | description
--- | --- | ---
ref_image | string | location of the reference image
def_image | string | location of the deformed image
def_video | string | location of the deformation video
subset_size | int | Size of the subset(*default=11*)
initial_guess | list | Initial guess for deformations(*default=[0.0,0.0]*)
debug | bool | Use debug printing mode
output | string | name of the output csv file
visualize | bool | Option to visualize the deformations


#### Example
Measuring deformation from an image:

`$ cd /<PathToPackage>/deformeasure/Functions/`

`$ python3 measuring_deformation.py -ri ../generated/image/ref/ref_translation_x.bmp -di ../generated/image/def/def_translation_x.bmp -v`

Measuring deformation from a video:

`$ cd /<PathToPackage>/deformeasure/Functions/`

`$ python3 measuring_deformation.py -ri ../generated/video/ref/ref_translation_x.bmp -di ../generated/video/def/def_translation_x.gif -v`

### Testing

Once inside deformeasure, it can be tested by running pytest.

`$ pytest`

## License

[MIT](https://github.com/SoftwareDevEngResearch/deformeasure/blob/main/LICENSE)

### Reference

The source code used in measuring deformation were extended from [PReDIC](https://github.com/texm/PReDIC) Github repository.

 
 















