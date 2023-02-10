"""
Module containing the general setup for a table top fluidflower rig.
Includes segmentation of the geometry and possibility to tune the expert
knowledge if needed.

"""
from pathlib import Path
from typing import Union

import numpy as np
from darsia_fluidflower.analysis.fluidflowerco2analysis import \
    FluidFlowerCO2Analysis
from darsia_fluidflower.rigs.segmentedfluidflower import SegmentedFluidFlower


class FluidFlower(SegmentedFluidFlower, FluidFlowerCO2Analysis):
    def __init__(
        self,
        baseline: Union[str, Path, list[str], list[Path]],
        config: Union[str, Path],
        results: Union[str, Path],
        update_setup: bool = False,
        verbosity: bool = True,
    ) -> None:
        """
        Constructor for table top rig specific data.

        Args:
            base (str, Path or list of such): baseline images, used to
                set up analysis tools and cleaning tools
            config (str or Path): path to config dict
            update_setup (bool): flag controlling whether cache in setup
                routines is emptied.
        """
        SegmentedFluidFlower.__init__(self, baseline, config, update_setup)
        FluidFlowerCO2Analysis.__init__(
            self, baseline, config, results, update_setup, verbosity
        )

    # ! ---- Auxiliary setup routines

    def _segment_geometry(self, update_setup: bool = False) -> None:
        """
        See SegmentedFluidFlower.

        """
        # super()._segment_geometry(update_setup)
        self.labels = np.ones(self.base.img.shape[:2], dtype=int)

        # TODO enable if expert knowledge is needed

        # # Identify water layer
        # self.water = self._labels_to_mask(self.config["segmentation"]["water"])

        # # Identify ESF layer
        # self.esf_sand = self._labels_to_mask(self.config["segmentation"]["esf"])

        # # Identify C layer
        # self.c_sand = self._labels_to_mask(self.config["segmentation"]["c"])

    # ! ---- Expert knowledge

    def _expert_knowledge_co2(self) -> np.ndarray:
        """
        Retrieve expert knowledge, i.e., areas with possibility for CO2.

        Returns:
            np.ndarray: mask with no CO2.

        """
        return FluidFlowerCO2Analysis._expert_knowledge_co2(self)

    def _expert_knowledge_co2_gas(self, co2) -> np.ndarray:
        """
        Retrieve expert knowledge, i.e., areas with possibility for CO2(g).

        Args:
            co2 (darsia.Image): mask for CO2.

        Returns:
            np.ndarray: mask with no CO2(g)

        """
        return FluidFlowerCO2Analysis._expert_knowledge_co2_gas(self, co2)
