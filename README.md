# Overview

Smithsonian has an open access collection consisting of various dataset from museums, archives, etc.
The collection stores both metadata and images from each dataset.
The scripts in this repo scan a dataset for CC0 images (based on the metadata) and downloads those images.
There are also scripts for listing image resolutions, resizing images, and creating ready-to-go Pytorch-ingestible datasets with train/val splits.

# Requirements

## Programs
`python`: for scanning license info in metadata
`aria2`: for downloading images
`parallel`: for resizing images
`libvips-tools`: for resizing images

## Python packages
`pillow`: Image resolution info & splitting dataset

# Files

`download-metadata.sh`: Retrieve jsonl files containing individual image license info
`manifest_cc0.py`: Scan jsonl metadata files for CC0 image licenses
`download-images.sh`: Retrieve CC0 images
`scan_resolutions.py`: List resolutions of images in a dir
`resize.sh`: Resize images (preserves aspect ratio)
`make_split.py`: Creates train/test split directories (with soft links)

# Steps

```
1. bash download-metadata.sh nasm
2. python manifest_cc0.py metadata/edan/nasm/ > metadata/nasm.tsv
3. bash download-images.sh nasm
4. (optional) python scan_resolutions.py images/nasm
5. (edit resize.sh) bash resize.sh
6. python make_split.py images/nasm_512 /work/dataset
```
