""" SequenceExecutor class

Includes methods for loading the sequence ids and executing the init, before move, after move, end
list of sequences input.

Source: https://github.com/rdegosse/Loop-Plants-With-Filters, thank you @rdegosse!

Variables:
    log {method} -- A reference function Logger().log()
"""

from farmware_tools import app
from farmware_tools import device

# import static logger and create shortcut function
from logger import Logger
log = Logger.log


class SequenceExecutor():
    def __init__(self, farmwarename, input_store):
        self.farmwarename = farmwarename
        self.input_store = input_store
        self.input = input_store.input
        self.load_sequences_ids()

    def load_sequences_ids(self):
        self.sequences = app.get('sequences')

        self.input['sequence_init_dic'] = {}
        self.input['sequence_beforemove_dic'] = {}
        self.input['sequence_aftermove_dic'] = {}
        self.input['sequence_end_dic'] = {}

        for s in self.sequences:
            for e in self.input['sequence_init']:
                if str(s['name']).lower() == e.lower():
                    self.input['sequence_init_dic'][s['name']] = int(s['id'])
            for e in self.input['sequence_beforemove']:
                if str(s['name']).lower() == e.lower():
                    self.input['sequence_beforemove_dic'][s['name']] = int(s['id'])
            for e in self.input['sequence_aftermove']:
                if str(s['name']).lower() == e.lower():
                    self.input['sequence_aftermove_dic'][s['name']] = int(s['id'])
            for e in self.input['sequence_end']:
                if str(s['name']).lower() == e.lower():
                    self.input['sequence_end_dic'][s['name']] = int(s['id'])

        log('init: {}'.format(self.input['sequence_init_dic']), title='load_sequences_id')
        log('before: {}'.format(self.input['sequence_beforemove_dic']), title='load_sequences_id')
        log('after: {}'.format(self.input['sequence_aftermove_dic']), title='load_sequences_id')
        log('end: {}'.format(self.input['sequence_end_dic']), title='load_sequences_id')

    def execute_sequence_init(self):
        if len(self.input['sequence_init_dic']) != 0:
            for s in self.input['sequence_init_dic']:
                log('Execute Sequence: {} id: {}'.format(s, self.input['sequence_init_dic'][s]),
                    title='execute_sequence_init')
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(sequence_id=self.input['sequence_init_dic'][s])
        else:
            log('Nothing to execute', title='execute_sequence_init')

    def execute_sequence_before(self):
        if len(self.input['sequence_beforemove_dic']) != 0:
            for s in self.input['sequence_beforemove_dic']:
                log('Execute Sequence: {} id: {}'.format(s, self.input['sequence_beforemove_dic'][s]),
                    title='execute_sequence_before')
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(sequence_id=self.input['sequence_beforemove_dic'][s])
        else:
            log('Nothing to execute', title='execute_sequence_before')

    def execute_sequence_after(self):
        if len(self.input['sequence_aftermove_dic']) != 0:
            for s in self.input['sequence_aftermove_dic']:
                log('Execute Sequence: {} id: {}'.format(s, self.input['sequence_aftermove_dic'][s]),
                    title='execute_sequence_after')
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(sequence_id=self.input['sequence_aftermove_dic'][s])
        else:
            log('Nothing to execute', title='execute_sequence_after')

    def execute_sequence_end(self):
        if len(self.input['sequence_end_dic']) != 0:
            for s in self.input['sequence_end_dic']:
                log('Execute Sequence: {} id: {}'.format(s, self.input['sequence_end_dic'][s]),
                    title='execute_sequence_end')
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(sequence_id=self.input['sequence_end_dic'][s])
        else:
            log('Nothing to execute', title='execute_sequence_end')

    def move_absolute_point(self, point):
        offset_x = 0 if self.input['offset_x'] is None else self.input['offset_x']
        offset_y = 0 if self.input['offset_y'] is None else self.input['offset_y']
        default_z = 0 if self.input['default_z'] is None else self.input['default_z']

        point_desc = '{} of type {}'.format(point['name'], point['pointer_type']) if 'name' in point else ''

        log('Move absolute to {} ({}, {}) with offset ({}, {}) and default_z {}'.format(
            point_desc, point['x'], point['y'], offset_x, offset_y, default_z
        ), title='move_absolute_point')

        if Logger.LOGGER_LEVEL < 2:
            device.move_absolute(location=device.assemble_coordinate(point['x'], point['y'], default_z),
                                 offset=device.assemble_coordinate(offset_x, offset_y, 0),
                                 speed=self.input['default_speed'])
