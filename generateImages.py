
# I've installed the forked version of PIL know as Pillow
# i.e. pip install Pillow
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
