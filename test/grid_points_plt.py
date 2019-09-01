""" Test script for GridPoints.

Uses matplotlib to draw resulting points to visit.

Variables:
    sys.path.append('../powerloop/') {[type]} -- [description]
    log {[type]} -- [description]
    FARMWARE_NAME {str} -- [description]
    if __name__ {[type]} -- [description]
"""

import sys
import random
from traceback import format_exc


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from itertools import cycle

sys.path.append("../src/")

from fake_plants import FakePlants
from grid_points import GridPoints

# import static logger and create shortcut function
from logger import Logger

log = Logger.log

# Farmware name, must be same as "package" attribe in manifest.json
FARMWARE_NAME = "power_loop_dev"

Logger.FARMWARE_NAME = FARMWARE_NAME

cycol = cycle("bgrcmyk")  # cycle through colors

# config
cover = {"x": 400, "y": 400}
offset = {"x": 25, "y": 25}
overlap = 0

if __name__ == "__main__":
    try:
        # set logger level
        Logger.set_level(3)

        log(
            "Started with python version {}".format(sys.version_info),
            message_type="info",
            title="init",
        )

        # Load fake plants
        points_plants = FakePlants.get_fake_plants()

        # init instance of GridPoints
        grid_points = GridPoints(
            FARMWARE_NAME,
            config={
                "grid_coverage_per_step": cover,
                "grid_coverage_offset": offset,
                "grid_coverage_overlap": overlap,
            },
        )

        # points_grid = grid_points.calc_waypoints_basic(points_plants)
        # Use plants loaded to choose grid waypoints, if overlap = 0, use basic waypoints
        if overlap >= 30:
            waypoints = grid_points.calc_waypoints_summary(points_plants)
        else:
            waypoints = grid_points.calc_waypoints_basic(points_plants)

        points = waypoints if waypoints else points_plants

        # ------------- plot plants ----------------
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt_x = []
        plt_y = []
        for p in points_plants:
            plt_x.append(p["x"])
            plt_y.append(p["y"])

            # draw rect around radius
            r = int(p["radius"])
            ax.add_patch(
                Rectangle(
                    xy=(p["x"] - r, p["y"] - r),
                    width=r * 2,
                    height=r * 2,
                    linewidth=2,
                    color="g",
                    fill=False,
                )
            )
        ax.scatter(plt_x, plt_y, color=next(cycol), s=10)

        # Add rectangles using resulting points as center
        for p in points:
            ax.add_patch(
                # xy (bottom-left) uses coverage/2 area and offset for each axis to calc
                Rectangle(
                    xy=(
                        p["x"] - (cover["x"] / 2) + offset["x"],
                        p["y"] - (cover["y"] / 2) + offset["y"],
                    ),
                    width=cover["x"],
                    height=cover["y"],
                    linewidth=random.randint(1, 3),
                    color=next(cycol),
                    fill=False,
                )
            )
        ax.axis("equal")
        plt.show()
        # ------------- plot plants ----------------

    except Exception as e:
        log(
            "Exception thrown: {}, traceback: {}".format(e, format_exc()),
            message_type="error",
            title="main",
        )
        raise Exception(e)

    log("End", message_type="success", title=FARMWARE_NAME)
