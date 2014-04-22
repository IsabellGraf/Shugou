# I've installed the forked version of PIL know as Pillow
# i.e. pip install Pillow
<<<<<<< HEAD
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

'''
This is a basic script to generate all the images needed.
This script should be completely removed by William's work, but this is a guide

The Font will have probably have to be changed
'''
# The shape
for indexshape, shape in enumerate([u"#", u"!", u"*"]):
    # The indexnumber
    for indexnumber, number in enumerate([1, 2, 3]):
        # A replacement for fill
        for indexfontsize, fontsize in enumerate([20, 40, 60]):
            # The colour
            for indexcolor, color in enumerate([(255, 255, 0), (0, 255, 255), (255, 0, 255)]):
                font = ImageFont.truetype(
                    "/usr/local/lib/python3.3/site-packages/kivy/data/fonts/DejaVuSans.ttf", fontsize)
                img = Image.new("RGBA", (200, 100), (200, 200, 200))
                draw = ImageDraw.Draw(img)
                draw.text((0, 0), (shape + " ") * number, color, font=font)
                draw = ImageDraw.Draw(img)
                draw = ImageDraw.Draw(img)
                img.save("images/" + str(indexnumber + 1) + str(indexcolor + 1)
                         + str(indexfontsize + 1) + str(indexshape + 1) + ".png")

for indexshape, shape in enumerate(["★", "█", "●"]):
    # The indexnumber
    for indexnumber, number in enumerate([1, 2, 3]):
        # A replacement for fill
        for indexfontsize, fontsize in enumerate([20, 40, 60]):
            # The colour
            for indexcolor, color in enumerate([(255, 255, 0), (0, 255, 255), (255, 0, 255)]):
                font = ImageFont.truetype(
                    "/usr/local/lib/python3.3/site-packages/kivy/data/fonts/DejaVuSans.ttf", fontsize)
                img = Image.new("RGBA", (200, 100), (120, 20, 20))
                draw = ImageDraw.Draw(img)
                draw.text((0, 0), (shape + " ") * number, color, font=font)
                draw = ImageDraw.Draw(img)
                draw = ImageDraw.Draw(img)
                img.save("images/" + str(indexnumber + 1) + str(indexcolor + 1)
                         + str(indexfontsize + 1) + str(indexshape + 1) + "_down.png")
=======
from PIL import ImageFont, Image, ImageDraw

from Deck import Deck


def make_star(infos, size):
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
    xx = [(d - 0.75 * a, c - 0.3 * a), (d + 0.1 * a, c - a), (d + 0.67 * a, c + a)]
    return xx


def make_square(infos, size):
    a = infos[0] * 0.9 * size
    d = infos[1]
    c = infos[2]
    #xx = [d - a, c - a, d - a, c + a, d + a, c + a, d + a, c - a]
    xx = [(d - 0.6 * a, c - a), (d + a, c - 0.6 * a), (d + 0.6 * a, c + a), (d - a, c + 0.6 * a)]
    return xx


white = (255, 255, 255)
red = (255, 200, 200)

double = 9
smaller = 0.8
colors = {1: (51, 153, 250), 2: (0, 200, 0), 3: (253, 236, 0)}
shapes = {1: make_star, 2: make_square, 3: make_triangle}
# [size, x, y]
numbers = {1: [[double*19, double*31, double*19]], 
           2: [[double*14, double*16.5, double*19], [double*14, double*43.5, double*19]],
           3: [[double*12.5, double*13, double*23], [double*12.5, double*31, double*15], [double*12.5, double*48, double*23]]}


deck = Deck()

for card in deck:
    im1 = Image.new('RGB', (double*62, double*38), white) # normal state
    im2 = Image.new('RGB', (double*62, double*38), red) # down state
    draw1 = ImageDraw.Draw(im1)
    draw2 = ImageDraw.Draw(im2)

    number = numbers[card.number]
    shape = shapes[card.shape]
    color = colors[card.colour]

    for counter,info in enumerate(number): # create 1, 2 or 3 object
        size = smaller
        infovec = list(info) # copying the data
        if card.number == 3 and card.shape == 3:
            infovec[2] = double*19
        if card.number == 3 and card.shape == 2 and counter == 1:
            infovec[1] = double*32.5
        draw1.polygon(shape(infovec, size), fill=color, outline=None)
        draw2.polygon(shape(infovec, size), fill=color, outline=None)

    if card.filling > 1:
        for counter,infos in enumerate(number):
            size=0.7 * smaller
            infovec = list(infos)
            if card.number == 3 and card.shape == 3:
                infovec[2] = double*19
            if card.number == 3 and card.shape == 2 and counter == 1:
                infovec[1] = double*32.5
            draw1.polygon(shape(infovec,size),fill = white, outline = None)
            draw2.polygon(shape(infovec,size),fill = red, outline = None)

    if card.filling > 2:
        for counter,info in enumerate(number):
            size = 0.4 * smaller
            infovec = list(info)
            if card.number == 3 and card.shape == 3:
                infovec[2] = double*19
            if card.number == 3 and card.shape == 2 and counter == 1:
                infovec[1] = double*32.5
            draw1.polygon(
                shape(infovec, size), fill=color, outline=None)
            draw2.polygon(
                shape(infovec, size), fill=color, outline=None)

          
    im1.save(card.normalimage())
    im2.save(card.downimage())
>>>>>>> 43adc1e74be6bdb92702790891521931277ea27d
