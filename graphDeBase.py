from tkinter import *
from math import *


def func(val, f):
    #val = nombre et f="forme alge avec x"
    x = val
    return eval(f)


def xToScreen(x, xOrig, pixPerUnit):
    return pixPerUnit*x+xOrig


def yToScreen(y, yOrig, pixPerUnit):
    return yOrig-pixPerUnit*y


def buildMathCoords():
    ## fabrication des coordonnées x
    global x_start, xmath, ymath
    x = x_start
    xmath = []
    ymath = []
    while x < x_stop:
        xmath.append(x)
        x += x_step
    ## fabrication des coordonnées y
    for x in xmath:
        ymath.append(func(x, fonction))


def dessin():
    global xmath, ymath
    xscreen = []
    yscreen = []
    for x in xmath:
        xscreen.append(xToScreen(x, 200, pix_per_units))
    for y in ymath:
        yscreen.append(yToScreen(y, 200, pix_per_units))
    graph.delete("all")
    ## dessin des axes
    graph.create_line(0, haut_canvas/2, larg_canvas, haut_canvas/2, fill="red")
    graph.create_line(larg_canvas/2, 0, larg_canvas/2, haut_canvas, fill="red")
    ## Dessin des points
    for i in range(1, len(xscreen)):
        graph.create_line(xscreen[i-1], yscreen[i-1],
                          xscreen[i], yscreen[i], fill="blue")


def clickGauche(event):
    #on obtient les coordonnées du click
    mouse_x.set(event.x)
    mouse_y.set(event.y)
    #on le met dans x et y
    x = mouse_x.get()
    y = mouse_y.get()
    print("x : ", x, "y : ", y)


def clickDroit(event):
    #on obtient les coordonnées du click
    mouse_x.set(event.x)
    mouse_y.set(event.y)
    #on le met dans x et y
    x = mouse_x.get()
    y = mouse_y.get()


def foncbouton1():
    global fonction
    texte.set(entry.get())
    fonction = texte.get()
    print("Nouvelle fonction = ", fonction)
    buildMathCoords()
    dessin()


#Les variables globales
x_start = -10
x_stop = 10
x_range = x_stop-x_start
x_step = 0.01
number_of_points = round(x_range/x_step)

larg_canvas = 400
haut_canvas = 400
pix_per_units = larg_canvas/x_range

xmath = []
ymath = []


fonction = "x*sin(x)"

#Construction de l'interface graphique
root = Tk()
graph = Canvas(root, width=larg_canvas, height=haut_canvas)
graph.pack()


mouse_x = IntVar()
mouse_y = IntVar()
graph.bind("<1>", clickGauche)
graph.bind("<3>", clickDroit)

bouton = Button(root, text="graph", command=foncbouton1)
bouton.pack(side=LEFT)

texte = StringVar()
texte.set(fonction)


entry = Entry(master=root, width=400)
entry.pack(side=RIGHT)
entry.config(width=40)
entry.insert(0, texte.get())

buildMathCoords()
dessin()

mainloop()
