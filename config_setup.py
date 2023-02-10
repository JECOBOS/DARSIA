"""
5-step config setup applied to the images taken under the UiS FluidFlower workshop.
"""
import json
from pathlib import Path

import cv2
import darsia
import matplotlib.pyplot as plt
import skimage

# Control
plot = True

# Initialize
config: dict() = {}
config["description"] = "Config for images taken under the UiS FluidFlower workshop"
# TODO provide dimensions of the visible domain in meters
config["physical asset"] = {"width": TODO, "height": TODO, "depth": 0.012, "porosity": 0.44}
config["curvature"] = {}

# !----- 1. Step: Read curved image and initialize the config file

# Choose a image of your choice.
# TODO - specify path to folder containing all images.
folder = (
    TODO
)

# Read image
images = list(sorted((Path(folder)).glob("*.JPG")))
baseline = images[0]
img = cv2.imread(str(baseline))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Brighten up image for better control
img = skimage.exposure.adjust_gamma(img, gamma = 0.8)

# All relevant config parameters will be stored in a dictionary collecting several configs.
# Initialize the config dict.
curvature_correction = darsia.CurvatureCorrection(baseline)

# !----- 2. Step: Bulge
plt.imshow(img)
if plot:
    plt.show()

# Choose horizontal and vertical bulge such that all laser grid lines are bulged inwards.
# In some cases it might be necessary to define offsets for the image center;
# the default is to use the numerical center.
# TODO: Omit - only required for advanced analysis.
config["curvature"]["init"] = {
    "horizontal_bulge": 0e-9,
    "vertical_bulge": 0e-9,
}

# Apply bulge 'correction'
img = curvature_correction.simple_curvature_correction(
    img, **config["curvature"]["init"]
)

# !----- 3. Step: Bulge

# Read coordinates of 4 points, defining a rectangular of known dimensions.
# Here, we choose a bounding box with corners on the laser grid.
plt.imshow(img)
if plot:
    plt.show()

# Accurare dimensions from techincal drawing by Kristoffer Eikehaug.
fluidflower_width = config["physical asset"]["width"]
fluidflower_height = config["physical asset"]["height"]
config["curvature"]["dimensions"] = {
    "width": fluidflower_width,
    "height": fluidflower_height,
}

# Define config file for applying a perspective transform, which after all transforms
# and crops the image to a box with known aspect ratio. This step already
# corrects for bulging in the normal direction due to the curvature of the
# FluidFlower.
# TODO Provide (col,row) pixel coordinates. Start in the top left corner and
# TODO visit all corners in counterclock wise direction.
config["curvature"]["crop"] = {
    "pts_src": [
        [LEFT TOP, TODO],
        [LEFT BOTTOM, TODO],
        [RIGHT BOTTOM, TODO],
        [RIGH TOP, TODO],
    ],
    # Specify the true dimensions of the reference points - known as they are
    # points on the laser grid
    "width": fluidflower_width,
    "height": fluidflower_height,
}

# Extract quad ROI
img = darsia.extract_quadrilateral_ROI(img, **config["curvature"]["crop"])

# !----- 3. Step: Bulge in x and y direction

# Plot...
plt.imshow(img)
if plot:
    plt.show()

# ... and determine the parameters as described in the darsia-notes
# For this, require the dimensions of the image
Ny, Nx = img.shape[:2]

# Read the coordinates of the two largest impressions in y-direction (approx. top and bottom center)
# TODO: Omit - only required for advanced analysis.
left = 0
right = 0
top = 0
bottom = 0
(
    horizontal_bulge,
    horizontal_bulge_center_offset,
    vertical_bulge,
    vertical_bulge_center_offset,
) = curvature_correction.compute_bulge(
    img=img, left=left, right=right, top=top, bottom=bottom
)

# Choose horizontal and vertical bulge such that all laser grid lines are bulged inwards
config["curvature"]["bulge"] = {
    "horizontal_bulge": horizontal_bulge,
    "vertical_bulge": vertical_bulge,
    "horizontal_center_offset": horizontal_bulge_center_offset,
    "vertical_center_offset": vertical_bulge_center_offset,
}

# Apply final curvature correction
img = curvature_correction.simple_curvature_correction(
    img, **config["curvature"]["bulge"]
)

# !----- 4. Step: Correct for stretch

# Plot...
plt.imshow(img)
if plot:
    plt.show()

# TODO: Omit - only required for advanced analysis.
# Update the offset to the center
horizontal_stretch_center_offset = 0.
vertical_stretch_center_offset = 0.

# Compute the tuning parameter as explained in the notes
# Consider only well1 for now - and leave the stretch center in the center
horizontal_stretch = 0.
vertical_stretch = 0.

# Choose horizontal and vertical bulge such that all laser grid lines are bulged inwards
config["curvature"]["stretch"] = {
    "horizontal_stretch": horizontal_stretch,
    "horizontal_center_offset": horizontal_stretch_center_offset,
    "vertical_stretch": vertical_stretch,
    "vertical_center_offset": vertical_stretch_center_offset,
}

# Apply final curvature correction
img = curvature_correction.simple_curvature_correction(
    img, **config["curvature"]["stretch"]
)

# !----- 6. Step: Validation - Compare with a 'perfect' grid layed on top
da_img = darsia.Image(
    img,
    width=config["curvature"]["crop"]["width"],
    height=config["curvature"]["crop"]["height"],
).add_grid(dx=0.1, dy=0.1)

plt.imshow(da_img.img)
if plot:
    plt.show()

# !----- 7. Step: Color correction

# # Need to define a coarse ROI which contains the color checker - use [y,x] pixel ordering
# config["color"] = {
#     "roi": (
#         slice(int(50), int(550)),
#         slice(int(6550), int(7330)),
#     ),
# }

# !----- Summary of the config - copy and move to another file.
with open("config_pre.json", "w") as convert_file:
    convert_file.write(json.dumps(config, indent=4))
print("Include model parameters and location of cleaning filter, and rename to config.json.")
