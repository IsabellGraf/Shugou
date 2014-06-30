
from PIL import ImageFont, Image, ImageDraw
from Deck import Deck
from generateImages import make_star, make_triangle, make_square, make_ellipse

white = (255, 255, 255)
large, medium, small = 1, 0.7, 0.4
scale = 0.5


## initiate ##

imI = Image.new('RGB', (1024, 1024), white)  # normal state
imA = Image.new('RGB', (512, 512), white)  # normal state
drawI = ImageDraw.Draw(imI)
drawA = ImageDraw.Draw(imA)


## Android ##

info = [scale*250, scale*370, scale*270]
color = (51, 153, 250)
shape = make_star;
drawA.polygon(shape(info, large), fill=color)
drawA.polygon(shape(info, medium), fill=white)
drawA.polygon(shape(info, small), fill=color)

info = [scale*275, scale*740, scale*600]
color = (0, 200, 0)
shape = make_ellipse
drawA.ellipse(shape(info, large), fill=color)
drawA.ellipse(shape(info, medium), fill=white)

info = [scale*275, scale*280, scale*750]
color = (255, 100, 0)
shape = make_triangle
drawA.polygon(shape(info, large), fill=color)


## IOS ##

info = [250, 370, 270]
color = (51, 153, 250)
shape = make_star;
drawI.polygon(shape(info, large), fill=color)
drawI.polygon(shape(info, medium), fill=white)
drawI.polygon(shape(info, small), fill=color)

info = [275, 740, 600]
color = (0, 200, 0)
shape = make_ellipse
drawI.ellipse(shape(info, large), fill=color)
drawI.ellipse(shape(info, medium), fill=white)

info = [275, 280, 750]
color = (255, 100, 0)
shape = make_triangle
drawI.polygon(shape(info, large), fill=color)


## save ##

imI.save("images/LogoI.png", dpi=(600,600))
imA.save("images/LogoA.png", dpi=(600,600))


