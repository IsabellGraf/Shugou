
from PIL import ImageFont, Image, ImageDraw

from Deck import Deck


def make_star(infos,size):
    d = infos[1]
    c = infos[2]
    a = infos[0] * size
    b = 0.5 * infos[0] * size
    xx = [(d, c - b), (d - 0.5 * a, c - 0.866 * a),
          (d - 0.866 * b, c - 0.5 * b), (d - a, c),
          (d - 0.866 * b, c + 0.5 * b), (d - 0.5 * a, c + 0.866 * a),
          (d, c + b), (d + 0.5 * a, c + 0.866 * a),
          (d + 0.866 * b, c + 0.5 * b), (d + a, c),
          (d + 0.866 * b, c - 0.5 * b), (d + 0.5 * a, c - 0.866 * a)]
    return xx


def make_triangle(infos, size):
    a = infos[0] * 0.95 * size
    d = infos[1]
    c = infos[2]
    xx = [(d - 0.75 * a, c - 0.3 * a),
          (d + 0.1 * a, c - a), (d + 0.67 * a, c + a)]
    return xx


def make_square(infos, size):
    a = infos[0] * 0.9 * size
    d = infos[1]
    c = infos[2]
    xx = [(d,c-a), (d+0.8*a,c),(d,c+a),(d-0.8*a,c)]
    return xx


white = (255, 255, 255)



im = Image.new('RGB', (1024, 1024), white)  # normal state
draw = ImageDraw.Draw(im)


info = [250, 370, 270]
color = (51, 153, 250)
shape = make_star;
size = 1
draw.polygon(shape(info, size), fill=color)
size = 0.7
draw.polygon(shape(info, size), fill=white)
size = 0.4
draw.polygon(shape(info, size), fill=color)


info = [275, 740, 600]
color = (0, 200, 0)
shape = make_square
size = 1
draw.polygon(shape(info, size), fill=color)
size = 0.7
draw.polygon(shape(info, size), fill=white)

info = [275, 280, 750]
color = (253, 236, 0)
shape = make_triangle
size = 1
draw.polygon(shape(info, size), fill=color)




im.save("images/Logo.png", dpi=(600,600))
  
