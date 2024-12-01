# Extract Data from Paper (EDP)

## Overview

A tool designed to extract numerical data from scanned historical weather documents, specifically from the UK Met Office Observatories Year Book archive. It converts PDF tables into CSV and JSON formats using computer vision and OCR techniques.

> **Note:** This project was created in 2019 as an experimental effort. Modern OCR solutions and AI models may provide better results.

## Motivations

- Automate extraction of numerical data from scanned documents
- Be 60x faster than manual data entry
- Hit more than 98% accuracy on well-formatted documents
- Specialized for weather and climate data
- Support daily and monthly data formats

## System Requirements

- Python 3.5+
- Tesseract OCR 4.1.0
- Legacy trained data

## Quick Start

1. Install Tesseract OCR:

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr
```

2. Install Legacy Training Data:

```bash
# Download
curl -L -o eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# Install (choose based on your OS)
# macOS:
sudo mv eng.traineddata /opt/homebrew/share/tessdata/
# Ubuntu/Debian:
sudo mv eng.traineddata /usr/share/tessdata/
```

3. Install Python Dependencies:

```bash
python setup.py install
# OR
python setup.py install --user
```

4. Run the Program:

```bash
cd src/
python main.py
# or
jupyter notebook notebook.ipynb
```

<<<<<<< HEAD
You also have a few optional args you can use:

- `-ro`: Clear output directory
- # `-i`: Specify path to input

## Command Line Options

- `-ro`: Clear output directory
  > > > > > > > d0ed394849e04b27d8b50376f5e1de61dc3d4b35
- `-verbose`: Enable detailed logging

## Processing Pipeline

The project leverages the following OCR and image processing tech:

- Engine: Tesseract OCR 4.1.0 (July 2019) (Legacy mode)
- Page Segmentation Mode: 6
- Language: English
- OpenCV for image processing
- Python libraries: NumPy, Pandas, scikit-image

The system implements a multi-stage pipeline using Tesseract OCR, OpenCV, and Python data processing libraries:

1. **Input Processing**

   - Handles command line options (`-ro` to clear output, `-verbose` for detailed logs)
   - Validates input files and paths

2. **Document Selection**

   - Evaluates document quality using line detection
   - Filters out pages with insufficient data quality
   - Ensures only processable documents continue through pipeline

3. **Image Enhancement**

   - Cleans and improves image quality
   - Reduces noise, removes shadow and smear
   - Enhances text visibility
   - Prepares images for OCR processing (see /output folder)

4. **Block Detection**

   - Identifies and extracts distinct data blocks from each page
   - Creates separate image files for each block
   - Maintains document structure information

5. **Text Extraction**

   - Performs OCR on blocks or individual lines (Binarization for background-text contrast, skew angle correction, morphological operations for region segmentation)
   - Processes extracted text to correct common OCR errors
   - Preserves metadata (year, page, block numbers)

6. **Data Export**
   - Generates structured CSV output (see output.csv)
   - Includes extracted text and document metadata
   - Organizes data by year, page, and block

The pipeline is specifically optimized for the UK Met Office Observatories Year Book archive and requires Tesseract OCR installation.

![pre-processing](./docs/png/preprocessing-chain-lr.png)

## Technical Limitations

- Manual parameter tuning required:
  - Threshold values
  - Kernel sizes for morphological operations
  - Binarization settings
- Optimized for Observatories Year Book format
- Limited effectiveness on lower quality documents
  - Otsu binarization works well for high-quality scans
  - Alternative techniques needed for degraded documents

## Dataset

The project focuses on the UK Met Office Observatories Year Book (1922-1967) _[Observatories Year Book](https://digital.nmla.metoffice.gov.uk/SO_5575296f-0406-49f5-89cb-54cd79486b75/)_ which includes:

- Data from 5 locations
- Up to 30 weather variables
- Daily, monthly, and annual measurements

## Performance

Based on benchmarks against other OCR solutions:

- Legacy Tesseract shows superior results for this specific dataset
- Good page segmentation and layout preservation
- Some character recognition issues require post-processing
  The benchmark was run against several OCR systems:

- Amazon Textract ([output](./docs/txt/amazon-textract.txt))

  `It was almost impossible to retrieve the internal layout structure`

- Microsoft Azure Cognitive Service ([output](./docs/txt/microsoft-azure.txt))

  ```
  IOOI .31 +0.24 +0.21 +0.05 -0.16 -
  -0.22 -0.27
  -0.23 -0.05 +0.06 +0.24 +0.26 +0.12 +0.02 -0.16 -0.27 -0.31 -0.15 -0 02 +0.02 +0.08 +0.07 +0-05 +0.13 + 0.29
  1007.62 +0.23 +0.09 -0.09-0.30-0.38 -0-40-
  -0.33 -0.19 -0.1I -0.01 +0.02 +0-03 -0.05 -
  -0.28 -0.21 +0.05 +0'27 +0.38 +0-43 +0-47 +0.42 +0.38
  ```

- Google Vision OCR ([output](./docs/txt/google-vision.txt))

  ```
  1003'56 +o:38 +o27 tol —о07 —о:22 \~о-37 —о:33 —о18 —о-10 — о-II —о-10 —о-27 -о47 -0-59 —о-55 -о:38.
  10O1 31 +o:24 +o21 to05 —о-16 —о-22 -\~о-27 —о-23 \~о05 +o-об +o-24 +oо-26 +o-12 +о02 —о-16 —о-27 —0-31 —о-15 —о02 +o-02 +o-o8 +oo7 toos to13 +0:29
  I007 62 +o 23 +o.o9-0-09 -o-30 -o-38 -0-40 -o-33 -o-19-o-11 -o oi +o-02 +o*03 -o-05 -o-18 -o-25 -o-28 -o-21 +O 05 +o 27 +o 38 +o 43 +0-47 +o'42 +o-38
  -o 22 +o 02 +o-27 +0'43 +o-57 +o-62 +0-65 +o-62
  ```

- Tesseract with LTSM (`--oem 1 --psm 6`)([output](./docs/txt/tesseract_OEM1.txt))

  ```
  "AES: H 1003-56 40°38 +027 +0°11 —0-07 —0-22 —0-37 —0-33 —0-I8 —0-I0 —0‘II —0°'I0 —0+27 —0°47 —0-69 —0-55 —0:38 —0-22 +0-02 +027 +043 +0-57 + 0-62 +0-685 +0-62",
  "pCR 100131 40:24 +0°2X 40°05 —0'I6 —0'22 -\~0-27 —0*23 —0'05 +0°06 +0-24 +026 40-12 40:02 —0°16 —0-27 —0-31 —0'15 —0'02 + 0'02 +0-08 40-07 40-05 +0-13 + 0-29",
  "Mar. 100762 +023 +009 —0:09 —0-30 —0-38 —0-40 —0°33 —0'19 —0-11 —0-0I +06+02 40:03 —0-05 —0-18 —0-25 —0-28 —0-21 40-05 + 0°27 40°38 +043 + 0-47 + 0°42 +0-38"
  ```

- Tesseract with Legacy (`--oem 0 --psm 6`)([output](./docs/txt/tesseract_OEM0.txt)) :

  ```
  'Jan. 1003-56 +0-38 +0-27 +o-11 —-o-o7 —o-22 —0-37 —o\~33 —o-18 —o-10 —0-n —o-10 —0-27 —o-47 —0-59 —0-55 —o-38 —0-22 +o-02 +o-z7 +o-43 +o-57 +o\~62 +005 +o-62',
  "Feb. 1001-31 +o-24 +o-2x +0-05 —0-16 —0-22 »—o-27 —o-23 ——0-o5 +0-o6 +0-24 +0-26 +o-1z +0-oz —0-16 —o-27 —0-31 —0-15 —0-02 +o-oz +o-08 +0'07 +0'05 +013 +029",
  "Mar. 1007-62 +o-23 +o-09 —0-09 —o-3o —0-38 —0-40 —o-33 —o-19 —o-11 —o-01 +0-oz +o-o3 —o-o5 —0-18 —o-z5 ——0-28 —o-21 +0-05 +0-z7 +0-38 +0'43 +047 +o-42 +o\~38"
  ```

## Background

Historical weather records are crucial for:

- Understanding climate variability
- Developing accurate prediction systems
- Preserving historical data

Back in 2019 I couldn't find any efficient solution to accurately extract data from weather books, which [Ed Hawkins](<https://en.wikipedia.org/wiki/Ed_Hawkins_(scientist)>) also pointed out:

![tweet by ed hawkins](./docs/png/tweet-ed-500px.png)

Traditional manual digitization process was:

- Time-consuming: It took the [Operation Weather Rescue initiative](https://www.zooniverse.org/projects/edh/weather-rescue) 180 days and 3,300 volunteers to digitize 1,300,000 observations ([source](https://www.zooniverse.org/projects/edh/weather-rescue/stats/?classification=month&comment=month)).
- Labor-intensive
- Prone to human error
