:orphan:

Weather in China in 1931 - new stations (video)
===============================================

20CR version 3 assimilates very few observations over China. Scout 4.6.1 is identical to version 3 except that it assimilates additional observations from about 40 :doc:`new stations <../new_stations/new_stations>` - so it should be more accurate and more precise.

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/397628442?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for and ensemble at new station locations from 20CRv3 (left and in blue) and scout 4.6.1 (right and in red).</center></td></tr>
    </table>
    </center>

The blue lines are contours of the individual ensemble members. Black lines are contours of the ensemble mean. The green shading shows the uncertainty in each contour - the amount of shading shows the probability there is a contour at each location (estimated from the reanalysis ensemble). The yellow dots mark pressure observations assimilated while making the field shown. Red dots are additional station pressures assimilated by the scout run only.

The right panel compares the two ensembles at the new :doc:`new stations <../new_stations/new_stations>`: Black lines show the observed pressures, blue dots the original 20CRv3 ensemble at the station locations, and red dots the 20CR ensemble after assimilating all the observations except the observation at that location. Note that the observations shown include the reanalysis estimates for station bias and height effects (they are calculated from the 'Obfit.post' parameter in the 'psobs_posterior' observation feedback file).

Version 3 does very well considering there are so few observations over China. This means that there is limited opportunity for improvement. Even so, scout 4.6.1, assimilating about 40 additional once-daily station observations has a better fit to those new observations, and a smaller ensemble spread.

|

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/videos/v3_v_v4.6.1/video/plot_comparison.py

Uses scripts and data from the :doc:`new stations <../new_stations/new_stations>`.

To make the video, it is necessary to run the script above thousands of times - giving an image for every 15-minute period. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/videos/v3_v_v4.6.1/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i v3_v_v4.6.1/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p \
           -b:v 5M -maxrate 5M -bufsize 20M \
           -c:a copy v3_v_v4.6.1.mp4
