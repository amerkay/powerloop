# Smart Watering for Farmbot

With the PowerLoop and Water Doser farmware installed, you can water each plant precisely.

### Check your Farmbot configurations
> Make sure your Farmbot configurations are correct:
> - check camera calibration offset x and y,
> - Photos must align when enabled from the [farm designer](https://my.farm.bot/app/designer/plants) by toggling "Photos" on the right side. To take photos of entire planted area, use PowerLoops with grid_coverage_overlap set to 0. See [Automatic Farmbot Garden Selfie example](Automatic%20Farmbot%20Garden%20Selfie.md)
> - The way to check is to move the Farmbot to the plant location and drop the z axis to plant level and see if the center of the UMT aligns with the center of the plant.

### Steps to configure

1. Install ["PowerLoop"](https://github.com/amerkay/powerloop) AND ["Water Doser"](https://github.com/amerkay/water-doser) farmwares.

2. Create new sequence `Run Water Doser` to execute Farmware `Water Doser` with the default parameters.
> Hint: If you wish to use your own timed watering sequence, skip this step.
![Sequence Run Water Doser](http://i.imgur.com/VM8zBCy.png)

3. Create new sequence `Water all plants` with:
- Execute Sequence: `Pick up watering tool` (your own sequence)
- Excute Farmware `PowerLoop`:
	- Sequences After Move (created in previous step): `Run Water Doser`
	- Filter by meta data key: `last_watering_at`
	- Filter by meta data operator: `minutesmin`
	- Filter by meta data value (2 hours min passed): `120`
	- Save in meta data key: `last_watering_at`
	- Save in meta data value: `#now#`
	- Debug mode: `1`
- Execute Sequence: `Return watering tool` (your own sequence)

4. Test it by saving, and clicking "Test".

### Expected outcome:

Each plant visited in an optimized route, Water Doser is run for each plant and opens water valve the calculated amount. The meta key 'last_water_at' is set for each plant to avoid excessive watering in case of errors.

### Back to [README.md](../README.md) for more examples.