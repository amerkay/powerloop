import tsp_greedy_solver

from farmware_tools import device

# import static logger and create shortcut function
from logger import Logger
log = Logger.log


class PointSort():
    @staticmethod
    def sort_points(points):
        points_sorted = sorted(points, key=lambda elem: (int(elem['x']), int(elem['y'])))
        # log(points_sorted, title='sort_points')

        return points_sorted

    @staticmethod
    def sort_points_tsp_greedy(points):
        """
        Sort points using Travelling Salesman Greedy Solution. See tsp_greedy_solver.py
        """

        # Get current location
        curr_pos = device.get_current_position()

        # this is for local debugging purposes
        if curr_pos is None:
            curr_pos = {'x': 0, 'y': 0}

        # prepare points_to_sort = [tuple(float), ...]
        # add current location as starting point, id 0
        points_to_sort = [(0, curr_pos['x'], curr_pos['y'])]
        for p in points:
            points_to_sort.append((p['id'], p['x'], p['y']))

        # run through Greedy travelling salesman algorithm
        tsp_solution = tsp_greedy_solver.solveGreedyTSP(points_to_sort)

        # sort points according to tsp_solution's order
        points_sorted = []
        for p in tsp_solution[0]:
            try:
                p_full = next(item for item in points if item["id"] == p[0])
                points_sorted.append(p_full)
            except Exception:  # continue if id does not exist, eg starting point
                continue

        log("{} points sorted with TSP Greedy, min_dist is {}".format(len(tsp_solution[0]), tsp_solution[1]),
            'debug', title='sort_points_tsp_greedy')
        # log(points_sorted, 'debug', title='sort_points_tsp_greedy')

        return points_sorted
