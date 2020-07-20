'''
This script preprocess the given 360 panorama image under euqirectangular projection
and dump them to the given directory for further layout prediction and visualization.
The script will:
    - extract and dump the vanishing points
    - rotate the equirect image to align with the detected VP
    - extract the VP aligned line segments (for further layout prediction model)
The dump files:
    - `*_VP.txt` is the vanishg points
    - `*_aligned_rgb.png` is the VP aligned RGB image
    - `*_aligned_line.png` is the VP aligned line segments images

Author: Cheng Sun
Email : chengsun@gapp.nthu.edu.tw
Modified By: Aashutosh Pyakurel
Email: aashutosh.pyakurel@gmail.com
'''

import os
import glob
import argparse
import numpy as np
from PIL import Image

from pano_lsd_align import panoEdgeDetection, rotatePanorama


parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
# I/O related arguments
parser.add_argument('--i', required=True,
                    help='NOTE: Remeber to quote your glob path.')
parser.add_argument('--o', required=True)
# Preprocessing related arguments
parser.add_argument('--q_error', default=0.7, type=float)
parser.add_argument('--refine_iter', default=3, type=int)
args = parser.parse_args()

paths = sorted(glob.glob(args.i))
if len(paths) == 0:
    print('no images found')

# Check given path exist
for path in paths:
    assert os.path.isfile(path), '%s not found' % path

# Check target directory
if not os.path.isdir(args.o):
    print('Output directory %s not existed. Create one.')
    os.makedirs(args.o)

# Process each input
for i_path in paths:
    print('Processing', i_path, flush=True)

    # Load and cat input images
    img_ori = np.array(Image.open(i_path))[..., :3]

    # VP detection and line segment extraction
    _, vp, _, _, panoEdge, _, _ = panoEdgeDetection(img_ori,
                                                    qError=args.q_error,
                                                    refineIter=args.refine_iter)
    panoEdge = (panoEdge > 0)

    # Align images with VP
    i_img = rotatePanorama(img_ori / 255.0, vp[2::-1])

    # Dump results
    basename = os.path.splitext(os.path.basename(i_path))[0]
    path = os.path.join(args.o, '%s.jpg' % basename)
    Image.fromarray((i_img * 255).astype(np.uint8)).save(path)
