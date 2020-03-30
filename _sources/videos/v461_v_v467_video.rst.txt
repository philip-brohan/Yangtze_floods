:orphan:

Weather in China in 1931 - assimilation experiment (video)
==========================================================

Scout 4.6.7 is identical to scout 4.6.1 except that it reduces the assimilation parameter 'relaxation to prior' from 0.9 to 0.7 in the northern hemisphere and the tropics. This increases the power of the observations to reduce the spread in the ensemble, at the cost of reducing the resistance of the reanalysis to model error.

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/397773663?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for and ensemble at new station locations from scout 4.6.1 (left and in blue) and scout 4.6.7 (right and in red).</center></td></tr>
    </table>
    </center>

The blue lines are contours of the individual ensemble members. Black lines are contours of the ensemble mean. The green shading shows the uncertainty in each contour - the amount of shading shows the probability there is a contour at each location (estimated from the reanalysis ensemble). The yellow dots mark pressure observations assimilated while making the field shown. Red dots are additional station pressures assimilated by the scout run only.

The right panel compares the two ensembles at the new :doc:`new stations <../new_stations/new_stations>`: Black lines show the observed pressures, blue dots the scout 4.6.1 ensemble at the station locations, and red dots the scout 4.6.7 ensemble at the station locations. Note that the observations shown include the reanalysis estimates for station bias and height effects (they are calculated from the 'Obfit.post' parameter in the 'psobs_posterior' observation feedback file) - so the 'observations' for the two runs are not necessarily the same (different bias estimates).

The difference between the two scout runs is small.

|

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/videos/v4.6.1_v_v4.6.7/video/plot_comparison.py

Uses scripts and data from the :doc:`new stations <../new_stations/new_stations>`.

To make the video, it is necessary to run the script above thousands of times - giving an image for every 15-minute period. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/videos/v4.6.1_v_v4.6.7/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i v4.6.1_v_v4.6.7/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p \
           -b:v 5M -maxrate 5M -bufsize 20M \
           -c:a copy v4.6.1_v_v4.6.7.mp4
