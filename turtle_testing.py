import turtle

t = turtle.Turtle()

t.pos()
t.forward(100)    # dopředu
t.backward(50)    # dozadu

t.heading()
t.left(90)    # otočí se doleva
t.right(45)   # otočí se doprava

t.penup()   # zdvih pera => nekresli
t.pendown() # zacne kreslit

t.pencolor("red")
t.fillcolor("yellow")
t.pensize(5)

t.speed(1)    # nastaceni rychlosti

t.circle(50)

t.goto(100, 50)

t.begin_fill()
# kreslíš uzavřený tvar
t.end_fill()


turtle.done()