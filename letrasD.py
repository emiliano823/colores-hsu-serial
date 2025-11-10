import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    Rcap = cv2.resize(frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_NEAREST)
    if not ret:
        break

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(Rcap, cv2.COLOR_BGR2GRAY)

    _, letras = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    contorno, _ = cv2.findContours(letras, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contorno:
        area = cv2.contourArea(c)
        if area > 300:
            x, y, w, h = cv2.boundingRect(c)
            roi = letras[y:y+h, x:x+w]
            roii = cv2.resize(roi, (200, 200))
        
            A_zona = roii[0:30, 90:120]
            B_zona = roii[185:200, 90:120]
            D_zona = roii[100:120 , 0:30]
            I_zona = roii[80:110 , 170:200]

            

            N_arriba = np.any(A_zona == 255)
            N_abajo = np.any(B_zona == 255)
            N_derecha = np.any(D_zona == 255)
            N_izquierda = np.any(I_zona == 255)
            #print(N_arriba, N_abajo, N_derecha, N_izquierda)

            letra = ''
            if not N_arriba and not N_abajo and N_derecha and N_izquierda:
                letra = 'H'
            elif N_arriba and N_abajo or not N_derecha or not N_izquierda:
                letra = 'S'
            elif not N_arriba and N_abajo and N_derecha and N_izquierda:
                letra = 'U'
            else:
                letra = '?'

            cv2.putText(Rcap, letra, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.rectangle(Rcap, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('roi', roii)
            cv2.imshow('Arriba', A_zona)
            cv2.imshow('Abajo', B_zona)
            cv2.imshow('Derecha', D_zona)
            cv2.imshow('Izquierda', I_zona)
    
    cv2.imshow('frame', Rcap)
    cv2.imshow('letras', letras)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
