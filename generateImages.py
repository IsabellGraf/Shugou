# To run the file you must first install the Pillow module
# i.e. pip install Pillow or pip3 install Pillow

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
    xx = [(d - 0.75 * a, c - 0.3 * a),
          (d + 0.1 * a, c - a), (d + 0.67 * a, c + a)]
    return xx


def make_square(infos, size):
    a = infos[0] * 0.9 * size
    d = infos[1]
    c = infos[2]
    #xx = [d - a, c - a, d - a, c + a, d + a, c + a, d + a, c - a]
    xx = [(d - 0.6 * a, c - a), (d + a, c - 0.6 * a),
          (d + 0.6 * a, c + a), (d - a, c + 0.6 * a)]
    return xx


white = (255, 255, 255)
red = (255, 200, 200)

# A factor that creates a much larger image that is much larger than needed
# It is scalled back down later on, this greatly improves the image quality.
double = 9
# How the scalling occurs
smaller = 0.8
colors = {1: (51, 153, 250), 2: (0, 200, 0), 3: (253, 236, 0)}
shapes = {1: make_star, 2: make_square, 3: make_triangle}
# [size, x, y]
numbers = {1: [[double * 19, double * 31, double * 19]],
           2: [[double * 14, double * 16.5, double * 19],
              [double * 14, double * 43.5, double * 19]],
           3: [[double * 12.5, double * 13, double * 23], 
              [double * 12.5, double * 31, double * 15],
              [double * 12.5, double * 48, double * 23]]}


deck = Deck()

for card in deck:
    im1 = Image.new('RGB', (double * 62, double * 38), white)  # normal state
    im2 = Image.new('RGB', (double * 62, double * 38), red)  # down state
    draw1 = ImageDraw.Draw(im1)
    draw2 = ImageDraw.Draw(im2)

    number = numbers[card.number]
    shape = shapes[card.shape]
    color = colors[card.colour]

    # There is 3 types of fillings, they are doen by nesting the same images
    # a number of time
    # First a complete filling
    for counter, info in enumerate(number):  # create 1, 2 or 3 object
        size = smaller
        infovec = list(info)  # copying the data
        if card.number == 3 and card.shape == 3:
            infovec[2] = double * 19
        if card.number == 3 and card.shape == 2 and counter == 1:
            infovec[1] = double * 32.5
        draw1.polygon(shape(infovec, size), fill=color)
        draw2.polygon(shape(infovec, size), fill=color)

    # Cutting out a center
    if card.filling > 1:
        for counter, infos in enumerate(number):
            size = 0.7 * smaller
            infovec = list(infos)
            if card.number == 3 and card.shape == 3:
                infovec[2] = double * 19
            if card.number == 3 and card.shape == 2 and counter == 1:
                infovec[1] = double * 32.5
            draw1.polygon(shape(infovec, size), fill=white)
            draw2.polygon(shape(infovec, size), fill=red)

    # adding something back in
    if card.filling > 2:
        for counter, info in enumerate(number):
            size = 0.4 * smaller
            infovec = list(info)
            if card.number == 3 and card.shape == 3:
                infovec[2] = double * 19
            if card.number == 3 and card.shape == 2 and counter == 1:
                infovec[1] = double * 32.5
            draw1.polygon(shape(infovec, size), fill=color)
            draw2.polygon(shape(infovec, size), fill=color)

    # saves the images where normalimage() is pointing to
    im1.save(card.normalimage())
    im2.save(card.downimage())
