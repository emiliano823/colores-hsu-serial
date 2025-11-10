import cv2

import numpy as np


cap = cv2.VideoCapture(2)
#cap. set(cv2.CAP_PROP_FRAME_WIDTH, 128)
#cap. set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

lower_red = np.array([0, 30, 70])
upper_red = np.array([10, 255, 255])
 
lower_blue = np.array([100, 120, 70])
upper_blue = np.array([140, 255, 255])

lower_green = np.array([40, 91, 40])
upper_green = np.array([80, 255, 255])

lower_yellow = np.array([20, 110, 90])
upper_yellow = np.array([30, 255, 255])

color_detectado = False

font = cv2.FONT_HERSHEY_PLAIN

while True:

    ret, frame = cap.read()
    Fframe = cv2.flip(frame, 1)
    height, width, _ = Fframe.shape

    cx = int(width / 2)
    cy = int(height / 2)

    color_en_centro = False
    
   
    cv2.circle(Fframe, (cx, cy), 4, (40, 40, 40), 1)

    if not ret:
        break

    hsv = cv2.cvtColor(Fframe, cv2.COLOR_BGR2HSV)

    mask_red = cv2.inRange(hsv, lower_red, upper_red) 
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    contornos1,_ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for r in contornos1:
        area = cv2.contourArea(r)
        if area > 300:
            if cv2.pointPolygonTest(r, (cx, cy), False) >= 0:
                cv2.drawContours(Fframe, [r], -1, (0, 0, 255), 3)            

    contornos2,_ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for b in contornos2:
        area = cv2.contourArea(b)
        if area > 300:
            if cv2.pointPolygonTest(b, (cx, cy), False) >= 0:
                cv2.drawContours(Fframe, [b], -1, (255, 0, 0), 3)


    contornos3,_ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for g in contornos3:
        area = cv2.contourArea(g)
        if area > 300:
            if cv2.pointPolygonTest(g, (cx, cy), False) >= 0:
                cv2.drawContours(Fframe, [g], -1, (0, 255, 0), 3)
                
    contornos4,_ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for y in contornos4:
        area = cv2.contourArea(y)
        if area > 300:
            if cv2.pointPolygonTest(y, (cx, cy), False) >= 0:
                cv2.drawContours(Fframe, [y], -1, (0, 255, 255), 3)

    if not color_en_centro:
        color_detectado = False

            
    cv2.imshow("Original", Fframe)


    


    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
