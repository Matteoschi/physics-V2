from kalmanfilter import KalmanFilter
import cv2
# Kalman Filter+
kf = KalmanFilter()
img = cv2.imread("sfondo.jpg")
ball_positions = [(50, 100), (100, 100), (150, 100), (200, 100), (250, 100), (300, 100), (350, 100), (400, 100), (450, 100)]
for pt in ball_positions:
    cv2.circle(img, pt, 15, (0, 20, 220), -1)
    predicted = kf.predict(pt[0], pt[1])
    cv2.circle(img, predicted, 15, (20, 220, 0), 4)
for i in range(10):
    predicted=kf.predict(predicted[0],predicted[1])
    cv2.circle(img, predicted, 15, (20, 220, 0),4)
cv2.imshow("Img", img)
cv2.waitKey(0)