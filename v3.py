# Importer les librairies
from tkinter import *
from math import *

# Function initial
primaryFunction = "x**3"
secondaryFunction = "x-5"

# Defini les couleurs à utiliser pour les différentes fonctions représentées
functionColors = ['#38BDF8','#22C55E']

# Renvoyer la valeur de la fonction pour un certain point
def functionValue(function, value):
    x = value
    return eval(function)

### Construction de l'interface
# Taille en px
canvasWidthAndHeight = 700
guiWidth = 400

# Moitié des valeurs précédentes pour divers utilisations
halfCanvasWidthAndHeight = canvasWidthAndHeight/2
halfGuiWidth = guiWidth/2

# Methode pour créer la window
root = Tk()
root.configure(bg='#111827')

# Titre de la fenetre
root.title("GeoGeclatax © | Le concurent direct à GeoGebra, mais vraiment éclaté")

# Création de 2 pannels : Un Canvas pour les graphiques ainsi qu'une Frame pour les elements du GUI
graph = Canvas(root,width=canvasWidthAndHeight,height=canvasWidthAndHeight,bg="white",background="white")
gui = Frame(root,width=guiWidth,height=canvasWidthAndHeight,bg="#111827")

# On place les 2 pannels cotes à cotes
graph.pack(fill=BOTH, expand=YES,side="left")
gui.pack(fill=BOTH, expand=YES,side="right",padx=10)

# Range du x et y
rangeEnd = 10
# Vu qu'on utilise une echelle, on peut se permettre de donner simplement l'inverse
# TODO: Faire en sorte de pouvoir donner des valeurs différentes des 2 côtés, en fait comme pouvoir bouger à l'intérieur du canvas avec un click 
rangeStart = -1 * rangeEnd

# Quel est la fréquence du calcul des coordonnées
stepBetween = 0.01

rangeBetween = rangeEnd - rangeStart 

# On calcule le nombre de pixel 
pxForEachStep = canvasWidthAndHeight/rangeBetween

# Graduation du graphique, données pour le range initiale
smallGraduationStep = 1
bigGraduationStep = 5

# Fonction pour générér les coordonées X et Y pour une fonction ainsi que les 
def createCoordinates(function):
    # Vide les valeurs possiblement existantes dans les listes et/ou créer les listes
    global coordinatesX, coordinatesY, pointsX, pointsY, intersectionsWithX
    
    # Listes contenant les données généréés
    coordinatesX = []
    coordinatesY = []

    pointsX = []
    pointsY = []

    intersectionsWithX = []
    
    # Fabrication des coordonnées x
    x = rangeStart
    while x < rangeEnd:
        # On obtient les valeurs X et Y
        # x = x
        y = functionValue(function,x)

        # On ajoute dans les listes respectivent les coordonnées
        coordinatesX.append(x)
        coordinatesY.append(y)

        # Genère les points en prenant en compte le step, permet un affichage
        pointsX.append(pxForEachStep*x+halfCanvasWidthAndHeight)
        pointsY.append(halfCanvasWidthAndHeight-pxForEachStep*y)

        # Obtiens les zéros approximatifs en analysant le comportement de la fonction et regarde lorsqu'il y a un changement dans le signe des points OU est directemment égal à 0
        # Il est impossible de simplement d'observer le tableau puisque les valeurs ne sont que rarement égal à 0
        if len(coordinatesY) >= 2:
            if y == 0:
                intersectionsWithX.append(len(coordinatesY))
            elif y > 0 and coordinatesY[-2] < 0:
                intersectionsWithX.append(len(coordinatesY))
            elif y < 0 and coordinatesY[-2] > 0:
                intersectionsWithX.append(len(coordinatesY))           
        x += stepBetween

        # On utilise cette technique uniquement pour l'affichage des zéros et éviter de grands calculs, pour l'obtention des zéros de manière plus précises une autre fonction sera nécéssaire
    
    # A la fin de la fonction on renvoie un grand array contenant tous les tableaux ainsi que la fonction utilisée pour pouvoir comparer
    dataset = [coordinatesX,coordinatesY,pointsX,pointsY,intersectionsWithX,function]
    return dataset

def drawAxes():
    # Dessin des axes (Dessine de (x1,y1) à (x2,y2))
    # Axe des X
    graph.create_line(0, halfCanvasWidthAndHeight, canvasWidthAndHeight,halfCanvasWidthAndHeight,fill="black")
    # Axe des Y
    graph.create_line(halfCanvasWidthAndHeight, 0, halfCanvasWidthAndHeight,canvasWidthAndHeight,fill="black")

    # Dessine la graduation
    x = rangeStart
    graduationSize = 0
    smallGraduationSize = 8
    bigGraduationSize = 16

    # Determine les cordonnées X dans le range 
    count = 1
    bigGraduationInCanvasList = []
    while(True):
        if count*bigGraduationStep <= rangeEnd:
            bigGraduationInCanvasList.append(count*bigGraduationStep)
            bigGraduationInCanvasList.append(-count*bigGraduationStep)
        else:
            break
        count += 1

    while(x <= rangeEnd):
        # On regarde si le x correspond a une grande ou petite graduation
        if x in bigGraduationInCanvasList:
            graduationSize = bigGraduationSize/2
        else:
            graduationSize = smallGraduationSize/2
        # Créer une graduation pour l'axe X et Y
        graph.create_line(x*pxForEachStep + halfCanvasWidthAndHeight, halfCanvasWidthAndHeight - graduationSize, x*pxForEachStep + halfCanvasWidthAndHeight, halfCanvasWidthAndHeight + graduationSize, width=1.5, fill="black")
        graph.create_line(halfCanvasWidthAndHeight - graduationSize, x*pxForEachStep + halfCanvasWidthAndHeight , halfCanvasWidthAndHeight + graduationSize, x*pxForEachStep + halfCanvasWidthAndHeight, width=1.5, fill="black")

        x += smallGraduationStep

