"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject

Installs packages using distutils

Run:
    python setup.py install

to install this package.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
import sys
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
# from io import open

here = path.abspath(path.dirname(__file__))


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='extract-data-from-paper',  # Changed: Use hyphenated name for PyPI compatibility
    version='0.1',
    description='Extract information from old weather books containing typed and handwritten values into CSV format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/floriancochard/extract-data-from-paper',
    keywords='extract data paper digitize historical weather records ocr pdf table csv',
    license='AGPL-3.0',  # Changed: Use SPDX identifier
    author='Florian Cochard',
    
    # Changed: Uncomment packages and specify correctly
    packages=find_packages(where='src'),  # Assuming code is in src directory
    package_dir={'': 'src'},
    
    # Changed: Update Python version requirements
    python_requires='>=3.5',  # Removed Python 2.7 support since it's not tested
    
    # Changed: Organize dependencies
    install_requires=[
        'opencv-python>=4.0.0',
        'numpy>=1.16.0',
        'pandas>=1.0.0',
        'pytesseract>=0.3.0',
        'matplotlib>=3.0.0',
        'scikit-image>=0.15.0',
        'scikit-learn>=0.22.0',
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',  # Added: More specific audience
        'Topic :: Scientific/Engineering :: Image Recognition',  # Added: More specific topic
        'License :: OSI Approved :: GNU Affero General Public License v3',  # Fixed: Correct license classifier
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    
    # Changed: Add entry point for CLI
    entry_points={
        'console_scripts': [
            'extract-data=src.main:main',
        ],
    },
    
    project_urls={
        'Bug Reports': 'https://github.com/floriancochard/extract-data-from-paper/issues',
        'Source': 'https://github.com/floriancochard/extract-data-from-paper/',
    },
)
