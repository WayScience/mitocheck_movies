'''
Author: Keenan Manpearl
Date Created: 1/30/2023
'''


import pandas as pd
import pathlib
import os
from aspera_download import AsperaDownloader



aspera_path = pathlib.Path("/home/keenanmanpearl/.aspera/ascli/sdk/ascp")
aspera_key_path = pathlib.Path("asperaweb_id_dsa.openssh")
# metadata downloaded from https://github.com/IDR/idr-metadata/blob/master/idr0013-neumann-mitocheck/screenA/idr0013-screenA-plates.tsv
screens_path = pathlib.Path("idr0013-screenA-plates.tsv")
idr_id = "idr0013"
num_wells = 384



with open(screens_path) as f:
    plates = [row.split()[0] for row in f]
# change to desired number of plates to download
# whole dataset is > 20 TB
plate_subset = plates[:5]

downloader = AsperaDownloader(aspera_path, aspera_key_path, screens_path, idr_id)
for plate in plate_subset:
    for well in range(1,num_wells +1):
        save_dir = pathlib.Path(f"{plate}/{well}.ch5")
        downloader.download_image(plate = plate, well_num = well, save_dir = save_dir)

