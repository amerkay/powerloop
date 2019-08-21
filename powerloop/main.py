""" Main farmware class

This is the main executable class for powerloop farmware. Read comments below for description of how
it works.

### To copy just one of the classes for use in your own project:

I tried to keep all classes separated by functionality as much as possible. To use any of the classes
independantely in your own project, just replace or copy relevant classes and use in your project:
    - Remove Logger and replace with your own "print()" or "log()" function throughout the class copied.

Variables:
    log {method} -- A reference function Logger().log()
"""

import sys
from traceback import format_exc
import concurrent.futures

from plants import Plants
from grid_points import GridPoints
from input_store import InputStore
from sequence_executor import SequenceExecutor
from point_sort import PointSort

# import static logger and create shortcut function
from logger import Logger
log = Logger.log

# Farmware name, must be same as "package" attribe in manifest.json
FARMWARE_NAME = "power_loop"


def run_points_loop(points, sexec, run_after_each=None, use_tsp_solver=True):
    """ Loop all the points loaded, and execute sequences.

    Arguments:
        points {list of Points} -- list of points to loop
        sexec {SequenceExecutor instance} -- SequenceExecutor instance, see sequence_executor.py

    Keyword Arguments:
        run_after_each {method} -- Method to run after each move (default: {None})
        use_tsp_solver {bool} -- Use TSP Solver instead of regular sort (default: {True})
    """
    points_sorted = PointSort.sort_points(points, use_tsp_solver)

    if len(points_sorted) > 0:
        sexec.execute_sequence_init()

        # for every plant, do
        for p in points_sorted:
            sexec.execute_sequence_before()
            sexec.move_absolute_point(p)
            sexec.execute_sequence_after()

            if run_after_each is not None:
                run_after_each(p)

        sexec.execute_sequence_end()


if __name__ == "__main__":
    Logger.FARMWARE_NAME = FARMWARE_NAME

    try:
        # create new instance of the InputStore. this will load the user input or defaults
        input_store = InputStore(FARMWARE_NAME)
        # set logger level
        Logger.set_level(input_store.input['debug'])

        # create SequenceExecutor instance
        sexec = SequenceExecutor(FARMWARE_NAME, input_store.input)

        log('Started with python version {}'.format(sys.version_info), message_type='info', title="init")

        # create Plants class instance
        plants = Plants(FARMWARE_NAME, input_store.input)
        grid_points = GridPoints(FARMWARE_NAME, input_store.input)

        # Start a concurrent task executor, with pool size 4
        # Example at doc @ https://docs.python.org/3/library/concurrent.futures.html
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=4)

        # load the plants
        points_plants = plants.load_points_with_filters()

        # Use plants loaded to choose grid waypoints
        points_grid = grid_points.calc_points_from_points(points_plants)

        def run_after_each(p):
            """ Function to pass to run_points_loop() to run after each move.

            Simply adds plants.save_plant(p) to the Task Executor. Note that exceptions raised
            from execution are not fatal, and this save will be lost. An error should be logged
            by save_plant().

            Arguments:
                p {set} -- Celeryscript Point JSON object
            """
            executor.submit(plants.save_plant, p)

        # use points resulting from points_grid if used (returns not None)
        run_points_loop(points=points_grid if points_grid else points_plants,
                        sexec=sexec,
                        run_after_each=run_after_each if points_grid is None else None,
                        use_tsp_solver=input_store.input['use_tsp_greedy'])

    except Exception as e:
        log("Exception thrown: {}, traceback: {}".format(e, format_exc()), message_type='error', title="main")
        raise Exception(e)

    # shutdown executor
    executor.shutdown()
    log('End', message_type='success', title=FARMWARE_NAME)
