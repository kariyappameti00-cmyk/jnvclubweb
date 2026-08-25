import turtle

t = turtle.Turtle()
s = turtle.Screen()

s.bgcolor("black")
t.speed(0)
t.width(2)

colors = ["cyan", "magenta", "yellow", "lime", "white"]

for i in range(1200):

    t.pencolor(colors[i % 5])

    t.circle(10, 50)

    t.left(70)

    t.forward(59)

    t.left(20)

    t.circle(i * 4, 60)

t.hideturtle()

turtle.done()
