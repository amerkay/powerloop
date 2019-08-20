import re
import time
import random

from datetime import datetime as dt
from farmware_tools import app
from fake_plants import FakePlants

# import static logger and create shortcut function
from logger import Logger
log = Logger.log


class Plants():
    """
    Main class to load with filters and loop plants

    Adapted from https://github.com/rdegosse/Loop-Plants-With-Filters, thank you @rdegosse!
    """
    def __init__(self, farmwarename, input_store):
        self.farmwarename = farmwarename
        self.input_store = input_store
        self.input = input_store.input

    def load_points_with_filters(self):
        points = app.post('points/search', payload={'pointer_type': 'Plant'})

        points = FakePlants.get_fake_plants() if Logger.LOGGER_LEVEL == 2 else points

        # this is for local debugging purposes
        if isinstance(points, str):
            return []

        log("all points loaded, count {}".format(len(points)), title='load_points_with_filters')

        points_out = self.apply_filters(points=points,
                                        point_name=self.input['pointname'],
                                        openfarm_slug=self.input['openfarm_slug'],
                                        age_min_day=self.input['age_min_day'],
                                        age_max_day=self.input['age_max_day'],
                                        meta_key=self.input['filter_meta_key'],
                                        meta_value=self.input['filter_meta_value'],
                                        min_x=self.input['filter_min_x'],
                                        min_y=self.input['filter_min_y'],
                                        max_x=self.input['filter_max_x'],
                                        max_y=self.input['filter_max_y'],
                                        pointer_type='Plant',
                                        plant_stage=self.input['filter_plant_stage'])

        log('filters applied, resulting in {} points'.format(len(points_out)),
            title='load_points_with_filters')
        # log(self.points, title='load_points_with_filters')
        return points_out

    def apply_filters(self,
                      points,
                      point_name='',
                      openfarm_slug='',
                      age_min_day=0,
                      age_max_day=36500,
                      meta_key=None,
                      meta_value=None,
                      min_x=None,
                      max_x=None,
                      min_y=None,
                      max_y=None,
                      pointer_type='Plant',
                      plant_stage=None):

        filtered_points = []
        now = dt.utcnow()

        for p in points:
            if p['pointer_type'].lower() == pointer_type.lower():
                ref_date = p['planted_at']
                if str(p['planted_at']).lower() == 'none' or str(p['planted_at']).lower() is None:
                    ref_date = p['created_at']

                age_day = (now - dt.strptime(ref_date, '%Y-%m-%dT%H:%M:%S.%fZ')).days

                b_meta = self._filter_meta(p, meta_key, meta_value)
                b_coordinate_x = self._filter_coordinates(int(p['x']), min_x, max_x)
                b_coordinate_y = self._filter_coordinates(int(p['y']), min_y, max_y)
                b_plantstage = self._filter_plant_stage(p['plant_stage'], plant_stage)

                if (p['name'].lower().find(point_name.lower()) >= 0 or point_name == '*') \
                    and (p['openfarm_slug'].lower().find(openfarm_slug.lower()) >= 0 or openfarm_slug == '*')\
                    and (age_min_day <= age_day <= age_max_day) and b_meta is True \
                        and b_coordinate_x and b_coordinate_y and b_plantstage:
                    filtered_points.append(p.copy())

        return filtered_points

    def _filter_plant_stage(self, p_stage, plant_stage):
        if None not in (p_stage, plant_stage):
            try:
                if plant_stage.lower() == p_stage.lower():
                    return True
                else:
                    return False
            except Exception as e:
                return True

        # default is true if None or failed
        return True

    def _filter_coordinates(self, p_coord, min_coord, max_coord):
        """ Filter point p by min and max

        [description]

        Arguments:
            p_coord {int} -- point coordinate p['x'] or 'y'
            min_coord {int} -- min coordinate value allowed
            max_coord {int} -- max coordinate value allowed

        Returns:
            bool -- True if match or None, False if not match
        """
        if None not in (min_coord, max_coord, p_coord):
            if int(min_coord) <= int(p_coord) <= int(max_coord):
                return True
        else:
            return True

        # if not a match, return False
        return False

    def _filter_meta(self, p, meta_key, meta_value):
        if None not in (p, meta_key, meta_value):
            try:
                target_age_in_seconds = \
                    (dt.utcnow() - dt.strptime(p['meta'][meta_key], '%Y-%m-%d %H:%M:%S.%f')).total_seconds()

                # log('==> p is None {}, key {}, value {}'.format(p is None, meta_key, meta_value), title='_filter_meta')

                if self.input['filter_meta_op'] is None or self.input['filter_meta_op'] == "==":
                    return ((p['meta'][meta_key]).lower() == meta_value.lower())
                elif self.input['filter_meta_op'] == ">=":
                    return ((p['meta'][meta_key]) >= meta_value)
                elif self.input['filter_meta_op'] == "<=":
                    return ((p['meta'][meta_key]) <= meta_value)
                elif self.input['filter_meta_op'] == "<":
                    return ((p['meta'][meta_key]) < meta_value)
                elif self.input['filter_meta_op'] == ">":
                    return ((p['meta'][meta_key]) > meta_value)
                elif self.input['filter_meta_op'] == "!=":
                    return ((p['meta'][meta_key]).lower() != meta_value.lower())
                elif self.input['filter_meta_op'].lower() == "regex":
                    return bool(re.compile(meta_value).match(p['meta'][meta_key]))
                elif self.input['filter_meta_op'].lower() == "daysmax":
                    return bool(target_age_in_seconds / 86400 <= int(meta_value))
                elif self.input['filter_meta_op'].lower() == "minutesmax":
                    return bool(target_age_in_seconds / 60 <= int(meta_value))
                elif self.input['filter_meta_op'].lower() == "daysmin":
                    return bool(target_age_in_seconds / 86400 >= int(meta_value))
                elif self.input['filter_meta_op'].lower() == "minutesmin":
                    return bool(target_age_in_seconds / 60 >= int(meta_value))
                else:
                    return False
            except Exception as e:
                log(e, 'error', title='exception filter_meta')
                return False

        return True

    def _update_save_meta(self, point, save_point={}):
        if self.input['save_meta_key'] is not None:
            save_meta_key = str(self.input['save_meta_key']).lower()
            save_meta_value = self.input['save_meta_value'].lower()

            save_point = {'id': point['id'], 'meta': {}} if len(save_point) < 1 else save_point

            save_point['meta'][save_meta_key] = str(dt.utcnow()) if save_meta_value == "#now#" else save_meta_value

        return save_point

    def _update_save_plant_stage(self, point, save_point={}):
        if self.input['save_plant_stage'] is not None:
            save_plant_stage = str(self.input['save_plant_stage']).lower()
            save_point = {'id': point['id']} if len(save_point) < 1 else save_point

            if save_plant_stage in ('planned', 'planted', 'sprouted', 'harvested'):
                save_point['plant_stage'] = save_plant_stage

                if save_plant_stage == 'planted':
                    save_point['planted_at'] = str(dt.utcnow())
            else:
                log('Wrong save_plant_stage value: {}'.format(save_plant_stage), 'error',
                    title='save_plant_stage')

        return save_point

    def save_plant(self, point):
        try:
            save_point = self._update_save_meta(point)
            save_point = self._update_save_plant_stage(point, save_point)

            if len(save_point) < 2:
                log('Nothing to save: {}'.format(save_point), title='save_plant')
                return

            log('Saving Point: {}'.format(save_point), title='save_plant')

            if Logger.LOGGER_LEVEL < 2:
                endpoint = 'points/{}'.format(save_point['id'])
                app.put(endpoint, payload=save_point)
            else:
                time.sleep(2)
                log('Slept 2s for: {}'.format(save_point), title='save_plant')

        except Exception as e:
            log('Exception thrown: {}'.format(e), 'error', title='save_plant')
            raise e
