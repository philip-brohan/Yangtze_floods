#!/usr/bin/bash

# Merge all the dragon frames

./merge_frame_to_background.py --frame=1 > run
for f in {2..197}; do echo ./merge_frame_to_background.py --frame=$f >> run; done
parallel < run