# Dessine l'ensemble des points qui se relient entre eux pour dessiner la fonction
def drawPoints(color, dataset):
    # On reprend les array qui ont été générés précédemment à partir du dataset
    pointsX = dataset[2]
    pointsY = dataset[3]

    # Pour chaque point, on place sa coordonée dans l'ordre sur le graphique et on le relis avec le précédent
    for i in range(1, len(pointsX)):
        graph.create_line(pointsX[i-1], pointsY[i-1],pointsX[i], pointsY[i], fill=color, width=1.5)

# Dessine les points sur les coordonées d'intesections avec l'axe des X | Approx. des zéros de la fonction
def drawDots(color,dataset):
    
    intersectionsWithX = dataset[4]

    for i in range(0,len(intersectionsWithX)):
        graph.create_oval(intersectionsWithX[i]/(rangeBetween/canvasWidthAndHeight*100),halfCanvasWidthAndHeight,intersectionsWithX[i]/(rangeBetween/canvasWidthAndHeight*100),halfCanvasWidthAndHeight,fill=color, width=7,outline=color)

# Fonction mère regroupant toutes les autres fonctions nécéssaires à la création d'une fonction (calculs,affichage,etc..)
def drawFunction(function,color,letter):
    # On appelle les fonctions dans l'ordre pour afficher au final une fonction
    dataset = createCoordinates(function)
    drawPoints(color,dataset)
    drawDots(color,dataset)

    # Affiche l'expression de la fonction sous forme de texte
    # TODO; Améliorer cette fonction en se basant sur les 3/4 visible et non pas totals des coordonnées
    # La si une fonction est exponentielle, il y a de très grande chances de ne pas remarquer le nom de la fonction
    # Ensuite il faudrait aussi observer le comportement de la fonction pour en déduire dans quelle direction il faut placer le nom afin de ne pas la couvrir
    graph.create_text(pointsX[floor(3/4*len(pointsX))]+35,pointsY[floor(3/4*len(pointsX))]-10,fill=color,font="Helvetica 12",text=letter + "(x) = " + function,justify='left',anchor='w')
    
    # On renvoie le dataset généré par la fonction createCoordinates, utile par la suite pour nos calculs
    return dataset

# def selectStartPoint(event):
#     print('Right Click')
#     global startingPointLine, endingPointLine, xStartCoord, polygonIntegralShape, polygonIntegralShapeText
    
#     graph.delete(polygonIntegralShape)
#     graph.delete(polygonIntegralShapeText)

#     mouse_x.set(event.x)
#     xStartCoord = mouse_x.get()
#     print(xStartCoord)
#     # Supprime une ligne précédentes si existe
#     graph.delete(startingPointLine)
#     graph.delete(endingPointLine)
#     # Créer une ligne
#     startingPointLine = graph.create_line(xStartCoord,0,xStartCoord,canvasWidthAndHeight, width=1.5, fill="#94A3B8",dash=(10,20))

# def selectEndPoint(event):
#     print('Left Click')
#     global endingPointLine, xEndCoord
#     mouse_x.set(event.x)
#     xEndCoord = mouse_x.get()
#     # Supprime une ligne précédentes si existe
#     graph.delete(endingPointLine)
#     # Créer une ligne
#     endingPointLine = graph.create_line(xEndCoord,0,xEndCoord,canvasWidthAndHeight, width=1.5, fill="#94A3B8",dash=(10,20))
#     # Créer la forme pour l'integrale
#     createPolygon()

# def calculateInegral(function):
#     global xStartCoord, xEndCoord
#     unite = ((xStartCoord-xEndCoord)*pxForEachStep)/1000
#     surface = 0

#     for i in range(0,1000):
#         surface = surface + functionValue(function,i) * unite
#     return round(surface,2)

# def createPolygon():
#     global xStartCoord, xEndCoord, polygonIntegralShape, polygonIntegralShapeText

#     # print(coordinatesX[round((rangeBetween/stepBetween)/canvasWidthAndHeight*xStartCoord)])
#     # print(coordinatesX[round((rangeBetween/stepBetween)/canvasWidthAndHeight*xEndCoord)])

