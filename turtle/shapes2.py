#chosing color
color=input("what is your chosen color")

import turtle

wn=turtle.Screen()
t=turtle.Turtle()

#make the player faster
t.speed(1000000)

t.pensize(0.5)

#looping the line so it would look like a circle

for item in range(360):
    t.color(color)
    t.forward(100)
    t.right(30)
    t.forward(20)
    t.left(60)
    t.forward(50)
    t.penup()
    t.setposition(0, 0)
    t.pendown()
    #changing the direction
    t.right(1)

#the end
turtle.done()