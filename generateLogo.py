
from PIL import ImageFont, Image, ImageDraw

from Deck import Deck
from generateImages import make_star, make_triangle, make_square

white = (255, 255, 255)

im = Image.new('RGB', (1024, 1024), white)  # normal state
draw = ImageDraw.Draw(im)
large, medium, small = 1, 0.7, 0.4
info = [250, 370, 270]
color = (51, 153, 250)
shape = make_star
draw.polygon(shape(info, large), fill=color)
draw.polygon(shape(info, medium), fill=white)
draw.polygon(shape(info, small), fill=color)

info = [275, 740, 600]
color = (0, 200, 0)
shape = make_square
draw.polygon(shape(info, large), fill=color)
draw.polygon(shape(info, medium), fill=white)

info = [275, 280, 750]
color = (253, 236, 0)
shape = make_triangle
draw.polygon(shape(info, large), fill=color)

im.save("images/Logo.png", dpi=(600, 600))
