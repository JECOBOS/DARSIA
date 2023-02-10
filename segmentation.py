"""
Segmentation analysis.
"""
from fluidflower import FluidFlower
from pathlib import Path
import cv2

################################################################
# Organize the data

# TODO provide the path to the folder containing all images
images_folder = Path("...")
images = list(sorted(images_folder.glob("*.JPG")))

# Extract basline image (here the first image)
baseline = images[:1]
images = images[3::3]

# Path to analysis specific config file
config = Path("./config.json")

# Path to results directory, create if not existent yet
results = Path("./results")
results.mkdir(parents=True, exist_ok=True)

################################################################
# Define FluidFlower based on a full set of basline images
analysis = FluidFlower(
    baseline=baseline,  # paths to baseline images
    config=config,  # path to config file
    results=results,  # path to results directory
)

################################################################
# Perform standardized CO2 batch analysis.
analysis.batch_segmentation(images, plot_contours=False, write_contours_to_file=True)
