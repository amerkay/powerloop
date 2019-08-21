import os
import re
import random

# import static logger and create shortcut function
from logger import Logger
log = Logger.log


class InputStore():
    """ InputStore class to load user input settings or defaults.

    Variables:
        INPUT_DEFAULTS {dict} -- Set of inputs to load and format
            {'variable name': (default value, type), ...}
            Types supported are
                - 'str',
                - 'int' (support 'randint(i,j)'),
                - 'bool'
                - 'list' (.split(",") run on it)

            More info in manifest.json and README
    """

    INPUT_DEFAULTS = {
        'pointname': ('*', 'str'),
        'openfarm_slug': ('*', 'str'),
        'age_min_day': (-1, 'int'),
        'age_max_day': (36500, 'int'),
        'filter_meta_key': ('None', 'str'),
        'filter_meta_op': ('None', 'str'),
        'filter_meta_value': ('None', 'str'),
        'filter_plant_stage': ('None', 'list'),
        'filter_min_x': ('None', 'int'),
        'filter_max_x': ('None', 'int'),
        'filter_min_y': ('None', 'int'),
        'filter_max_y': ('None', 'int'),
        'sequence_init': ('None', 'list'),
        'sequence_beforemove': ('None', 'list'),
        'sequence_aftermove': ('None', 'list'),
        'sequence_end': ('None', 'list'),
        'save_meta_key': ('None', 'str'),
        'save_meta_value': ('None', 'str'),
        'save_plant_stage': ('None', 'str'),
        'offset_x': ('None', 'int'),
        'offset_y': ('None', 'int'),
        'default_z': (0, 'int'),
        'default_speed': (100, 'int'),
        'use_tsp_greedy': (True, 'bool'),
        'grid_coverage_per_step': ('None', 'str'),
        'debug': (1, 'int')
    }

    def __init__(self, farmwarename):
        self.farmwarename = farmwarename
        self.input = {}
        self.get_input_env()

    def get_input_env(self):
        """ Get input variables values. """
        prefix = self.farmwarename.replace('-', '_')
        log('using prefix {}'.format(prefix), 'info', title='get_input_env')

        # get all inputs values
        for key, settings in InputStore.INPUT_DEFAULTS.items():
            self.input[key] = self.get_input_val(key, settings, prefix)

        # special case input: extract (x, y) pair
        self.input['grid_coverage_per_step'] = self.parse_xy_pair(self.input['grid_coverage_per_step'])

        for key, val in self.input.items():
            log('input {}: {}'.format(key, val), title='get_input_env')

    def get_input_val(self, key, settings=('None', 'str'), prefix='farmware'):
        """ Get input values and sanitize them. None values returned for easy checking with 'is None'.

        Arguments:
            key {str} -- the input variable key

        Keyword Arguments:
            settings {tuple} -- default value (None, 0, or input val) and
                type (str, int, bool, list, float) (default: {('None', 'str')})
            prefix {str} -- farmware name prefix (default: {'farmware'})

        Returns:
            mixed types -- based on settings {tuple}
        """

        # get the value set by user or default
        val = os.environ.get('{p}_{k}'.format(p=prefix, k=key), settings[0])

        # remove trailing spaces and convert the value to lower case
        val_clean_str = str(val).lower().strip()

        # set the expected value type for post-processing
        val_type = settings[1] if settings[1] in ['str', 'int', 'bool', 'list', 'float'] else 'str'

        if val_type == 'int':
            return int(self.is_randint(val)) if val_clean_str != 'none' else None
        elif val_type == 'float':
            return float(val) if val_clean_str != 'none' else None
        elif val_type == 'bool':
            return val_clean_str in ['true', '1', 'y', 'yes', 'on']
        elif val_type == 'list':
            return val_clean_str.replace(" , ", ",").replace(", ", ",")\
                .replace(" ,", ",").split(",") if val_clean_str != 'none' else []

        # default treat like str
        return str(val).strip() if val_clean_str != 'none' else None

    def is_randint(self, val):
        """is_randint
        Checks if val is a string, and returns

        Arguments:
            val {str, int} -- str to be parsed, if not instance of string,
            return as is.
        Returns:
            int or object if not instance of str
        """
        if isinstance(val, str):
            # Strip spaces and lowercase if string
            val = val.replace(" ", "").lower()

            if val.startswith("randint("):
                # return the randint result of the parsed range from regex
                m = re.findall(r"randint\((\d+),(\d+)\)", val)
                pos = random.randint(int(m[0][0]), int(m[0][1]))
                pos *= -1 if random.randint(0, 1) else 1
                return pos

        # otherwise, return as is
        return val

    def parse_xy_pair(self, str_in):
        if isinstance(str_in, str):
            # extract (x, y) from input string
            str_in = str_in.replace(" ", "").lower()

            if str_in.lower() == 'none':
                return None

            # find matches using regex
            m = re.findall(r"\((\d+),(\d+)\)", str_in)
            if len(m) > 0 and len(m[0]) == 2:
                # build pair (x, y) and return it
                return (int(m[0][0]), int(m[0][1]))

        # should not reach here if parse correctled, see previous return statement
        log('str_in {} could not be parsed'.format(str_in), title='parse_xy_pair')
        return None

    @staticmethod
    def merge_config(default_config, new_config):
        merged_config = default_config.copy()

        if isinstance(default_config, dict) and isinstance(new_config, dict):
            # merge the input config with self.config, only if key defined.
            for k, v in new_config.items():
                if k in default_config:
                    merged_config[k] = v

            log("configs merged: {}".format(merged_config), title='merge_config')
            return merged_config
        else:
            log("configs must be dicts, instead got {} and {}".format(type(default_config), type(new_config)),
                'error',
                title='merge_config')
            raise Exception('configs must be a dict in merge_config')
