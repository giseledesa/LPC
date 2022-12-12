import turtle
import math


def fibo_plot(n):
    a = 0
    b = 1
    i = 0
    square_a = a
    square_b = b
    x.pencolor("blue")

    for i in range(3):
        x.forward(b * factor)
        x.left(90)
    x.forward(b * factor)

    temp = square_b
    square_b = square_b + square_a
    square_a = temp

    for i in range(1, n):
        x.backward(square_a * factor)
        x.right(90)

        for j in range(2):
            x.forward(square_b * factor)
            x.left(90)
        x.forward(square_b * factor)

        temp = square_b
        square_b = square_b + square_a
        square_a = temp

    x.penup()
    x.setposition(factor, 0)
    x.seth(0)
    x.pendown()
    x.pencolor("red")
    x.left(90)

    for i in range(n):
        print(b)
        frd = math.pi * b * factor / 2
        frd /= 90
        for j in range(90):
            x.forward(frd)
            x.left(1)
        temp = a
        a = b
        b = temp + b


term = int(input('Enter the number of iterations (must be > 1): '))

if term > 0:
    print("Fibonacci series for", term, "elements :")
    factor = 20
    x = turtle.Turtle()
    x.speed(100)
    fibo_plot(term)
    turtle.done()
else:
    print("Number of iterations must be > 0")
