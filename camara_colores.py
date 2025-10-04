import cv2
import numpy as np
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
portsList = []

camara_colores = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(2)
#camara_colores.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
#camara_colores.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

limite_inferior_rojo = np.array([0, 30, 70])
limite_superior_rojo = np.array([10, 255, 255])
 
limite_inferior_azul = np.array([100, 120, 70])
limite_superior_azul = np.array([140, 255, 255])

limite_inferior_verde = np.array([40, 91, 40])
limite_superior_verde = np.array([80, 255, 255])

limite_inferior_amarillo = np.array([20, 110, 90])
limite_superior_amarillo = np.array([30, 255, 255])

bandera_color_detectado = False

fuente_texto_colores = cv2.FONT_HERSHEY_PLAIN

print("Puertos disponibles:")
for one in ports:
    portsList.append(one.device)  # solo el nombre (ej. COM3)
    print(one.device)

# Elegir puerto
com = input("Selecciona el número de puerto (ej. COM3): ")

if com not in portsList:
    print("⚠️ Puerto no válido. Intenta de nuevo.")
    exit()

# Configurar conexión
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = com
serialInst.open()

print(f"✅ Conectado a {com}")

while True:
    command = input("Arduino Command (ON/OFF/exit): ").strip()
    serialInst.write(command.encode('utf-8'))

    if command.lower() == 'exit':
        print("Cerrando conexión...")
        serialInst.close()
        break

    ret, frame = camara_colores.read()
    Rcap = cv2.resize(frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_NEAREST)
    if not ret:
        break

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
            print(N_arriba, N_abajo, N_derecha, N_izquierda)

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
    


    lectura_correcta, cuadro_colores = camara_colores.read()
    cuadro_espejo = cv2.flip(cuadro_colores, 1)
    alto_frame, ancho_frame, _ = cuadro_espejo.shape

    centro_x = int(ancho_frame / 2)
    centro_y = int(alto_frame / 2)

    bandera_color_en_centro = False
    
    cv2.circle(cuadro_espejo, (centro_x, centro_y), 4, (40, 40, 40), 1)

    if not lectura_correcta:
        break

    hsv_colores = cv2.cvtColor(cuadro_espejo, cv2.COLOR_BGR2HSV)

    mascara_rojo = cv2.inRange(hsv_colores, limite_inferior_rojo, limite_superior_rojo) 
    mascara_azul = cv2.inRange(hsv_colores, limite_inferior_azul, limite_superior_azul)
    mascara_verde = cv2.inRange(hsv_colores, limite_inferior_verde, limite_superior_verde)
    mascara_amarillo = cv2.inRange(hsv_colores, limite_inferior_amarillo, limite_superior_amarillo)

    contornos_rojo,_ = cv2.findContours(mascara_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contorno_r in contornos_rojo:
        area_r = cv2.contourArea(contorno_r)
        if area_r > 300:
            if cv2.pointPolygonTest(contorno_r, (centro_x, centro_y), False) >= 0:
                cv2.drawContours(cuadro_espejo, [contorno_r], -1, (0, 0, 255), 3)            

    contornos_azul,_ = cv2.findContours(mascara_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contorno_b in contornos_azul:
        area_b = cv2.contourArea(contorno_b)
        if area_b > 300:
            if cv2.pointPolygonTest(contorno_b, (centro_x, centro_y), False) >= 0:
                cv2.drawContours(cuadro_espejo, [contorno_b], -1, (255, 0, 0), 3)

    contornos_verde,_ = cv2.findContours(mascara_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contorno_g in contornos_verde:
        area_g = cv2.contourArea(contorno_g)
        if area_g > 300:
            if cv2.pointPolygonTest(contorno_g, (centro_x, centro_y), False) >= 0:
                cv2.drawContours(cuadro_espejo, [contorno_g], -1, (0, 255, 0), 3)
                
    contornos_amarillo,_ = cv2.findContours(mascara_amarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contorno_y in contornos_amarillo:
        area_y = cv2.contourArea(contorno_y)
        if area_y > 300:
            if cv2.pointPolygonTest(contorno_y, (centro_x, centro_y), False) >= 0:
                cv2.drawContours(cuadro_espejo, [contorno_y], -1, (0, 255, 255), 3)

    if not bandera_color_en_centro:
        bandera_color_detectado = False

    cv2.imshow("Deteccion de Colores", cuadro_espejo)
    cv2.imshow('frame', Rcap)
    cv2.imshow('letras', letras)

    if cv2.waitKey(1) == 27:
        break

camara_colores.release()
cv2.destroyAllWindows()
