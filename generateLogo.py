
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


## initiate ##

imI = Image.new('RGB', (1024, 1024), white)  # normal state
imA = Image.new('RGB', (512, 512), white)  # normal state
drawI = ImageDraw.Draw(imI)
drawA = ImageDraw.Draw(imA)

scale = 0.5


## Android ##

info = [scale*250, scale*370, scale*270]
color = (51, 153, 250)
shape = make_star;
size = 1
drawA.polygon(shape(info, size), fill=color)
size = 0.7
drawA.polygon(shape(info, size), fill=white)
size = 0.4
drawA.polygon(shape(info, size), fill=color)


info = [scale*275, scale*740, scale*600]
color = (0, 200, 0)
shape = make_square
size = 1
drawA.polygon(shape(info, size), fill=color)
size = 0.7
drawA.polygon(shape(info, size), fill=white)

info = [scale*275, scale*280, scale*750]
color = (253, 236, 0)
shape = make_triangle
size = 1
drawA.polygon(shape(info, size), fill=color)

## IOS ##


info = [250, 370, 270]
color = (51, 153, 250)
shape = make_star;
size = 1
drawI.polygon(shape(info, size), fill=color)
size = 0.7
drawI.polygon(shape(info, size), fill=white)
size = 0.4
drawI.polygon(shape(info, size), fill=color)


info = [275, 740, 600]
color = (0, 200, 0)
shape = make_square
size = 1
drawI.polygon(shape(info, size), fill=color)
size = 0.7
drawI.polygon(shape(info, size), fill=white)

info = [275, 280, 750]
color = (253, 236, 0)
shape = make_triangle
size = 1
drawI.polygon(shape(info, size), fill=color)


## save ##

imI.save("images/LogoI.png", dpi=(600,600))
imA.save("images/LogoA2.png", dpi=(600,600))
imA.save("images/LogoA1.png", dpi=(512,512))
imI.save("images/LogoA3.png", dpi=(512,512))
  
