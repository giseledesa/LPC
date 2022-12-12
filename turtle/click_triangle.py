import turtle

wn = turtle.Screen()
test = turtle.Turtle()


def click_triangle(x, y):
    test.penup()
    test.goto(x, y)
    test.pendown()
    for i in range(3):
        test.forward(100)
        test.left(120)
        test.forward(100)


turtle.onscreenclick(click_triangle, 1)

turtle.listen()
turtle.done()
