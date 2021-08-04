# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 22:44:48 2021

@author: cosmi


@author: cosmi
Working Batch Processer for DNG to JPG
rawpy is an easy-to-use Python wrapper for the LibRaw library. 
rawpy works natively with numpy arrays and supports a lot of options, 
including direct access to the unprocessed Bayer data
It also contains some extra functionality for finding and repairing hot/dead pixels.
import rawpy.enhance for this
"""

import os
import rawpy
import imageio


import fnmatch
import numpy as np
from PIL import Image
from tqdm import trange

## Image Processing libraries for histogram equalisation
from skimage import exposure

#1st part of code - load and process DNG (RAW) files 

for infile in os.listdir("./"):
    print( "file : " + infile)
    if infile[-3:] == "tif" or infile[-3:] == "DNG" :
       # print "is tif or DNG (RAW)"
       outfile = infile[:-3] + "jpg"
       raw = rawpy.imread(infile)
       print( "new filename : " + outfile)
       

       # Postprocessing, i.e demosaicing here, will always 
       #change the original pixel values. Typically what you want
       # is to get a linearly postprocessed image so that roughly 
       #the number of photons are in linear relation to the pixel values. 
       #You can do that with:

       rgb = raw.postprocess()

       #Apply gamma corrections: gamma values greater than 1 will shift the image histogram towards left and the output image will be darker than the input image. On the other hand, for gamma values less than 1, the histogram will shift towards right and the output image will be brighter than the input image.
    

       gamma_corrected_image = exposure.adjust_gamma(rgb, gamma=1, gain=0.5)

       
       image=gamma_corrected_image
       
       #apply histogram equalization
       #using skimage (easy way)
       hist_equalized_image = exposure.equalize_hist(image)
    

       imageio.imsave(outfile, hist_equalized_image)
       
       
#2nd part of code - process the output jpgs in the directory (avg, sum or brighten)
       

images_in = "img"
brighness_divide = 5.0


def find(directory, pattern):
	file_list = []
	for root, dirs, files in os.walk(directory):
		for basename in files:
			if fnmatch.fnmatch(basename, pattern):
				filename = os.path.join(root, basename)
				file_list.append(filename)
	return file_list


# Find pictures in specified directory
files   = os.listdir(os.getcwd())

imlist  = [name for name in files if name[-4:] in [".jpg", ".JPG"]]


# take first picture as a refference
w, h = Image.open(imlist[0]).size

arr = np.zeros((h, w, 3), np.float)
for j in trange(len(imlist), desc='Frames'):
	imgin = Image.open(imlist[j])
	imarr = np.array(imgin, dtype=np.float)
	arr = arr + imarr / len(imlist)

arr = np.array(np.round(arr), dtype=np.uint8)
out = Image.fromarray(arr, mode="RGB")
out.save("avg_"+images_in+".jpg")
            