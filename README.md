# Heatmap of Interest
This documentation covers the scripts used to create a person's heatmap of interest (what they find the most and least interesting in their field of view).

### How it Works
To make someone's interest, you need both eyetracking and a measure of their concentration at that point in time. We use SSVEP (Steady State Visually Evoked Potentials) to track when you were particularily stimulated and map that level of stimulation to the (X,Y) position your eyes were looking at. The higher the SSVEP response, the more likely you were focused on that point in the image.

![Result](/src/old/prev_takes/3/result.jpg)

Red points show areas where you looked and were highly stimulated. Dark points show areas where you looked at but weren't highly stimulated. White areas weren't looked at.

After mapping, we squish the 3D array image into a 1D array for the CNC plotter. We segment and average the 1D array by the number of rays we want to plot.

### Steps
1. In muse_MACS.py, assign 'myaddress' to the mac adress of the muse being used. Plug in an occipital electrode to the device.
2. Run flash_img.py to open the pygame window with the flashing image.
3. Run collect.py to start collecting muse data.
4. Run eyetrack.sh to start eye tracking. These must be run in seperate terminals and eyetrack.sh must be run less than 10 sec after collect.py
5. Stare at the image for as long as you'd like (10 min is sufficient). Look around at objects that interest you. If there is food displayed, imagine yourself eating each food.
6. Once done, ctrl-c the eyetrack.sh terminal then ctrl-c the collect.py terminal. It must be done in that order.
7. Run EXODIA.py - the mapped image will appear as data/result.jpg
8. 
