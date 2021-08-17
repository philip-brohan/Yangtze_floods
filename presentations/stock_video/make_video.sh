#!/usr/bin/bash

# Make video from merged frames

ffmpeg -r 24 -pattern_type glob -i $SCRATCH/images/Dragon_merged/\*.jpg \
       -c:v libx264 -threads 4 -preset veryslow -tune film \
       -profile:v high -level 4.2 -pix_fmt yuv420p -b:v 5M \
       -maxrate 15M -bufsize 5M -c:a copy $SCRATCH/images/Dragon.mp4