#     startIndex = round((rangeBetween/stepBetween)/canvasWidthAndHeight*xStartCoord)
#     endIndex = round((rangeBetween/stepBetween)/canvasWidthAndHeight*xEndCoord)

#     # Commence la shape
#     shapeCordinatesY = [xStartCoord,halfCanvasWidthAndHeight]

#     # Créer les coordonées de la forme
#     for index in range(startIndex,endIndex):
#         shapeCordinatesY.append(pointsX[index])

#         if pointsY[index] > halfCanvasWidthAndHeight:
#             shapeCordinatesY.append(halfCanvasWidthAndHeight)
#         else:
#             shapeCordinatesY.append(pointsY[index])

#     # Ferme la shape
#     shapeCordinatesY.append(xEndCoord)
#     shapeCordinatesY.append(halfCanvasWidthAndHeight)

#     # Calcul l'intégral

#     # Création de la forme et du texte
#     polygonIntegralShape = graph.create_polygon(shapeCordinatesY,fill='#CFFAFE',width=1)
#     polygonIntegralShapeText = graph.create_text((xStartCoord+xEndCoord)/2,halfCanvasWidthAndHeight+40,fill='#0C4A6E',font="Helvetica 24 bold",text=calculateInegral(primaryFunction),justify='center',anchor='center')

def changeScale(event):
    xMax = e3.get()
    global rangeEnd, rangeStart, rangeBetween, pxForEachStep
    rangeEnd = xMax
    rangeStart = -1*xMax
    rangeBetween = rangeEnd - rangeStart 
    pxForEachStep = canvasWidthAndHeight/rangeBetween

    graph.delete("all")
    drawAxes()
    

# polygonIntegralShape = 0
# polygonIntegralShapeText = 0
# xStartCoord = 1
# xEndCoord = 1
# startingPointLine = 0
# endingPointLine = 0
# mouse_x = IntVar()
# # Click gauche
# graph.bind("<Button-1>", selectStartPoint)
# # Click droit pour Windows et Linux
# graph.bind("<Button-3>", selectEndPoint)
# # Click droit pour MacOs
# graph.bind("<Button-2>", selectEndPoint)


# Titre
Label(gui, text="GeoGeclatax", fg='white', font=("Comic Sans MS", 33,'bold'),justify='center',background='#111827').grid(row=0, column=0,pady=5)

# Defini le style pour éviter de devoir tout réecrire
labelStyle = {'font': ("Helvetica", 14,''), 'background': '#111827', 'fg': '#64748B'}
subTitleStyle = {'font': ("Comic Sans MS", 18,'bold'), 'background': '#111827', 'fg': 'white'}
entryStyle = {'font': ("Comic Sans MS", 14,'bold'), 'background': 'white','borderwidth':0,'highlightthickness':0,'borderwidth':3,'relief':'flat'}
sliderStyle = {'font': ("Comic Sans MS", 9,'bold'), 'background': '#111827', 'fg': 'white','borderwidth':0,'cursor':'sb_h_double_arrow'}

l3 = Label(gui, text = "Réglages", **subTitleStyle)
l3.grid(row = 1, column = 0, columnspan=3, sticky = W, pady = 4)

# Label 1
l1 = Label(gui, text = "Fonction principale :", **labelStyle)
l1.grid(row = 2, column = 0, sticky = W, pady = 4)
e1 = Entry(gui, fg=functionColors[0], **entryStyle)
e1.grid(row = 2, column = 1, pady = 4)

# Label 2
l2 = Label(gui, text = "Fonction secondaire :", **labelStyle)
l2.grid(row = 3, column = 0, sticky = W, pady = 4)
e2 = Entry(gui, fg=functionColors[1], **entryStyle)
e2.grid(row = 3, column = 1, pady = 4)

# Label 3
l3 = Label(gui, text = "Echelle :", **labelStyle)
l3.grid(row = 4, column = 0, sticky = W, pady = 4)
e3 = Scale(gui, from_=10, to=100, command=changeScale, orient='horizontal',bd=0,resolution=10,**sliderStyle)
e3.grid(row = 4, column = 1,columnspan=3 , pady = 4,sticky=N+S+E+W) # sticky=N+S+E+W permet de faire que les élement occupent toute la place de la column
  

l3 = Label(gui, text = "Analyse fonction principale", **subTitleStyle)
l3.grid(row = 5, column = 0, columnspan=3, sticky = W, pady = 4)

l3 = Label(gui, text = "Analyse fonction secondaire", **subTitleStyle)
l3.grid(row = 7, column = 0, columnspan=3, sticky = W, pady = 4)



# Version en bas pour un max de professionalisme
Label(gui, text="V 1.0.0", fg='white', font=("Helvetica ", 10),justify='center',background='#111827').place(x=0, y=canvasWidthAndHeight-5, anchor='w')

# Main
graph.delete("all")
drawFunction(primaryFunction,'#38bdf8','f')
# drawFunction('5','red')
drawAxes()



# Empecher la possibilité de resize la fenetre
root.resizable(False, False) 
# Pour que le programme tourne sans arrêt
mainloop()
