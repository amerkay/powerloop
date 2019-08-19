# import datetime
import math

# from farmware_tools import app

# import static logger and create shortcut function
from logger import Logger
log = Logger.log


class GridPoints():
    def __init__(self, farmwarename, input_store):
        self.farmwarename = farmwarename
        self.input_store = input_store
        self.input = input_store.input

    def calc_steps(self, min_pos=0, max_pos=0, coverage=220):
        # if they are the same, return
        if max_pos == min_pos:
            return [min_pos]

        steps_ceil = math.ceil((max_pos - min_pos) / coverage)
        step_width = int((max_pos - min_pos) / steps_ceil)

        # next, we need to get the bed dimensions
        steps = [(i * step_width) + (min_pos - step_width) for i in range(1, steps_ceil + 2)]

        log('--> [calc_steps] min_pos {}, max_pos {}, coverage {} --- steps_ceil {}, step_width {}, steps {}'.
            format(min_pos, max_pos, coverage, steps_ceil, step_width, steps),
            title='load_points')

        return steps

    def calc_points_from_points(self, points):
        if self.input['grid_coverage_per_step'] is None or len(points) == 0:
            return None

        # get array of x's and y's, then pass min and max to calc_steps()
        xs = [p['x'] for p in points]
        ys = [p['y'] for p in points]
        steps_x = self.calc_steps(min(xs), max(xs), self.input['grid_coverage_per_step'][0])
        steps_y = self.calc_steps(min(ys), max(ys), self.input['grid_coverage_per_step'][1])

        i = 1
        points_out = []
        for x in steps_x:
            for y in steps_y:
                points_out.append({'id': i, 'x': x, 'y': y})
                i += 1

        log('points calculated, result: {}'.format(points_out), title='load_points')

        return points_out
