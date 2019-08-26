# Automatic Farmbot Garden Selfie

This is a simple example of how to use PowerLoop to photograph all your plants with the least number of waypoints visited to cover the area needed.

### Steps to configure

After you've installed PowerLoop on your device ([see README](../README.md)), do the following:

1. Make sure you have a 'Take a photo' sequence.

![Take a photo sequence](http://i.imgur.com/hl6Gk2t.png)
*Fig. 1: Take a photo sequence*

2. Create new sequence with the following parameters:
- Sequences After Move: *Take a photo*
    > Hint: You can use a sequence that runs the 'Weed Detector' farmware.
- Plant name: *\* (or partial plant name to filter by)*
- Grid coverage (x, y) per step: *(230, 300)* (you can check your config by taking a photo and measuring it out on the grid)
- Grid coverage offset (x, y) from center (check your camera's calibration): *(25,25)*
- Grid coverage overlap: 30


### Expected outcome:

A Selfie of only areas with plants.

#### Selfie with overlap=0, choosing only rectangles with plants in them:

![Selfie with overlap=0, choosing only rectangles with plants in them](http://i.imgur.com/7epQ6ja.png)
*Fig. 2: Selfie with overlap=0*

#### Selfie with overlap=30:
Overlap >= 30 automatically switches to using plant radius and covering each plant including once at least.

![Selfie with overlap=30, taking into consideration plant radius](http://i.imgur.com/jpcPl1J.png)
*Fig. 3: Selfie with overlap=30*


#### Back to [README.md](../README.md) for more examples.