import cv2
from orange_detector import OrangeDetector
from kalmanfilter import KalmanFilter
from matplotlib import pyplot as plt
plt.xlim(0, 100) 
plt.ylim(0, 100)
cap=cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920) #dimensioni
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080) #dimensioni
od=OrangeDetector()
kf=KalmanFilter()
while True:
    ret,frame=cap.read()
    if ret is False:
        break
    orange_boards=od.detect(frame)

    x,y,x2,y2=orange_boards
    cx=int((x+x2)/2)
    cy=int((y+y2)/2)
    print("centro x: ",cx,"centro y: ",cy)
    predicted=kf.predict(cx,cy)
    cv2.circle(frame,(predicted[0],predicted[1]),20,(255,0,0),-1) #blu è quello predictato
    cv2.circle(frame,(cx,cy),20,(0,0,255),-1) #rosso è la arancia
    
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1)
    if key == ord("q"):
        break
    plt.plot(int(cx/10),int(cy/10), color="green", marker="o")
    plt.plot(predicted[0]/10,predicted[1]/10, color="red", marker="o")
plt.show()
