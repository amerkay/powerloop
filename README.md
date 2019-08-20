# [FARMWARE] PowerLoop for Farmbot

Loop your Farmbot by plants with filters, or by automatic waypoint calculation to cover plant search results grid area.

> FARMBOT_OS 6. Tested only on 7.0.1 for now. Should work on 6. Please open an issue with problems with other versions.

> Originally forked from https://github.com/rdegosse/Loop-Plants-With-Filters, thank you @rdegosse!


## PowerLoop's Features

- Load all plants for current device
- Filter plants with Plant name, Openfarm Slug Name, Plant Age in day range, Meta data key/value, Coordinates
- Sort resulting Plants or Grid waypoints using simple sort(x, y), or using Travelling Salesman Greedy Algorithm by setting 'Use Travelling Salesman Problem Greedy algorithm' to 'True'.
- Execute Init list of sequences
- Loop all filtered plants
    - Execute 'Before Move' list of sequences
    - Move to plant coordinate (X,Y) with Offset X, Offset Y, Default Z and Default speed
    - Offset X and Offset Y can be set to randint(i,j) to randomize the X Y offset. One use case is for repetitive tasks like watering seedlings that you don't want to harm with the water pressure.
    - Execute 'After Move' list of sequences
    - Save meta data key/value if required
    - Save plant_stage value if required
- Execute End list of sequences

![Travelling Salesman Solution](tsp_greedy_farmware_screenshot.jpg)
*Fig. 1: Travelling Salesman Solution to filtered list of plants*


## PowerLoop's Input Variables Documentation

[See manifest.json](manifest.json), includes extra "help" key with more information.

## Example usage

> TODO