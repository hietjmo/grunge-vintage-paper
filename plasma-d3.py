
# plasma.py
# plasma fractal
# FB - 201003147
# https://code.activestate.com/recipes/577113-plasma-fractal-using-python-image-library/

from PIL import Image
from collections import defaultdict
import math
import random
import time

start = time.time()
# image size
w = 720
h = 720
img = defaultdict (lambda: 0)
# roughness = random.randint(2, 5)
roughness = 2

def adjust(xa, ya, x, y, xb, yb):
  global img
  if (img[(x,y)] == 0):
    d=math.fabs(xa-xb) + math.fabs(ya-yb)
    v=(img[(xa,ya)] + img[(xb,yb)])/2.0 \
     + (random.random()-0.5) * d * roughness
    c=int(math.fabs(v) % 256)
    img[(x,y)] = c

def subdivide(x1, y1, x2, y2):
  global img
  if (not((x2-x1 < 2.0) and (y2-y1 < 2.0))):
    x=int((x1 + x2)/2.0)
    y=int((y1 + y2)/2.0)
    adjust(x1,y1,x,y1,x2,y1)
    adjust(x2,y1,x2,y,x2,y2)
    adjust(x1,y2,x,y2,x2,y2)
    adjust(x1,y1,x1,y,x1,y2)
    if (img[(x,y)] == 0):
      v=int((img[(x1,y1)] + img[(x2,y1)] 
         + img[(x2,y2)] + img[(x1,y2)])/4.0)
      img[(x,y)] = v

    subdivide(x1,y1,x,y)
    subdivide(x,y1,x2,y)
    subdivide(x,y,x2,y2)
    subdivide(x1,y,x,y2)

img[(0,0)] = random.randint(0, 255)
img[(w-1,0)] = random.randint(0, 255)
img[(w-1,h-1)] = random.randint(0, 255)
img[(0,h-1)] = random.randint(0, 255)
subdivide(0,0,w-1,h-1)

end = time.time()
tid = end - start
print (f"{tid:.4f} s")

# print (img)
start = time.time()

dark   = (196,170,143)
bright = (236,227,217)

def gradient (c):
  return (
   int(dark[0] + (c/255) * (bright[0]-dark[0])),
   int(dark[1] + (c/255) * (bright[1]-dark[1])),
   int(dark[2] + (c/255) * (bright[2]-dark[2])))

image = Image.new("RGB", (w, h))
for x in range (0,w):
  for y in range (0,h):
    image.putpixel((x,y), gradient(img[(x,y)]))
number = random.randint (1,99999)
image.save(f"plasma-{roughness}-{number}.png", "PNG")
end = time.time()
tid = end - start
print (f"{tid:.4f} s")



