import turtle
from math import cos, radians

# shapes settings (num of vertices in the shape and num of shapes)-->
#calculations of the angle according to the num of vertices (shape)

shape = int(input("how many vertices would you like-->"))
num = int(input("how many-->"))
angle = (shape - 2) * 180 / shape

#color settings (from color to color+calculations of each and every part of the rgb)-->
#(red ,green, blue and for the dsecond color [color finale]+the change of this colors)
turtle.colormode(255)
colorbegin=int(input("what color do you want from(rgb)-->"))
colorfinale=int(input("what color do you want to(rgb)-->"))
#-----------------------------------------------------------
redcurrent=int(colorbegin/(10**6))
greencurrent=int((colorbegin/(10**3))%(10**3))
bluecurrent=int(colorbegin%(10**3))
#-----------------------------------------------------------
redfinale=int(colorfinale/(10**6))
greenfinale=int((colorfinale/(10**3))%(10**3))
bluefinale=int(colorfinale%(10**3))
#-----------------------------------------------------------
redchange=(redfinale-redcurrent)/num
bluechange = (bluefinale -bluecurrent) / num
greenchange = (greenfinale - greencurrent) / num

#start
wn = turtle.Screen()
t = turtle.Turtle()
#settings the correct elemants so the scrupt work
t.pu()
t.goto(0, 0)
t.setheading(180)
cnt = 2
radius = 50
#counting each shape so it woulld print the number of the shape
cnt1=0
# main loop
pensize0=0
#repeting the creation of the shape the num of times that the user asked
for item0 in range(num):
    pensize0 += 0.75
    cnt1 += 1
    t.pensize(pensize0)
    t.left(angle/2)
    #setting the pencolor to the rgb
    t.pencolor(redcurrent, greencurrent, bluecurrent)
    t.fd(radius)
    t.pd()
    t.right(angle / 2)
    #calculations of the edges of the shape according to the radius
    edge = 2 * cos(radians(angle / 2)) * radius
    #creating the shape
    for item in range(shape):
        t.pensize(pensize0)
        t.right(180 - angle)
        t.fd(edge)
    t.pu()
    t.goto(0,0)
    t.setheading(180)
    radius += 30
    #printing the rgb of each shape
    redcurrent = int(redcurrent+redchange)
    print("------------------------------------------------------")
    print("red _", cnt1, ": is equal to=", redcurrent)
    greencurrent = int(greencurrent + greenchange)
    print("green _", cnt1, ": is equal to=", greencurrent)
    bluecurrent = int(bluecurrent + bluechange)
    print("blue _", cnt1, " : is equal to=", bluecurrent)
    print("rgb=", redcurrent, ",", greencurrent, ",", bluecurrent)
    print("------------------------------------------------------")
#end
turtle.mainloop()