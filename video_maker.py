import os
import glob
import argparse
import cv2
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--i', required=True,
                    help='NOTE: Remeber to quote your glob path.')
parser.add_argument('--o', required=True)
args = parser.parse_args()
paths = sorted(glob.glob(args.i))
if len(paths) == 0:
    print('no images found')
img_arr = []
for path in paths:
	img_arr.append(cv2.imread(path))
	print("Read %s"%path)

out = cv2.VideoWriter(os.path.join(args.o),
					cv2.VideoWriter_fourcc(*'DIVX'),
					30, 
					(3840,1920))
count  = 0
for i in img_arr:
	out.write(i)
	print("Completed %d"%count)
	count = count + 1
out.release()
