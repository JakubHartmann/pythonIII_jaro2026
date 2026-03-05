import turtle



def obrys_vlajky():
    t.penup()

    t.goto(-150,100)
    t.pendown()
    t.forward(300)
    t.right(90)
    t.forward(200)
    t.right(90)
    t.forward(300)
    t.right(90)
    t.forward(200)


t = turtle.Turtle()

obrys_vlajky()

t.fillcolor("blue")
t.begin_fill()
t.goto(0,0)
t.goto(-150,-100)
t.goto(-150,100)
t.end_fill()

t.goto(-150, -100)
t.fillcolor("red")
t.begin_fill()
t.goto(0,0)
t.goto(150,0)
t.goto(150,-100)
t.goto(-150, -100)
t.end_fill()


t.reset()

obrys_vlajky()

t.penup()
t.goto(0,-50)
t.pendown()
t.right(90)

t.fillcolor("red")
t.begin_fill()
t.circle(50)
t.end_fill()






turtle.done()
