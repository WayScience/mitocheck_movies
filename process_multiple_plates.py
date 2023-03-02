import pathlib
import cv2
import imagej
import skimage
import numpy as np
import warnings
import PyBaSiC.pybasic as pybasic
from IPython.utils.io import capture_output
from preprocessor import BasicpyPreprocessor


fiji_path = pathlib.Path("/home/keenanmanpearl/Desktop/mitocheck/fiji-linux64/Fiji.app")
movie_dir = pathlib.Path("/home/keenanmanpearl/Desktop/mitocheck_movies/movies/")
fiji = BasicpyPreprocessor(fiji_path)
# change to desired number of frames per movie
frames = 10

for plate_dir in movie_dir.iterdir():
    for well_dir in plate_dir.iterdir():
        for movie_path in well_dir.iterdir():
            movie = fiji.load_mitocheck_movie_data(movie_path)
            corrected_movie = fiji.pybasic_illumination_correction(movie)
            # change to control image compression
            down_factor = 20
            # frames = len(corrected_movie)
            # height = 1024
            height = len(corrected_movie[0])
            # width = 1344
            width = len(corrected_movie[0][0])
            # dimensions for compressed images
            down_height = int(height / down_factor)
            down_width = int(width / down_factor)
            down_points = (down_width, down_height)

            # save corrected movie with the same name as original movie but updated extension
            save_path = movie_path.with_suffix(".avi")
            # compression type to write movie
            fourcc = cv2.VideoWriter_fourcc(*"jpeg")
            # frames per second
            fps = 4
            # False for black and white
            out = cv2.VideoWriter(f"{save_path}", fourcc, fps, down_points, False)
            for frame in range(frames):
                corrected_image = corrected_movie[frame]
                # compress each frame
                resized_image = cv2.resize(corrected_image, down_points)
                out.write(resized_image)
            out.release()
