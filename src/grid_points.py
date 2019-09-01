""" GridPoints class

Two main functions:
- calc_waypoints_basic() - simple grid covering input Plants area
- calc_waypoints_summary() - loops to find areas (of coverage size) with most points within,
    outputs only waypoints containing points (and their radius).

"""
import math

from itertools import product
from input_store import InputStore

# import static logger and create shortcut function
from logger import Logger

log = Logger.log


class GridPoints:
    # default config
    config = {
        "grid_coverage_per_step": {"x": 250, "y": 250},
        "grid_coverage_offset": {"x": 0, "y": 0},
        "grid_coverage_overlap": 30,
    }

    def __init__(self, farmwarename, config):
        """ Class constructor """
        self.farmwarename = farmwarename
        self.config = InputStore.merge_config(self.config, config)
        self._chk_inputs()

    def calc_waypoints_basic(self, points):
        """ Basic grid around points provided.

        Arguments:
            points {list of dicts} -- Points to cover

        Returns:
            [list of dicts] -- resulting points
        """
        if self.config["grid_coverage_per_step"] is None or len(points) == 0:
            return None

        # generate steps
        steps = self._gen_steps(points)

        i = 1
        waypoints = []

        steps_counted = self._find_points_for_steps(points, steps, use_radius=False)
        for s in steps_counted:
            if len(s["points"]) > 0:
                waypoints.append({"id": i, "x": s["x"], "y": s["y"]})
                i += 1

        log(
            "points calculated, result: {}".format(len(waypoints)),
            title="calc_waypoints_basic",
        )

        return waypoints

    def calc_waypoints_summary(self, points):
        """ Summarize Points only if a point is found within rectangular coverage area,
        using config values (see __init__):
         - grid_coverage_per_step x,y,
         - grid_coverage_offset per step x,y
         - grid_coverage_overlap percentage (20-50 integer).

        Arguments:
            points {list of point dicts} -- Points to cover, could be using Plants class filtering.

        Returns:
            list of point dicts -- resulting points list to cover input points
        """
        if self.config["grid_coverage_per_step"] is None or len(points) == 0:
            return None

        cover = self.config["grid_coverage_per_step"]
        pid = 1
        points_in = points.copy()
        waypoints = []

        # generate steps to search
        steps = self._gen_steps(points)

        while len(points_in) > 0:
            steps_counted = self._find_points_for_steps(
                points_in, steps, use_radius=True
            )

            if len(steps_counted) == 0:
                raise Exception(
                    "Grid points failed. Try using a higher overlap value. Try 50%."
                )

            rect_with_max_plants = max(steps_counted, key=lambda i: len(i["points"]))
            # print("rect_with_max_plants cnt {}".format(len(rect_with_max_plants['points'])))

            # add id and append
            waypoints.append({**rect_with_max_plants, **{"id": pid}})
            pid += 1

            # delete points appended from points_in and loop
            for p in rect_with_max_plants["points"]:
                points_in = self._del_from_dict_list(points_in, p["id"])

            # print("==> points remaining  {}".format(len(points_in)))

        log(
            "summarized into {} points with coverage {}".format(len(waypoints), cover),
            title="calc_waypoints_summary",
        )

        return waypoints

    def _chk_inputs(self):
        """ Check configuration or raise exception

        Raises:
            Exception -- if irrecoverable invalid config
        """
        cover = self.config["grid_coverage_per_step"]
        if cover is None:
            return

        if cover["x"] < 100 or cover["y"] < 100:
            raise Exception("coverage (x,y) cannot be less than 100,100")

        if not (0 <= self.config["grid_coverage_overlap"] <= 50):
            self.config["grid_coverage_overlap"] = 30
            log(
                "Invalid value, resetting grid_coverage_overlap to default: {}".format(
                    self.config["grid_coverage_overlap"]
                ),
                title="GridPoints __init__",
            )

        if self.config["grid_coverage_offset"] is not None:
            offset = self.config["grid_coverage_offset"]
            if abs(offset["x"]) >= cover["x"] / 2 or abs(offset["y"]) >= cover["y"] / 2:
                raise Exception(
                    "Summarize by coverage cannot have offset >= 50% of the coverage."
                )

    def _gen_steps_for_dimension(self, min_pos=0, max_pos=0, coverage=220):
        """ Generate steps for dimension (x or y)

        Keyword Arguments:
            min_pos {int} -- Minimum position (default: {0})
            max_pos {int} -- Maximum position (default: {0})
            coverage {int} -- coverage in mm (passed from input coverage) (default: {220})

        Returns:
            [list] -- of integer steps
        """
        # if they are the same, return
        if max_pos == min_pos:
            return [min_pos]

        # set overlap percentage. recommended 0.2-0.5 value
        overlap = self.config["grid_coverage_overlap"] / 100
        step_width = coverage * (1 - overlap)
        steps_ceil = math.ceil((max_pos - min_pos) / step_width)

        # next, we need to get the bed dimensions
        start_point = min_pos - step_width
        steps = [(i * step_width) + start_point for i in range(1, steps_ceil + 2)]

        # log('--> [_gen_steps_for_dimension] min_pos {}, max_pos {}, coverage {} --- steps_ceil {}, step_width {}, steps {}'
        #     .format(min_pos, max_pos, coverage, steps_ceil, step_width, steps),
        #     title='_gen_steps_for_dimension')

        return steps

    def _gen_steps(self, points):
        """ Uses _gen_steps_for_dimension() to generate steps for each axis.

        Arguments:
            points {list of dict} -- Points input to use for step generation.

        Returns:
            [list of (x,y) pairs] -- Resulting steps generated
        """
        cover = self.config["grid_coverage_per_step"]
        offset = self.config["grid_coverage_offset"]

        # get array of x's and y's, then pass min and max to _gen_steps_for_dimension()
        # take plant radius into consideration
        # TODO could take plant spread from Openfarm
        min_x = (
            min([int(p["x"]) - int(p["radius"]) for p in points])
            - offset["x"]
            + cover["x"] / 2
        )
        max_x = (
            max([int(p["x"]) + int(p["radius"]) for p in points])
            - offset["x"]
            - cover["x"] / 2
        )
        min_y = (
            min([int(p["y"]) - int(p["radius"]) for p in points])
            - offset["y"]
            + cover["y"] / 2
        )
        max_y = (
            max([int(p["y"]) + int(p["radius"]) for p in points])
            - offset["y"]
            - cover["y"] / 2
        )

        steps_x = self._gen_steps_for_dimension(min_x, max_x, cover["x"])
        steps_y = self._gen_steps_for_dimension(min_y, max_y, cover["y"])

        return list(product(steps_x, steps_y))

    def _del_from_dict_list(self, source_list, dict_id):
        """ Delete dict with 'id' = dict_id from source_list
        See https://stackoverflow.com/a/31068594

        Arguments:
            source_list {list of dicts} -- with 'id' value set
            dict_id {int} -- Used to match dict to delete with 'id' = dict_id
        """
        return [d for d in source_list if d["id"] != dict_id]

    def _find_points_in_rect(
        self, points, step_center={"x": 0, "y": 0}, use_radius=True
    ):
        """ Count number of points that fall within the rect bound by bottom_left and top_right corners.

        Arguments:
            points {list} -- of Celeryscript points with ['x'] and ['y'] dict keys

        Keyword Arguments:
            step_center {tuple} -- (x, y) coordinates of the rect's center (default: {(0, 0)})

        Returns:
            int -- the count of points within that rect
        """
        out_arr = []
        cover = self.config["grid_coverage_per_step"]
        offset = self.config["grid_coverage_offset"]

        bottom_left = {
            "x": step_center["x"] - (cover["x"] / 2) + offset["x"],
            "y": step_center["y"] - (cover["y"] / 2) + offset["y"],
        }
        top_right = {
            "x": bottom_left["x"] + cover["x"],
            "y": bottom_left["y"] + cover["y"],
        }

        for p in points:
            r = int(p["radius"]) if use_radius else 0
            if (
                bottom_left["x"] <= int(p["x"]) - r
                and int(p["x"]) + r <= top_right["x"]
                and bottom_left["y"] <= int(p["y"]) - r
                and int(p["y"]) + r <= top_right["y"]
            ):
                out_arr.append(p)

        # print("==> found {} points in rect {}, {}".format(len(out_arr), bottom_left, top_right))

        return out_arr

    def _find_points_for_steps(self, points, steps, use_radius=True):
        """ Uses _find_points_in_rect() to find points in each rect

        Arguments:
            points {list of dicts} -- The points to fit into the steps rectangles
            steps {list of pairs (x,y)} -- to count plants within

        Keyword Arguments:
            use_radius {bool} -- Consider plant radius (default: True)

        Returns:
            [type] -- list of point dicts [{'x': 0, 'y': 0, 'points': dict of points}]. The
            x, y will be the input steps with points they contain.
        """
        points_counts = []
        for x, y in steps:
            # count how many plants in rect
            points_in_sq = self._find_points_in_rect(
                points, step_center={"x": x, "y": y}, use_radius=use_radius
            )

            if len(points_in_sq) > 0:
                points_counts.append({"x": x, "y": y, "points": points_in_sq})

        # log('points_counts: {}'.format(len(points_counts)), title='_find_points_for_steps')
        return points_counts
