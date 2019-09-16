# [FARMWARE] PowerLoop for Farmbot

Loop your Farmbot by plants with filters, or by automatic waypoint calculation to cover plant search results grid area.

> Originally forked from [Loop-Plants-With-Filters](https://github.com/rdegosse/Loop-Plants-With-Filters), thank you @rdegosse!

![Selfie with overlap=30, taking into consideration plant radius](http://i.imgur.com/jpcPl1J.png)
*Fig. P30: [PowerLoop taking a Selfie](./examples/Automatic%20Farmbot%20Garden%20Selfie.md) of my Farmbot garden, automatically choosing steps where the photos includes plants (with their radius), excluding empty shots*

## Installation

#### For Farmbot OS 8 ***(new)***
Go to [My Farmbot -> Farmware](https://my.farm.bot/app/farmware/), then paste the manifest.json path to install:
```
https://raw.githubusercontent.com/amerkay/powerloop/master/manifest_v2.json
```

> Please report bugs using the [issues tab](../../issues/).


#### For Farmbot OS 6 and 7
Go to [My Farmbot -> Farmware](https://my.farm.bot/app/farmware/), then paste the manifest.json path to install:
```
https://raw.githubusercontent.com/amerkay/powerloop/master/manifest.json
```

## Developers

I tried to add as much comments and documentation within the files, as well as clear variable and method naming. If you want to use one of the files in your own project, I made sure they are as self-contained and documented as possible. Please use freely. Pull requests appreciated - even if it takes me time to get to it.

## PowerLoop's Features

- Load all plants for current device from Farmbot API.

- Filter plants by plant name, Openfarm slug, age in day range. meta data key/value, and coordinates. [See manifest.json](manifest.json).

- Sort resulting plants or Grid waypoints using simple sort(x, y), or using Travelling Salesman Greedy Algorithm by setting 'Use Travelling Salesman Problem Greedy algorithm' to 'True'.

- Calculate grid coverage waypoints, using (optionally filtered) plant list as input. This is useful when you want to scan your garden with multiple photos or run the deweeding algorithm. See examples section.

- Execute list of sequences (initial, before each move, after each move, end).

- Offset X and Offset Y for each move. Can be set to `randint(i,j)` to randomize the X Y offset. One use case is for repetitive tasks like watering seedlings that you don't want to harm with the water pressure, e.g set offset `randint(-20,20)` to randomize movement by +/- 2cm.

- Loop all filtered plants
    - Move to plant coordinate (X, Y) with offset X, offset Y, default Z and default speed
    - Save meta data key/value, if set
    - Save plant_stage value, if set
    - Runs before and after list of sequences, if set

- Uses official [farmware_tools](https://github.com/FarmBot-Labs/farmware-tools) to contact Farmbot API and control device.

- Uses concurrent task executor to save meta data to API, to save time executing each move. More about [concurrent.futures.ProcessPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html) at Python docs.


## PowerLoop's Input Variables Documentation

[See manifest.json](manifest.json), includes extra "help" key with more information.

## Example 1: [Automatic Farmbot Garden Selfie](./examples/Automatic%20Farmbot%20Garden%20Selfie.md)

Automate taking photos/weed detecion of your plants with the least number of waypoints to visit. You can run it in two different modes: basic and summary. [Tutorial here](./examples/Automatic%20Farmbot%20Garden%20Selfie.md).

#### Basic grid coverage with grid_coverage_summarize = False, only uses the plant's point (no radius)

![Selfie with overlap=0, grid_coverage_summarize = False, excluding any steps that cover no plant points](http://i.imgur.com/oetvubR.png)
*Fig. ST0: Selfie with coverage area=(400,400), grid_coverage_summarize = False, and overlap=0. Python test file output with matplotlib. See /test/ directory*

#### Summary grid coverage with grid_coverage_summarize = True, takes plant radius into consideration

![Selfie with overlap=30, grid_coverage_summarize = True, taking into consideration each plant's radius](http://i.imgur.com/rnHEVJ1.png)
*Fig. ST30: Selfie with coverage area=(400,400), grid_coverage_summarize = True, and overlap=30. Python test file output with matplotlib. See /test/ directory*


## Example 2: [Water all Farmbot plants](./examples/Smart%20Watering%20for%20Farmbot.md) using 'Water Doser' farmware

["Water Doser"](https://github.com/amerkay/water-doser) farmware automatically calculate how many seconds to water each plant individually based on it's age and maximum spread from OpenFarm data. Can be run independantly, as it guesses which plant the farmbot is on top of automatically if configured correctly.
Alternatively, you can have your own watering sequence. [Tutorial here](./examples/Smart%20Watering%20for%20Farmbot.md)

![Travelling Salesman Solution](tsp_greedy_farmware_screenshot.jpg)
*Fig. TSP: Travelling Salesman Solution for moving between the resulting filtered list of plants (default behavior)*

## More examples and notes:

- [Calibrating Farmbot Camera for precision](./examples/Calibrating%20Farmbot%20Camera%20for%20precision.md), with an example on how to setup to shoot weeds with the water output (without the watering tool).