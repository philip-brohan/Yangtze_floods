#!/usr/bin/bash

# Split the dragon video into individual frames (png format, to keep the alpha channel)

mkdir -p $SCRATCH/images/Dragon_frames

ffmpeg -i $DATADIR/stock_footage/Dragon_1296362209.mov $SCRATCH/images/Dragon_frames/%04d.png
