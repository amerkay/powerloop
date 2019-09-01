""" SequenceExecutor class

Includes methods for loading the sequence ids and executing the init, before move, after move, end
list of sequences input.

Source: https://github.com/rdegosse/Loop-Plants-With-Filters, thank you @rdegosse!

Variables:
    log {method} -- A reference function Logger().log()
"""

from farmware_tools import app
from farmware_tools import device
from input_store import InputStore

# import static logger and create shortcut function
from logger import Logger

log = Logger.log


class SequenceExecutor:
    # default config
    config = {
        "sequence_init": [],
        "sequence_beforemove": [],
        "sequence_aftermove": [],
        "sequence_end": [],
        "move_offset_x": 0,
        "move_offset_y": 0,
        "move_z": 0,
        "move_speed": 100,
    }

    def __init__(self, farmwarename, config):
        self.farmwarename = farmwarename
        self.config = InputStore.merge_config(self.config, config)
        self.load_sequences_ids()

    def load_sequences_ids(self):
        self.sequences = app.get("sequences")

        self.config["sequence_init_dic"] = {}
        self.config["sequence_beforemove_dic"] = {}
        self.config["sequence_aftermove_dic"] = {}
        self.config["sequence_end_dic"] = {}

        for s in self.sequences:
            for e in self.config["sequence_init"]:
                if str(s["name"]).lower() == e.lower():
                    self.config["sequence_init_dic"][s["name"]] = int(s["id"])
            for e in self.config["sequence_beforemove"]:
                if str(s["name"]).lower() == e.lower():
                    self.config["sequence_beforemove_dic"][s["name"]] = int(s["id"])
            for e in self.config["sequence_aftermove"]:
                if str(s["name"]).lower() == e.lower():
                    self.config["sequence_aftermove_dic"][s["name"]] = int(s["id"])
            for e in self.config["sequence_end"]:
                if str(s["name"]).lower() == e.lower():
                    self.config["sequence_end_dic"][s["name"]] = int(s["id"])

        log(
            "init: {}".format(self.config["sequence_init_dic"]),
            title="load_sequences_id",
        )
        log(
            "before: {}".format(self.config["sequence_beforemove_dic"]),
            title="load_sequences_id",
        )
        log(
            "after: {}".format(self.config["sequence_aftermove_dic"]),
            title="load_sequences_id",
        )
        log(
            "end: {}".format(self.config["sequence_end_dic"]), title="load_sequences_id"
        )

    def execute_sequence_init(self):
        if len(self.config["sequence_init_dic"]) != 0:
            for s in self.config["sequence_init_dic"]:
                log(
                    "Execute Sequence: {} id: {}".format(
                        s, self.config["sequence_init_dic"][s]
                    ),
                    title="execute_sequence_init",
                )
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(sequence_id=self.config["sequence_init_dic"][s])
        else:
            log("Nothing to execute", title="execute_sequence_init")

    def execute_sequence_before(self):
        if len(self.config["sequence_beforemove_dic"]) != 0:
            for s in self.config["sequence_beforemove_dic"]:
                log(
                    "Execute Sequence: {} id: {}".format(
                        s, self.config["sequence_beforemove_dic"][s]
                    ),
                    title="execute_sequence_before",
                )
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(
                        sequence_id=self.config["sequence_beforemove_dic"][s]
                    )
        else:
            log("Nothing to execute", title="execute_sequence_before")

    def execute_sequence_after(self):
        if len(self.config["sequence_aftermove_dic"]) != 0:
            for s in self.config["sequence_aftermove_dic"]:
                log(
                    "Execute Sequence: {} id: {}".format(
                        s, self.config["sequence_aftermove_dic"][s]
                    ),
                    title="execute_sequence_after",
                )
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(sequence_id=self.config["sequence_aftermove_dic"][s])
        else:
            log("Nothing to execute", title="execute_sequence_after")

    def execute_sequence_end(self):
        if len(self.config["sequence_end_dic"]) != 0:
            for s in self.config["sequence_end_dic"]:
                log(
                    "Execute Sequence: {} id: {}".format(
                        s, self.config["sequence_end_dic"][s]
                    ),
                    title="execute_sequence_end",
                )
                if Logger.LOGGER_LEVEL < 2:
                    device.execute(sequence_id=self.config["sequence_end_dic"][s])
        else:
            log("Nothing to execute", title="execute_sequence_end")

    def move_absolute_point(self, point):
        move_offset_x = (
            0 if self.config["move_offset_x"] is None else self.config["move_offset_x"]
        )
        move_offset_y = (
            0 if self.config["move_offset_y"] is None else self.config["move_offset_y"]
        )
        move_z = 0 if self.config["move_z"] is None else self.config["move_z"]

        point_desc = (
            "{} of type {}".format(point["name"], point["pointer_type"])
            if "name" in point
            else ""
        )

        log(
            "Move absolute to {} ({}, {}) with offset ({}, {}) and move_z {}".format(
                point_desc, point["x"], point["y"], move_offset_x, move_offset_y, move_z
            ),
            title="move_absolute_point",
        )

        if Logger.LOGGER_LEVEL < 2:
            device.move_absolute(
                location=device.assemble_coordinate(point["x"], point["y"], move_z),
                offset=device.assemble_coordinate(move_offset_x, move_offset_y, 0),
                speed=self.config["move_speed"],
            )
