

# from importlib.resources import path
import os
import pathlib
import pickle

import imagej
import skimage
import numpy as np
from IPython.utils.io import capture_output

import warnings
import PyBaSiC.pybasic as pybasic

class BasicpyPreprocessor:
    """
    This class holds all functions needed to preprocess IDR-downloaded mitosis movies with PyBaSiC
    When preprocessing a mitosis movie, imagej is used to load the movie ]
    and convert it to a numpy array before illumination correction with PyBaSiC

    Attributes
    ----------
    ij : ImageJ gateway
        loaded pyimagej wrapper

    Methods
    -------
    load_mitocheck_movie_data(movie_load_path)
        get numpy array of movie data from .ch5 file
    pybasic_illumination_correction(brightfield_images)
        use pybasic to correct brighfield images
    """

    def __init__(self, fiji_path: pathlib.Path):
        """
        __init__ function for BasicpyPreprocessor class

        Parameters
        ----------
        fiji_path : pathlib.Path
            path to installed FIJI program, 
            ex pathlib.Path("/home/user/Fiji.app")
        """
        original_path = os.getcwd()
        self.ij = imagej.init(fiji_path)
        # imagej init sets directory to fiji_path so have to go back to original dir
        os.chdir(original_path)

    def load_mitocheck_movie_data(self, movie_load_path: pathlib.Path) -> np.ndarray:
        """
        get numpy array of movie data from .ch5 file

        Parameters
        ----------
        movie_load_path : pathlib.Path
            path to mitosis movie

        Returns
        -------
        np.ndarray
            array of movie data
        """
        # imagej prints lots of output that isnt necessary, unfortunately some will still come through
        with capture_output():
            jmovie = self.ij.io().open(str(movie_load_path.resolve()))
            movie = self.ij.py.from_java(jmovie)
            movie_arr = movie.values[:, :, :, 0]
            return movie_arr

    def pybasic_illumination_correction(self, brightfield_images: np.ndarray):
        """
        PyBaSiC Illumination correction as described in http://www.nature.com/articles/ncomms14836

        Parameters
        ----------
        brightfield_images : np.ndarray
            array of frames to perform illumination correction on

        Returns
        -------
        np.ndarray
            illumination corrected frames
        """
        # capture pybasic warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            flatfield, darkfield = pybasic.basic(
                brightfield_images, darkfield=True, verbosity=False
            )
            baseflour = pybasic.background_timelapse(
                images_list=brightfield_images,
                flatfield=flatfield,
                darkfield=darkfield,
                verbosity=False,
            )
            brightfield_images_corrected_original = pybasic.correct_illumination(
                images_list=brightfield_images,
                flatfield=flatfield,
                darkfield=darkfield,
                background_timelapse=baseflour,
            )

            # convert corrected images to numpy array, normalize, and convert to uint8
            brightfield_images_corrected = np.array(
                brightfield_images_corrected_original
            )
            brightfield_images_corrected[
                brightfield_images_corrected < 0
            ] = 0  # make negatives 0
            brightfield_images_corrected = brightfield_images_corrected / np.max(
                brightfield_images_corrected
            )  # normalize the data to 0 - 1
            brightfield_images_corrected = (
                255 * brightfield_images_corrected
            )  # Now scale by 255
            corrected_movie = brightfield_images_corrected.astype(np.uint8)

            return corrected_movie
