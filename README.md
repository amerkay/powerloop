# [FARMWARE] PowerLoop for Farmbot

Loop plants with filters, execute sequences and save meta data (FARMBOT_OS 6 minimum, I only tested on v7.0.1 for now).

Forked from https://github.com/rdegosse/Loop-Plants-With-Filters, thank you @rdegosse!


## Features

- Load all plants for current device
- Filter plants with Plant name, Openfarm Slug Name, Plant Age in day range, Meta data key/value, Coordinates
- Sort using simple sort(x, y), or using Travelling Salesman Greedy Algorithm by setting 'Use Travelling Salesman Problem Greedy algorithm' to 'yes'.
- Sort plants by X,Y
- Execute Init Sequences
- Loop all filtered plants
    - Execute 'Before Move' Sequences
    - Move to plant coordinate (X,Y) with Offset X, Offset Y, Default Z and Default speed
    - Offset X and Offset Y can be set to randint(i,j) to randomize the X Y offset. One use case is for repetitive tasks like watering seedlings that you don't want to harm with the water pressure.
    - Execute 'After Move' Sequences
    - Save meta data key/value if required
    - Save plant_stage value if required
- Execute End Sequences

![Travelling Salesman Solution](tsp_greedy_farmware_screenshot.jpg)
*Fig. 1: Travelling Salesman Solution to filtered list of plants*


## Inputs documentation

[See manifest.json](manifest.json), includes extra "help" key with more information.