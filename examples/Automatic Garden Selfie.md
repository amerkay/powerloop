# Automatic Farmbot Garden Selfie

This is a simple example of how to use PowerLoop to photograph all your plants with the least number of waypoints visited to cover the area needed.

### Steps to configure

After you've installed PowerLoop on your device ([see README](README.md)), do the following:

1. Make sure you have a 'Take a photo' sequence.

![Take a photo sequence](http://i.imgur.com/hl6Gk2t.png)

2. Create new sequence with the following parameters:
- Sequences After Move: *Take a photo*
    > Hint: You can change that to a new sequence that runs the Check for Weeds farmware.
- Grid coverage (x, y) per step: *(200, 300)*
- Grid coverage offset (x, y) from center (check your camera's calibration): *(25,25)*

### Expected outcome:

A Selfie consisting of the minimum number of pictures taken.

![Selfie with optimized number of pictures taken](http://i.imgur.com/X3mU555.png)

### Back to [README.md](README.md) for more examples.