
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

def make_star(infos,size):
    d=infos[1]
    c=infos[2]
    a=infos[0]*size
    b=0.5*infos[0]*size
    xx = [(d,c-b),(d-0.5*a,c-0.866*a),(d-0.866*b,c-0.5*b),(d-a,c),(d-0.866*b,c+0.5*b),(d-0.5*a,c+0.866*a),(d,c+b),\
(d+0.5*a,c+0.866*a),(d+0.866*b,c+0.5*b),(d+a,c),(d+0.866*b,c-0.5*b),(d+0.5*a,c-0.866*a)]
    return xx
    
def make_triangle(infos,size):
    a=infos[0]*size
    d=infos[1]
    c=infos[2]
    xx = [(d-0.2*a,c-0.7*a),(d+0.75*a,c+0.8*a),(d-a,c)]
    return xx

def make_square(infos,size):
    a=infos[0]*0.7*size
    d=infos[1]
    c=infos[2]
    xx=[d-a,c-a,d-a,c+a,d+a,c+a,d+a,c-a]
    return xx


colors = [(51,153,250),(0,200,0),(253,236,0)]
shapes = [make_star,make_square,make_triangle]
fillings = [0,1,2]
numbers = [[[50,100,50]],[[40,50,50],[40,150,50]],[[35,37,60],[35,100,40],[35,162,60]]]
white = (255,255,255)
red = (255,200,200)


for color_number,color in enumerate(colors):
    for shape_number,shape in enumerate(shapes):
        for number_number,number in enumerate(numbers):
            for filling_number,filling in enumerate(fillings):
                im1 = Image.new('RGB',(200,100),white)
                im2 = Image.new('RGB',(200,100),red)
                draw1 = ImageDraw.Draw(im1)
                draw2 = ImageDraw.Draw(im2)
                for infos in number:
                    size=1
                    infovec = list(infos)
                    if number_number==2 and shape_number==2:
                        infovec[2]=50
                    draw1.polygon(shape(infovec,size), fill = color, outline = None)
                    draw2.polygon(shape(infovec,size), fill = color, outline = None)
                if filling > 0:
                    for infos in number:
                        size=0.7
                        infovec = list(infos)
                        if number_number==2 and shape_number==2:
                            infovec[2]=50
                        draw1.polygon(shape(infovec,size),fill = white, outline = None)
                        draw2.polygon(shape(infovec,size),fill = red, outline = None)
                if filling == 2:
                    for infos in number:
                        size = 0.4
                        infovec = list(infos)
                        if number_number==2 and shape_number==2:
                            infovec[2]=50
                        draw1.polygon(shape(infovec,size),fill = color, outline = None)
                        draw2.polygon(shape(infovec,size),fill = color, outline = None)
                del draw1
		del draw2
                im1.save('images/' + str(color_number+1)+str(shape_number+1)+str(number_number+1)+str(filling_number+1)+'.png')
                im2.save('images/' + str(color_number+1)+str(shape_number+1)+str(number_number+1)+str(filling_number+1)+'_down'+'.png')
                
                
