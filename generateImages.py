# To run the file you must first install the Pillow module
# i.e. pip install Pillow or pip3 install Pillow
# need install cairo module
# brew install cairo, brew install py2cairo(for python2) or pycairo(for python3)

from PIL import ImageFont, Image, ImageDraw

from Deck import Deck
import cairo

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
    xx = [(d - 0.75 * a, c - 0.3 * a),
          (d + 0.1 * a, c - a), (d + 0.67 * a, c + a)]
    return xx


def make_square(infos, size):
    a = infos[0] * size
    d = infos[1]
    c = infos[2]
    xx = [(d,c-0.75*a), (d+a,c),(d,c+0.75*a),(d-a,c)]
    return xx


def make_ellipse(infos, size):
    a = infos[0] * size * 0.85
    d = infos[1]
    c = infos[2]
    xx = [(d-a,c-a), (d+a,c+a)]
    return xx

def draw_rounded(cr, area, radius, fillin, *argv):
    """ draws rectangles with rounded (circular arc) corners """
    from math import pi
    a,b,c,d=area
    cr.arc(a + radius, c + radius, radius, 2*(pi/2), 3*(pi/2))
    cr.arc(b - radius, c + radius, radius, 3*(pi/2), 4*(pi/2))
    cr.arc(b - radius, d - radius, radius, 0*(pi/2), 1*(pi/2))  # ;o)
    cr.arc(a + radius, d - radius, radius, 1*(pi/2), 2*(pi/2))
    cr.close_path()
    if fillin == 'Fill':
        cr.set_source_rgba(*argv)
        cr.fill()
    else:
        cr.set_line_width(5)
        cr.set_source_rgba(*argv)
        cr.stroke()


def draw_contour(w,h,state):
    import cairo
    offset = 10
    wid = 35
    if state == 'Normal':
        fig_size = (w+offset,h+offset+wid)
    else:
        fig_size = (w+offset,h+offset)

    # an area with coordinates of
    # (top, bottom, left, right) edges in absolute coordinates:
    inside_area = (offset, w-offset, offset, h-offset)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *fig_size)
    cr = cairo.Context(surface)

    if state == 'Normal':
        colorcode = (101/255.,173/255.,178/255.,1)
        background_color = (1.,1.,1.,1.)
        inside_area_down = (offset, w-offset, offset, h-wid)

        draw_rounded(cr, inside_area, 40, 'Fill', *colorcode)
        draw_rounded(cr, inside_area, 40,'Border', *colorcode)

        draw_rounded(cr, inside_area_down, 40,'Fill', *background_color)
        draw_rounded(cr, inside_area_down, 40,'Border', *colorcode)

    elif state == 'Down':
        background_color = (255/255.,200/255.,200/255.,1.)
        colorcode = (101/255.,173/255.,178/255.,1)

        draw_rounded(cr, inside_area, 40, 'Fill', *background_color)
        draw_rounded(cr, inside_area, 40,'Border', *colorcode)

    im = Image.frombuffer("RGBA", fig_size, surface.get_data(), "raw", "BGRA", 0,1)
    return im


white = (255, 255, 255)
red = (255, 200, 200)

# A factor that creates a much larger image that is much larger than needed
# It is scalled back down later on, this greatly improves the image quality.
double = 9
# How the scalling occurs
smaller = 0.8
large, medium, small = 1, 0.7, 0.4
colors = {1: (51, 153, 250), 2: (0, 200, 0), 3: (255, 100, 0)}
shapes = {1: make_star, 2: make_ellipse, 3: make_triangle}
# [size, x, y]
numbers = {1: [[double * 20, double * 31, double * 19]],
           2: [[double * 15, double * 16.5, double * 19],
              [double * 15, double * 43.5, double * 19]],
           3: [[double * 13, double * 13, double * 23], 
              [double * 13, double * 30.5, double * 15],
              [double * 13, double * 48, double * 23]]}


deck = Deck()

for card in deck:
    #im1 = Image.new('RGB', (double * 62, double * 38), white)  # normal state
    #im2 = Image.new('RGB', (double * 62, double * 38), red)  # down state
    im1 = draw_contour(double * 62, double * 38, 'Normal')
    im2 = draw_contour(double * 62, double * 38, 'Down')
    draw1 = ImageDraw.Draw(im1)
    draw2 = ImageDraw.Draw(im2)

    number = numbers[card.number]
    shape = shapes[card.shape]
    color = colors[card.colour]

    # There is 3 types of fillings, they are doen by nesting the same images
    # a number of time
    # First a complete filling
    for counter, info in enumerate(number):  # create 1, 2 or 3 object
        size = large*smaller
        infovec = list(info)  # copying the data
        if card.number == 3 and card.shape == 3:
            infovec[2] = double * 19
        if card.shape == 2:
            draw1.ellipse(shape(infovec, size), fill=color)
            draw2.ellipse(shape(infovec, size), fill=color)
        else:
            draw1.polygon(shape(infovec, size), fill=color)
            draw2.polygon(shape(infovec, size), fill=color)

    # Cutting out a center
    if card.filling > 1:
        for counter, infos in enumerate(number):
            size = medium * smaller
            infovec = list(infos)
            if card.number == 3 and card.shape == 3:
                infovec[2] = double * 19
            if card.shape == 2:
                draw1.ellipse(shape(infovec, size), fill=white)
                draw2.ellipse(shape(infovec, size), fill=red)
            else:
                draw1.polygon(shape(infovec, size), fill=white)
                draw2.polygon(shape(infovec, size), fill=red)

    # adding something back in
    if card.filling > 2:
        for counter, info in enumerate(number):
            size = small * smaller
            infovec = list(info)
            if card.number == 3 and card.shape == 3:
                infovec[2] = double * 19
            if card.shape == 2:
                draw1.ellipse(shape(infovec, size), fill=color)
                draw2.ellipse(shape(infovec, size), fill=color)
            else:
                draw1.polygon(shape(infovec, size), fill=color)
                draw2.polygon(shape(infovec, size), fill=color)

    # saves the images where normalimage and downimage is pointing to
    # dpi sets the resolution of images(dots per inch)
    im1.save(card.normalimage(), dpi=(264,264))
    im2.save(card.downimage(), dpi=(264,264))
