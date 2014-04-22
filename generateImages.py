# I've installed the forked version of PIL know as Pillow
# i.e. pip install Pillow
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
    a = infos[0] * size
    d = infos[1]
    c = infos[2]
    xx = [(d - 0.2 * a, c - 0.7 * a), (d + 0.75 * a, c + 0.8 * a), (d - a, c)]
    return xx


def make_square(infos, size):
    a = infos[0] * 0.7 * size
    d = infos[1]
    c = infos[2]
    xx = [d - a, c - a, d - a, c + a, d + a, c + a, d + a, c - a]
    return xx


white = (255, 255, 255)
red = (255, 200, 200)

colors = {1: (51, 153, 250), 2: (0, 200, 0), 3: (253, 236, 0)}
shapes = {1: make_star, 2: make_square, 3: make_triangle}
numbers = {1: [[50, 100, 50]], 2: [[40, 50, 50], [40, 150, 50]],
           3: [[35, 37, 60], [35, 100, 40], [35, 162, 60]]}


deck = Deck()

for card in deck:
    im1 = Image.new('RGB', (200, 100), white) # normal state
    im2 = Image.new('RGB', (200, 100), red) # down state
    draw1 = ImageDraw.Draw(im1)
    draw2 = ImageDraw.Draw(im2)

    number = numbers[card.number]
    shape = shapes[card.shape]
    color = colors[card.colour]

    for info in number: # create 1, 2 or 3 object
        size = 1
        infovec = list(info) # copying the data
        if card.number == 3 and card.shape == 3:
            infovec[2] = 50
        draw1.polygon(shape(infovec, size), fill=color, outline=None)
        draw2.polygon(shape(infovec, size), fill=color, outline=None)

    if card.filling > 1:
        for infos in number:
            size=0.7
            infovec = list(infos)
            if card.number == 3 and card.shape == 3:
                infovec[2]=50
            draw1.polygon(shape(infovec,size),fill = white, outline = None)
            draw2.polygon(shape(infovec,size),fill = red, outline = None)

    if card.filling > 2:
        for info in number:
            size = 0.4
            infovec = list(info)
            if card.number == 3 and card.shape == 3:
                infovec[2] = 50
            draw1.polygon(
                shape(infovec, size), fill=color, outline=None)
            draw2.polygon(
                shape(infovec, size), fill=color, outline=None)

          
    im1.save(card.normalimage())
    im2.save(card.downimage())
