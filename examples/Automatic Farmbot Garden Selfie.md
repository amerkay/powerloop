# Automatic Farmbot Garden Selfie

This is a simple example of how to use PowerLoop to photograph all your plants with the least number of waypoints visited to cover the area needed.

### Steps to configure

After you've installed PowerLoop on your device ([see README](../README.md)), do the following:

1. Make sure you have a 'Take a photo' sequence.

![Take a photo sequence](http://i.imgur.com/hl6Gk2t.png)
*Fig. SP: Take a photo sequence*

2. Create new sequence with the following parameters:
- Sequences After Move: *Take a photo*
    > Hint: You can use a sequence that runs the 'Weed Detector' farmware.
- Plant name: *\* (or partial plant name to filter by)*
- Grid coverage (x, y) per step: *(230, 300)* (you can check your config by taking a photo and measuring it out on the grid)
- Grid coverage offset (x, y) from center (check your camera's calibration): *(25,25)*
- Grid coverage overlap: 30


### Expected outcome:

A Selfie of only areas with plants.

#### Selfie with overlap=0, grid_coverage_summarize = False:

Choosing only rectangles/steps with plants in them (points only):

![Selfie with overlap=0, choosing only rectangles with plants in them](http://i.imgur.com/7epQ6ja.png)
*Fig. P0: Selfie with overlap=0*

#### Selfie with overlap=30, grid_coverage_summarize = True:
Overlap = 30, grid_coverage_summarize = True to enable using plant radius and covering each plant once.

![Selfie with overlap=30, grid_coverage_summarize = True, taking into consideration plant radius](http://i.imgur.com/jpcPl1J.png)
*Fig. P30: Selfie with overlap=30*


#### Back to [README.md](../README.md) for more examples.