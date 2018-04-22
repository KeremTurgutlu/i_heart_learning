Welcome to I :heart: Learning Repo !

This is an end-to-end pipeline for getting DICOM data ready for :heart: segmentation.

`solution`: Main package including modules that are used in the pipeline.

`parsing.py`: The original solution for starting. Has useful functions for parsing DICOM images and manually created contours into numpy array.

`final_data`: Under this directory you will find images directory which has **i_contour** and **o_contour** images under every patients own directory.

`notebook`: This folder consists two notebooks that I've used. Notebook **development** is used to develop, debug and design. The other notebook, **solution-manual** shows how to use `solution` package to create Dataloaders just in few lines of code.

