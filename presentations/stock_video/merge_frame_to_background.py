#!/usr/bin/env python

# Composite the foreground parts of the dragon video onto the fixed background image

import os
from PIL import Image, ImageFilter
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--frame", help="Frame number", type=int, required=True)
args = parser.parse_args()


# Get the background image
bkg = Image.open("./PPT_bkg.jpg")

# Get the Dragon frame
frm = Image.open(
    "%s/images/Dragon_frames/%04d.png" % (os.getenv("SCRATCH"), args.frame)
)

# Full size background, smaller dragon
bkg = bkg.resize((1920, 1080))
frm = frm.resize((1024, 768))

# Make the dragon's shadow
frs = frm.copy().convert("RGBA")
pixdata = frs.load()
width, height = frs.size
for y in range(height):
    for x in range(width):
        pixdata[x, y] = (0, 0, 0, int(pixdata[x, y][3] / 3))
frs = frs.filter(ImageFilter.BoxBlur(10))
bkg.paste(frs, (args.frame*2 - 120 + 100, 100), frs)

# Merge the dragon onto the background
bkg.paste(frm, (args.frame*2 - 120, 0), frm)

# Save the merged image
opn = "%s/images/Dragon_merged/%04d.jpg" % (os.getenv("SCRATCH"), args.frame)
if not os.path.isdir(os.path.dirname(opn)):
    os.makedirs(os.path.dirname(opn))

bkg.save(opn)
