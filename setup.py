#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='deformeasure',
    version='1.0.0',
    description='Measuring deformation from images and videos and creating deformed images and videos',
    author='Satyam Bhawsinghka',
    author_email='satyamdgr87@gmail.com',
    url='https://github.com/SoftwareDevEngResearch/deformeasure',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    python_requires='==3.7',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow>=9.0.1',
        'numpy>=1.21.5',
        'pycairo==1.19.1',
        'imageio>=2.16.1',
        'matplotlib>=3.5.1',
        'scipy==1.7.3'
            ],
    tests_require=['pytest']
)
