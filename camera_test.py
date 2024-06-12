import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
from math import pi

#cap = cv2.VideoCapture(0)

while(True):
	# Take each frame
	#_, frame = cap.read()
	image_path = 'FRA-Lab/lab2/image.png'
	frame = cv2.imread(image_path)

	# Convert to HSV color space
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Definir el rango de color en HSV
	lower_range = np.array([10, 100, 100])
	upper_range = np.array([25, 255, 255])

    # Umbralizar la imagen HSV para obtener solo los colores en rango
	mask = cv2.inRange(hsv, lower_range, upper_range)

	# Aplicar transformaciones morfológicas para reducir el ruido
	kernel = np.ones((5, 5), np.uint8)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Apertura
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Cierre

	# Encontrar contornos en la máscara
	contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Suponiendo que hay al menos un contorno, encontrar el contorno más grande
	if contours:
		largest_contour = max(contours, key=cv2.contourArea)

		# Calcular los momentos del contorno más grande
		M = cv2.moments(largest_contour)

		if M["m00"] != 0:
			# Calcular las coordenadas del centro del objeto
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
		else:
			cX, cY = 0, 0

		# Dibujar el contorno y el centro del objeto en la imagen original
		cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
		cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)
		cv2.putText(frame, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

	# Aplicar AND bit a bit de la máscara y la imagen original
	res = cv2.bitwise_and(frame, frame, mask=mask)

	# Mostrar la imagen con el objeto amarillo resaltado y el centro marcado
	cv2.imshow('image', frame)
	
	k = cv2.waitKey(10) & 0xFF
	if k == 27:
		rospy.signal_shutdown("User exit")
		cv2.destroyAllWindows()