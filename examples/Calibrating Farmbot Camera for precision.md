# Calibrating Farmbot (camera settings) for precision

> Note: This is untested, just my notes to get it to shoot precisely at a certain spot.

## Camera Calibration & shooting weeds with water

So, I went off documentation for the calibration, instead of calibrating to (0,0), I calibrated for the center of the UTM to be above the picture taken from z = 0.

To do so:
1. Before you start, make sure your farmbot is operating properly, and the axis are calibrated/homed.

2. Reset the camera calibration to 0's ![Reset Camera Calibration](http://i.imgur.com/rtf7YNI.png)

3. Calibrate, this should set up the rotation and pixel values for your setup.

4. Make sure you set "Origin Location in Image" to correct value. See [Farmbot camera calibration documentation](https://software.farm.bot/docs/camera-calibration).
![Successful calibration](http://i.imgur.com/nU43uXC.png)

5. Take a photo at Z=0.

6. Then use the [Farmbot Designer Move Mode](https://my.farmbot.io/app/designer/move_to) to move right above your calibration red object. Drop to Z=-400 (or just 100mm less than the max for your setup).
![Move to one of the calibration red objects](http://i.imgur.com/baP0jVa.png)

7. The center of the Universal Mount Tool (UMT) should align with the target object, be right above it. I used the Soil Sensor to check, as it's almost centered.
If it does not align, change the Camera Offset X/Y till it does. Notice, **my offset it 25x25mm.**
Each time going back to Z=0, taking a photo, repeating steps 5-7.
![Aligned](https://i.imgur.com/p3L0y10.jpg)

## Shooting Weeds Sequence

The idea here is to use the water nozel (high pressure 100ml/sec on my setup, ***without*** watering tool mounting).

> The nozel is at offset (x +9mm, y -15mm) from UTM Center according to Genesis v1.4 [UTM 3D model](https://sketchfab.com/3d-models/farmbot-genesis-v10-utm-cover-692c30a1e71a4f1791a0c8058342b1dc).

Now, you can shoot weeds at specific X, Y coordinates with the water stream. Use the "Move mode" to set an X and move to weed center, then run the following sequence.

![Shoot Weeds Sequence](http://i.imgur.com/O2VLFLG.png)

#### Back to [README.md](../README.md) for more examples.