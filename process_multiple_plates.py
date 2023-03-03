__author__ = "Keenan Manpearl"
__date__ = "2023/03/02"

"""
illumination correction, image compression and shortening of a batch of mitocheck movie
"""

import pathlib
import cv2
import imagej
import skimage
import numpy as np
import warnings
import PyBaSiC.pybasic as pybasic
from IPython.utils.io import capture_output
from processor import BasicpyPreprocessor, process_movies


fiji_path = pathlib.Path("/home/keenanmanpearl/Desktop/mitocheck/fiji-linux64/Fiji.app")
movie_dir = pathlib.Path("/home/keenanmanpearl/Desktop/mitocheck_movies/movies/")
# change to desired number of frames per movie
n_frames = 10
# change to control image compression
down_factor = 20

process_movies(fiji_path, movie_dir, n_frames, down_factor)

