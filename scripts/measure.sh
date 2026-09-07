#!/bin/bash
rm -f p-*.png
pdftoppm -r 60 -png "$1" p
python3 -c "
from PIL import Image
import glob
for f in sorted(glob.glob('p-*.png')):
  im=Image.open(f).convert('L');w,h=im.size;px=im.load();last=0
  for y in range(h):
    if min(px[x,y] for x in range(0,w,2))<230: last=y
  print(f,'%.0f%% = %.2f in'%(100*last/h,11*last/h))"
