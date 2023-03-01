import os
import pathlib
import pickle
import cv2

import imagej
import skimage
import numpy as np
from IPython.utils.io import capture_output

import warnings
import PyBaSiC.pybasic as pybasic

from preprocessor import BasicpyPreprocessor


fiji_path = pathlib.Path("/home/keenanmanpearl/Desktop/mitocheck/fiji-linux64/Fiji.app")
image_path = pathlib.Path("/home/keenanmanpearl/Desktop/mitocheck_movies/movies/LT0001_02/1.ch5/00001_01.ch5")
save_path = "/home/keenanmanpearl/Desktop/mitocheck_movies/corrected_movies/LT0001_02/1.avi"


fiji = BasicpyPreprocessor(fiji_path)
movie = fiji.load_mitocheck_movie_data(image_path)
corrected_movie = fiji.pybasic_illumination_correction(movie)
# only use first 10 frames
frames = 10
down_factor = 20
# height = 1024
height = len(corrected_movie[0])
# width = 1344
width = len(corrected_movie[0][0])

down_height = int(height/down_factor)
down_width = int(width/down_factor)
down_points = (down_width, down_height)

fourcc = cv2.VideoWriter_fourcc(*'jpeg')
fps = 4
out = cv2.VideoWriter(save_path, fourcc, fps, down_points, False)
for frame in range(frames):
    corrected_image = corrected_movie[frame]
    resized_image = cv2.resize(corrected_image, down_points)
    out.write(resized_image)
out.release()


# uncomment to save pickle file
# output = open('LT0001_02_00002_01.pkl', 'wb')
# pickle.dump(corrected_movie, output)
# output.close()