import math
from itertools import product
from input_store import InputStore

# import static logger and create shortcut function
from logger import Logger
log = Logger.log


class GridPoints():
    # default config
    config = {'grid_coverage_per_step': {'x': 250, 'y': 250}, 'grid_coverage_offset': {'x': 0, 'y': 0}}

    def __init__(self, farmwarename, config):
        self.farmwarename = farmwarename
        self.config = InputStore.merge_config(self.config, config)

    def _calc_steps_for_dimension(self, min_pos=0, max_pos=0, coverage=220):
        """ Calculate steps

        [description]

        Keyword Arguments:
            min_pos {number} -- [description] (default: {0})
            max_pos {number} -- [description] (default: {0})
            coverage {number} -- [description] (default: {220})

        Returns:
            [list] -- of integer steps
        """
        # if they are the same, return
        if max_pos == min_pos:
            return [min_pos]

        steps_ceil = math.ceil((max_pos - min_pos) / coverage)
        step_width = int((max_pos - min_pos) / steps_ceil)

        # next, we need to get the bed dimensions
        steps = [(i * step_width) + (min_pos - step_width) for i in range(1, steps_ceil + 2)]

        # log('--> [_calc_steps_for_dimension] min_pos {}, max_pos {}, coverage {} --- steps_ceil {}, step_width {}, steps {}'
        #     .format(min_pos, max_pos, coverage, steps_ceil, step_width, steps),
        #     title='load_points')

        return steps

    def _calc_steps(self, points):
        cover = self.config['grid_coverage_per_step']

        # get array of x's and y's, then pass min and max to _calc_steps_for_dimension()
        xs = [p['x'] for p in points]
        ys = [p['y'] for p in points]
        steps_x = self._calc_steps_for_dimension(min(xs), max(xs), cover['x'])
        steps_y = self._calc_steps_for_dimension(min(ys), max(ys), cover['y'])

        return list(product(steps_x, steps_y))

    def calc_points_from_points(self, points):
        if self.config['grid_coverage_per_step'] is None or len(points) == 0:
            return None

        # get steps
        steps = self._calc_steps(points)

        i = 1
        points_out = []
        for x, y in steps:
            points_out.append({'id': i, 'x': x, 'y': y})
            i += 1

        log('points calculated, result: {}'.format(len(points_out)), title='load_points')

        return points_out

    # see https://stackoverflow.com/questions/31068162/removing-a-dictionary-from-a-list-of-dictionaries-in-python
    def _del_from_dict_list(self, source_list, dict_id):
        return [d for d in source_list if d['id'] != dict_id]

    def _find_points_in_square(self, points, step_center={'x': 0, 'y': 0}):
        """ Count number of points that fall within the square bound by bottom_left and top_right corners.

        Arguments:
            points {list} -- of Celeryscript points with ['x'] and ['y'] dict keys

        Keyword Arguments:
            bottom_left {tuple} -- (x, y) coordinates of the square's bottom left corner (default: {(0, 0)})

        Returns:
            int -- the count of points within that square
        """
        out_arr = []
        cover = self.config['grid_coverage_per_step']
        offset = self.config['grid_coverage_offset']

        bottom_left = {
            'x': step_center["x"] - (cover['x'] / 2) + offset['x'],
            'y': step_center["y"] - (cover['y'] / 2) + offset['y']
        }
        top_right = {
            'x': step_center["x"] + (cover['x'] / 2) + offset['x'],\
            'y': step_center["y"] + (cover['y'] / 2) + offset['y']
        }

        for p in points:
            if bottom_left['x'] <= int(p['x']) <= top_right['x']\
                and bottom_left['y'] <= int(p['y']) <= top_right['y']:
                out_arr.append(p)

        # print("==> found {} points in square {}, {}".format(len(out_arr), bottom_left, top_right))

        return out_arr

    def _find_square_with_max_points(self, points, steps, starting_points=[{'x': 0, 'y': 0}]):
        """[summary]

        Arguments:
            points {[type]} -- [description]
            steps {list of pairs (x,y)} --

        Keyword Arguments:
            starting_points {list} -- [description] (default: {[{'x', 'y'}]})

        Returns:
            [type] -- list of point dicts [{'x': 0, 'y': 0, 'points': dict of points}]. The
            x, y will be set to the average point position between all points found.
        """

        points_counts = []
        for x, y in steps:
            # count how many plants in square
            points_in_sq = self._find_points_in_square(points, step_center={'x': x, 'y': y})

            if len(points_in_sq) > 0:
                points_counts.append({'x': x, 'y': y, 'points': points_in_sq})
                # avg_x = sum([points_in_sq[i]['x'] for i in range(0, len(points_in_sq))]) / len(points_in_sq)
                # avg_y = sum([points_in_sq[i]['y'] for i in range(0, len(points_in_sq))]) / len(points_in_sq)
                # points_counts.append({
                #     'x': avg_x,
                #     'y': avg_y,
                #     'points': self._find_points_in_square(points, step_center={'x': avg_x, 'y': avg_y})
                # })

        # log('points_counts: {}'.format(len(points_counts)), title='load_points')
        if len(points_counts) == 0:
            return None

        square_with_max_plants = max(points_counts, key=lambda i: len(i['points']))
        # print("square_with_max_plants cnt {}".format(len(square_with_max_plants['points'])))

        return square_with_max_plants

    def summarize_points_by_coverage(self, points):
        if self.config['grid_coverage_per_step'] is None or len(points) == 0:
            return None

        pid = 1
        points_in = points.copy()
        points_out = []

        # get steps for covering area for input points
        steps = self._calc_steps(points)

        while len(points_in) > 0:
            res = self._find_square_with_max_points(points_in, steps)

            if res is None:
                break

            points_out.append({**res, **{'id': pid}})
            pid += 1

            # delete points appended from points_in and loop
            for p in res['points']:
                points_in = self._del_from_dict_list(points_in, p['id'])

            # print("==> points remaining  {}".format(len(points_in)))

        log("summarized into {} points with coverage {}".format(len(points_out),
                                                                self.config['grid_coverage_per_step']),
            title="summarize_points_by_coverage")

        return points_out
