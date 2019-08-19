import os
from traceback import format_exc

from plants import Plants
from grid_points import GridPoints
from input_store import InputStore
from sequence_executor import SequenceExecutor
from point_sort import PointSort

# import static logger and create shortcut function
from logger import Logger
log = Logger.log


def run_points_loop(points, sexec, run_after_each=None, use_tsp_solver=True):
    points_sorted = sort_points(points, use_tsp_solver)

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


def sort_points(points, use_tsp_solver=True):
    """ Sort the points """
    if (use_tsp_solver is True):
        return PointSort.sort_points_tsp_greedy(points)
    else:
        return PointSort.sort_points(points)


if __name__ == "__main__":

    # get farmware name from path
    FARMWARE_NAME = "powerloop-farmware"
    try:
        FARMWARE_NAME = ((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', '')
    except:
        pass

    Logger.FARMWARE_NAME = FARMWARE_NAME

    try:
        # create new instance of the InputStore. this will load the user input or defaults
        input_store = InputStore(FARMWARE_NAME)
        # set logger level
        Logger.set_level(input_store.input['debug'])

        # create SequenceExecutor instance
        sexec = SequenceExecutor(FARMWARE_NAME, input_store)

        log('Start...', message_type='info', title=FARMWARE_NAME)

        # create Plants class instance
        plants = Plants(FARMWARE_NAME, input_store)
        grid_points = GridPoints(FARMWARE_NAME, input_store)
    except Exception as e:
        log("exception: {}, traceback: {}".format(e, format_exc()),
            message_type='error',
            title=FARMWARE_NAME + " : init")
        raise Exception(e)
    else:
        try:
            # load the plants
            points_plants = plants.load_points_with_filters()

            # Use plants loaded to choose grid waypoints
            points_grid = grid_points.calc_points_from_points(points_plants)

            # function to pass to run_points_loop() to run after each move
            def run_after_each(p):
                plants.save_meta(p)
                plants.save_plant_stage(p)

            # use points resulting from points_grid if used (returns not None)
            run_points_loop(points=points_grid if points_grid else points_plants,
                            sexec=sexec,
                            run_after_each=run_after_each if points_grid is None else None,
                            use_tsp_solver=input_store.input['use_tsp_greedy'])
        except Exception as e:
            log("exception: {}, traceback: {}".format(e, format_exc()),
                message_type='error',
                title=FARMWARE_NAME + " : runtime")
            raise Exception(e)

    log('End...', message_type='info', title=FARMWARE_NAME)
