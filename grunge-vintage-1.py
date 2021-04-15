
import cairo
import random
from math import sin,cos,sqrt,tau,floor

text = "Old Grunge Vintage Paper Test"

w_pic, h_pic = 1280,720
w,h = 1240,680

def draw_point2 (pt):
  x,y = pt
  ct.arc (x,y,3,0,tau)
  ct.set_source_rgba (0, 0, 0, 0.05)
  ct.fill ()

def draw_point (pt):
  (x,y) = pt
  draw_point2 ((3.5*x+20,h-3.5*y))

surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
ct = cairo.Context (surface)
ct.rectangle (0, 0, w_pic, h_pic)
ct.set_source_rgb (1.00, 1.00, 1.00)
ct.fill()

for i in range (3000):
  draw_point ((random.randint(0,355),random.randint(0,180)))

ct.set_source_rgba (0.1, 0.1, 0.1, 0.7)
    
ct.select_font_face("Averia Serif GWF", cairo.FONT_SLANT_NORMAL, 
    cairo.FONT_WEIGHT_NORMAL)
ct.set_font_size(64)

(x, y, width, height, dx, dy) = ct.text_extents (text)
tx,ty = w/2 - width/2 + 20, h/2 + 20
ct.move_to (tx,ty) 
ct.show_text (text)

pngfile = "grunge-vintage-1.png"
surface.write_to_png (pngfile)

