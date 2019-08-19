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

### Filter by plant name (equal/Not case sensitive)
```
{"name": "pointname", "label": "Filter by plant name", "value": "*"}
```
- default : * -> all plant name

### Filter by Openfarm type (equal/Not case sensitive)
```
{"name": "openfarm_slug", "label": "Filter by Openfarm slug name", "value": "*"}
```
- default : * -> all openfarm_slug


### Filter by minimum plant age in days
```
{"name": "age_min_day", "label": "Filter by plant age (minimum days)", "value": "-1"}
```
- default : -1 -> to be sure with time zone and large range..

### Filter by maximum plant age in days
```
{"name": "age_max_day", "label": "Filter by plant age (maximum days)", "value": "36500"}
```
- default : 36500 -> a plant of a century...

### Filter by meta data - KEY
```
{"name": "filter_meta_key", "label": "Filter by meta data : key", "value": "None"}
```
- default : None -> no meta filter

### Filter by meta data - OPERATOR
```
{"name": "filter_meta_op", "label": "Filter by meta data : operator (==,!=,>,<,>=,<=,regex,daysmin,daysmax,minutesmin,minutesmax)", "value": "=="}
```
- default : ==
- ==    : equals (numeric/string)
- !=    : different (numeric/string)
- >     : superior (numeric)
- <     : inferior (numeric)
- >=    : superior or equal (numeric)
- <=    : inferior or equal (numeric)
- regex : regular expression
- daysmin : minimum days number from now to include plant (datetime)
- daysmax : maximum days number from now to include plant (datetime)
- minutesmin : minimum minutes number from now to include plant (datetime)
- minutesmax : maximum minutes number from now to include plant (datetime)

### Filter by meta data - VALUE (Not case sensitive)
```
{"name": "filter_meta_value", "label": "Filter by meta data : value", "value": "None"}
```
- default : None -> no meta filter

### Filter by plant stage
```
{"name": "filter_plant_stage", "label": "Filter by plant stage (none,planned,planted,harvested)", "value": "None"}
```
- none,planned,planted or harvested
- default : None -> no plant_stage filter

### Filter by coordinates - X minimum
```
{"name": "filter_min_x", "label": "Filter by coordinates - Min X", "value": "None"}
```
- default : None -> no coordinates filter

### Filter by coordinates - X maximum
```
{"name": "filter_max_x", "label": "Filter by coordinates - Max X", "value": "None"}
```
- default : None -> no coordinates filter

### Filter by coordinates - Y minimum
```
{"name": "filter_min_y", "label": "Filter by coordinates - Min Y", "value": "None"}
```
- default : None -> no coordinates filter

### Filter by coordinates - Y maximum
```
{"name": "filter_max_y", "label": "Filter by coordinates - Max Y", "value": "None"}
```
- default : None -> no coordinates filter

### Execute sequences one time, on start
```
{"name": "sequence_init", "label": "Init Sequences Name - one time - (multiple: Seq1,Seq2,...)", "value": "None"}
```
- Sequences Name (equal/Not case sensitive)
- Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
- default : None -> no execute sequence

### Execute sequences before each move
```
{"name": "sequence_beforemove", "label": "Sequences Name Before Next Move - for each plant - (multiple: Seq1,Seq2,...)", "value": "None"}
```
- Sequence Name (equal/Not case sensitive)
- Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
- default : None -> no execute sequence

### Execute sequences after each move
```
{"name": "sequence_aftermove", "label": "Sequences Name After Move - for each plant - (multiple: Seq1,Seq2,...)", "value": "None"}
```
- Sequence Name (equal/Not case sensitive)
- Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
- default : None -> no execute sequence

### Execute sequences one time, at the end
```
{"name": "sequence_end", "label": "End Sequences Name - one time - (multiple: Seq1,Seq2,...)", "value": "None"}
```
- Sequence Name (equal/Not case sensitive)
- Can be an ordered list of sequences with , seperator : Seq1,Seq2,...
- default : None -> no execute sequence

### Save meta data after sequence_aftermove - KEY
```
{"name": "save_meta_key", "label": "Save in meta data : key", "value": "None"}
```
- default : None -> no save meta data

### Save meta data after sequence_aftermove - VALUE
```
{"name": "save_meta_value", "label": "Save in meta data : value", "value": "None"}
```
- default : None -> no save meta data

### Save plant stage to
```
{"name": "save_plant_stage", "label": "Set plant stage (none,planned,planted,harvested)", "value": "None"}
```
- Options: planned, planted or harvested
- default : None -> no plant stage change
- /!\ if planted : planted_at property is changed to now utc (like web app)

### Add offset X value to each plant
```
{"name": "offset_x", "label": "Offset X value when moving", "value": 0}
```
- default : 0 -> no offset
- Optional: set to 'randint(i,j)' no quotes, returns a random integer N such that i <= N <= j.

### Add offset Y value to each plant
```
{"name": "offset_y", "label": "Offset Y value when moving", "value": 0}
```
- default : 0 -> no offset
- Optional: set to 'randint(i,j)' no quotes, returns a random integer N such that i <= N <= j.

### Default z axis coordinate when moving
```
{"name": "default_z", "label": "default Z axis value when moving", "value": 0}
```
- default : 0 -> Z axis coordinate

### Default speed when moving
```
{"name": "default_speed", "label": "default speed value when moving", "value": 800}
```
- default : 800 -> default value in celery script

### [NEW] Use Travelling Salesman Greedy algorithm solver
```
{"name": "use_tsp_greedy", "label": "Use Travelling Salesman Problem Greedy algorithm to optimize route? If 'yes', no quotes, TSP Greedy Algorithm will be used", "value": "True"}
```
- Use Travelling Salesman Greedy algorithm solver to optimize route. If 'yes', no quotes, TSP Greedy Algorithm will be used.
- default : True -> use TSPGreedy, rather than sort(x,y)

### [NEW] Grid coverage (x, y) per step
```
  {"name": "grid_coverage_per_step", "label": "Grid coverage (x, y) per step. E.g for camera field of view enter '(200, 280)', no quotes, depending on your z axis height for fov. None to disable grid coverage. If set it uses the results of Plant filtering, then calculates steps based on grid_coverage_per_step value.", "value": "None"},
```
- Grid coverage (x, y) per step. E.g for camera field of view enter '(200, 280)', no quotes, depending on your z axis height for fov. None to disable grid coverage. If set it uses the results of Plant filtering, then calculates steps based on grid_coverage_per_step value.
- default : None -> uses the default plant search and filter for the points data

### Debug level
```
{"name": "debug", "label": "Debug (0-> No FW debug msg, 1-> FW debug msg, 2-> No Move/exec and FW debug msg only)", "value": 1}
```
- debug mode : 0 -> no farmware debug log, 1 -> farmware debug log, 2 -> simulation : no move, no execute sequence, no save meta data AND only farmware debug log
- default : 1 -> move/exec and debug log


