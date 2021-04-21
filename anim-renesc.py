
# https://code.activestate.com/recipes/577113-plasma-fractal-using-python-image-library/

# time python anim-renesc.py -fr 2750
# real	86m8,393s

# ffmpeg -y -framerate 25 -i frames2/frame-%06d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p vanha-paperi-2.mp4

from PIL import Image
from collections import defaultdict
import math
import random
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-fr','--frames',type=int,default=600)
parser.add_argument('-sp','--speed',type=float,default=7.0)

parser.add_argument('-w','--width',type=int,default=1280)
parser.add_argument('-ht','--height',type=int,default=720)

parser.add_argument('-d','--folder',default='frames')
parser.add_argument('-st','--style',type=int,default=1)

args = parser.parse_args()

frames = args.frames
speed = args.speed
style = args.style

rec_w = args.width
rec_h = args.height

def nextSq (x):
  return 2 ** (math.floor (math.log2 (x)) + 1) 

sq_h = nextSq (rec_h) + 1
sq_w = sq_h
print ("sq_h=",sq_h)
folder = args.folder

if not os.path.exists (folder):
  os.makedirs (folder)

"""
frames = 1000
speed = 7.0

rec_w = 1280
rec_h = 720
sq_w = 1025
sq_h = 1025
"""

number = random.randint (1,99999)
after_run = f"ffmpeg -y -framerate 25 -i {folder}/frame-%09d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p old-paper-{number}.mp4"
avail_x1,avail_x2 = 0,0
big = defaultdict (lambda: 0)
sq = defaultdict (lambda: 0)
image = Image.new ("RGB", (rec_w, rec_h))
# roughness = random.randint(2, 5)
roughness = 2

def adjust (xa, ya, x, y, xb, yb):
  global sq
  if (sq [(x,y)] == 0):
    d = math.fabs (xa-xb) + math.fabs (ya-yb)
    v = (sq[(xa,ya)] + sq[(xb,yb)])/2.0 \
      + (random.random()-0.5) * d * roughness
    c = int(math.fabs (v) % 256)
    sq [(x,y)] = c

def subdivide (x1, y1, x2, y2):
  global sq
  if (not((x2-x1 < 2.0) and (y2-y1 < 2.0))):
    x=int((x1 + x2)/2.0)
    y=int((y1 + y2)/2.0)
    adjust(x1,y1,x,y1,x2,y1)
    adjust(x2,y1,x2,y,x2,y2)
    adjust(x1,y2,x,y2,x2,y2)
    adjust(x1,y1,x1,y,x1,y2)
    if (sq[(x,y)] == 0):
      v=int((sq[(x1,y1)] + sq[(x2,y1)] 
         + sq[(x2,y2)] + sq[(x1,y2)])/4.0)
      sq[(x,y)] = v

    subdivide(x1,y1,x,y)
    subdivide(x,y1,x2,y)
    subdivide(x,y,x2,y2)
    subdivide(x1,y,x,y2)

def first_gen ():
  global sq
  sq[(0,0)] = random.randint(0, 255)
  sq[(sq_w-1,0)] = random.randint(0, 255)
  sq[(sq_w-1,sq_h-1)] = random.randint(0, 255)
  sq[(0,sq_h-1)] = random.randint(0, 255)
  subdivide(0,0,sq_w-1,sq_h-1)

if style == 1:
  dark   = (196,170,143) # brownie
  bright = (236,227,217) # brownie
elif style == 2:
  dark   = (212,142,101) # renesc
  bright = (250,234,202) # renesc
else:
  dark   = (0,0,0)       # black/
  bright = (255,255,255) # white

def new_gen ():
  global sq
  # print ("newgen")
  border = []
  for y in range (0,sq_h):
    border.append (sq [(sq_w-1,y)])
  sq = defaultdict (lambda: 0)
  for y in range (0,sq_h):
    sq [(0,y)] = border [y]
  sq [(sq_w-1,0)]      = random.randint (0, 255)
  sq [(sq_w-1,sq_h-1)] = random.randint (0, 255)
  subdivide (0,0,sq_w-1,sq_h-1)

def gradient (c):
  return (
   int(dark[0] + (c/255) * (bright[0]-dark[0])),
   int(dark[1] + (c/255) * (bright[1]-dark[1])),
   int(dark[2] + (c/255) * (bright[2]-dark[2])))

def add_to_big ():
  global sq, big, avail_x1, avail_x2
  for x in range (0,sq_w-1):
    # print(avail_x2+x, end=" ")
    for y in range (0,sq_h):
      big [(avail_x2+x,y)] = sq [(x+1,y)]
  avail_x2 += sq_w-1
  # print ("avail_x1=",avail_x1,"avail_x2=",avail_x2)

def make_frame (start_x,big):
  global image
  for x in range (0,rec_w):
    for y in range (0,rec_h):
      image.putpixel ((x,y), 
        gradient (big [(start_x+x,y)]))

print ("\nWhen the frames are ready, run:\n")
print (f"{after_run}\n")

first_gen ()
add_to_big ()

for frame in range (0,frames):
  print ("frame =",frame)
  start_x = frame * speed
  stop_x = start_x + rec_w
  while stop_x > avail_x2:
    new_gen ()
    add_to_big ()
  make_frame (start_x,big)

  image.save(f"{folder}/frame-" + str(frame).zfill(9) + ".png", 
    "PNG")

print ("\nNow run:\n")
print (f"{after_run}\n")

