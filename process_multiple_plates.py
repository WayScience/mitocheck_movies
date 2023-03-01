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
movie_dir = pathlib.Path("/home/keenanmanpearl/Desktop/mitocheck_movies/movies/")
fiji = BasicpyPreprocessor(fiji_path)
frames = 10

for plate_dir in movie_dir.iterdir():
    for well_dir in plate_dir.iterdir():
        for movie_path in well_dir.iterdir():
            print(movie_path)
            save_path = movie_path.with_suffix(".avi")
            movie = fiji.load_mitocheck_movie_data(movie_path)
            corrected_movie = fiji.pybasic_illumination_correction(movie)
            frames = 10
            #frames = len(corrected_movie)
            # height = 1024
            height = len(corrected_movie[0])
            # width = 1344
            width = len(corrected_movie[0][0])
            down_height = int(height/20)
            down_width = int(width/20)
            down_points = (down_width, down_height)

            fourcc = cv2.VideoWriter_fourcc(*'jpeg')
            fps = 4
            out = cv2.VideoWriter(f"{save_path}", fourcc, fps, down_points, False)
            for frame in range(frames):
                corrected_image = corrected_movie[frame]
                resized_image = cv2.resize(corrected_image, down_points)
                out.write(resized_image)
            out.release()


# uncomment to save pickle file
# output = open('LT0001_02_00002_01.pkl', 'wb')
# pickle.dump(corrected_movie, output)
# output.close()
