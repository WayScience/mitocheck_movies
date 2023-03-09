#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pathlib
import cv2
import imagej
import skimage
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from IPython.utils.io import capture_output
import warnings
from PIL import Image

sys.path.append(os.path.abspath("../"))
import PyBaSiC.pybasic
from processor import BasicpyPreprocessor


# In[2]:


base_dir = pathlib.Path("/home/keenanmanpearl/Desktop")
fiji_path = pathlib.Path(f"{base_dir}/mitocheck/fiji-linux64/Fiji.app")
movie_path = pathlib.Path(
    f"{base_dir}/mitocheck_movies/movies/LT0001_02/1.ch5/00001_01.ch5"
)
fiji = BasicpyPreprocessor(fiji_path)
movie = fiji.load_mitocheck_movie_data(movie_path)
corrected_movie = fiji.pybasic_illumination_correction(movie)


# In[3]:


def process_movie(
    down_factor, height, width, save_path, fourcc, fps, frames, corrected_movie
):
    down_height = int(height / down_factor)
    down_width = int(width / down_factor)
    down_points = (down_width, down_height)
    # False for black and white
    out = cv2.VideoWriter(f"{save_path}", fourcc, fps, down_points, False)
    corrected_array = []
    for frame in range(frames):
        corrected_image = corrected_movie[frame]
        # compress each frame
        resized_image = cv2.resize(corrected_image, down_points)
        out.write(resized_image)
        corrected_array.append(resized_image)
    corrected_array = np.asarray(corrected_array)
    out.release()
    return corrected_array


# In[4]:


# height = 1024
height = len(corrected_movie[0])
# width = 1344
width = len(corrected_movie[0][0])
# dimensions for compressed images
# save corrected movie with the same name as original movie but updated extension
save_path = movie_path.with_suffix(".avi")
# compression type to write movie
fourcc = cv2.VideoWriter_fourcc(*"jpeg")
# frames per second
fps = 4
frames = 10

save_path = pathlib.Path(
    f"{base_dir}/mitocheck_movies/movies/LT0001_02/1.ch5/00001_01_compression2.avi"
)
compressed2 = process_movie(
    down_factor = 2, 
    height = height, 
    width = width, 
    save_path = save_path, 
    fourcc = fourcc, 
    fps = fps, 
    frames = frames, 
    corrected_movie = corrected_movie
)

save_path = pathlib.Path(
   f"{base_dir}/mitocheck_movies/movies/LT0001_01/2.ch5/00001_01_compression5.avi"
)
compressed5 = process_movie(
    down_factor = 5, 
    height = height, 
    width = width, 
    save_path = save_path, 
    fourcc = fourcc, 
    fps = fps, 
    frames = frames, 
    corrected_movie = corrected_movie
)

save_path = pathlib.Path(
    f"{base_dir}/mitocheck_movies/movies/LT0001_02/1.ch5/00001_01_compression10.avi"
)

compressed10 = process_movie( 
    down_factor = 10, 
    height = height, 
    width = width, 
    save_path = save_path, 
    fourcc = fourcc, 
    fps = fps, 
    frames = frames, 
    corrected_movie = corrected_movie
)

save_path = pathlib.Path(
   
   f"{base_dir}/Desktop/mitocheck_movies/movies/LT0001_02/1.ch5/00001_01_compression20.avi"
)

compressed20 = process_movie(
    down_factor = 20, 
    height = height, 
    width = width, 
    save_path = save_path, 
    fourcc = fourcc, 
    fps = fps, 
    frames = frames, 
    corrected_movie = corrected_movie
)


# 

# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
uncorrected = plt.imshow(movie[1, :, :])


# In[6]:


get_ipython().run_line_magic('matplotlib', 'inline')
compressed2_image = compressed2[1, :, :]
im2 = plt.imshow(compressed2_image)


# In[7]:


get_ipython().run_line_magic('matplotlib', 'inline')
compressed5_image = compressed5[1, :, :]
im2 = plt.imshow(compressed5_image)


# In[8]:


get_ipython().run_line_magic('matplotlib', 'inline')
compressed10_image = compressed10[1, :, :]
im10 = plt.imshow(compressed10_image)


# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')
compressed20_image = compressed20[1, :, :]
im20 = plt.imshow(compressed20_image)

