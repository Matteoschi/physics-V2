import math
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
#entrata video
entrata=r"C:\Users\alessandrini\Documents\coding\trajectory\video\2.mp4"
catturato = cv2.VideoCapture(entrata)
#colore
colore = ColorFinder(False)
valori_colore = {'hmin': 0, 'smin': 157, 'vmin': 131, 'hmax': 21, 'smax': 255, 'vmax': 255}
#variabili
posListX, posListY = [], []
lista = [item for item in range(0, 1300)]
bersaglio = False
#punti bersaglio
x1=800    
x2=965
yb=600
while True:
    #processare immaggine
    success, img = catturato.read()
    #scontornare immaggine
    imgColor, maschera = colore.update(img, valori_colore)
    #locazione dell oggetto
    contorni, location = cvzone.findContours(img, maschera)
    if location :
        posListX.append(location[0]['center'][0])
        posListY.append(location[0]['center'][1])
    #bersaglio raffigurato
    cv2.circle(contorni, (x1,yb), 5, (0, 255, 0))
    cv2.circle(contorni, (x2,yb), 5, (0, 255, 0))
    cv2.line(contorni, (x1,yb),(x2,yb), (0, 0, 255),4)

    if posListX:
        A, B, C = np.polyfit(posListX, posListY, 2)
        #creare punti passaggio palla
        for i, (posX, posY) in enumerate(zip(posListX, posListY)):
            pos = (posX, posY)
            cv2.circle(contorni, pos, 5, (0, 255, 0))
            if i != 0:
                cv2.line(contorni, pos, (posListX[i - 1], posListY[i - 1]), (0, 255, 0), 1)
        #parabola
        for x in lista:
            y = int(A *x*x  + B * x + C) 
            cv2.circle(contorni, (x, y), 1, (0, 0, 255), cv2.FILLED)
        if len(posListX) <7: #10 punti detectati sul immagine
            if entrata != 0 or entrata != 1:
                c = C-1660      
            else:
                c=C-300     
            delta=float(B ** 2 - (4 * A * c))
            if delta > 0:
                radice=math.sqrt(delta)
                risultato = (int(-B +  radice/ (2 * A)))
                print("N ",i," risultato",risultato," pos(x,y) ",pos)
                bersaglio = x1 <= risultato <= x2
        if bersaglio:
            cvzone.putTextRect(contorni, "DENTRO", (10, 50), scale=2, thickness=5, colorR=(0, 200, 0), offset=20)
        else:
            cvzone.putTextRect(contorni, "FUORI", (10, 50),scale=2, thickness=5, colorR=(0, 0, 200), offset=20)
    press=cv2.waitKey(1)
    if press==ord("q"):
        break
    cv2.imshow("rilevamento", contorni)
    cv2.waitKey(1)  
# TODO 
# analizzare quando ce la telecamera live   
