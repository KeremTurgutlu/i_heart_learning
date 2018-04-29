## Welcome to I :heart: Learning Repo !

#### This is an end-to-end pipeline for getting DICOM data ready for :heart: segmentation.

`solution`: Main package including modules that are used in the pipeline.

`parsing.py`: The original solution for starting. Has useful functions for parsing DICOM images and manually created contours into numpy array.

`final_data`: Under this directory you will find images directory which has **i_contour** and **o_contour** images under every patients own directory. As well as **roi_intensities** folder which shows ROI pixel density distributions for each patient/study.

`notebooks`: This folder consists two notebooks per part. 

  Notebook **development** is used to develop, debug and design part 1. The other notebook, **solution-manual** shows how to use `solution` package to create Dataloaders just in few lines of code for part 1. 
  
  For part 2, similarly  **analysis_development-part2** is used to iterate, develop ideas and experiment. In this notebook, you may see how I thought through the problem. In **solution-manual2** I am calling all the functions needed from package `solution`, it shows **o-contour** parsing and continue with LV segmentation.

`report.pdf`: This is the report for thought experiment which includes plots and analysis.

