# darsia_demonstration
Template for a basic analysis of a table top FluidFlower.

In connection to the UiS workshop, organized by Kristoffer Eikehaug.
This repository contains material used in the image analysis session
of the 2-day workshop.

To proceed:

1. Visit config_setup.py and choose parameters such that
the images are cropped to a suitable ROI. This step produces
a config file config_pre.json.

2. Copy config_pre.json to config.json and add content of
tracer_config.json containing tuning parameters to steer
the thresholding.

3. Visit segmentation.py and adapt the path to run a
segmenentation analysis. Try running 'python segmentation.py'.

4. Start tuning the parameters. Focus on the color spaces,
and thresholding strategy (static vs. dynamic) and values.
If using verbosity = 1, the dynamic threshold values are
prompted to screen. If choosing verbosity = 2, also intermediate
results are plotted, as image differences, prior and posterior
etc. allowing to better understand deicision on the color
space.
