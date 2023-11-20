from GUI import GUI
from HAL import HAL
import cv2

prev_error = 0
sum_error = 0
targetX = 320

KP = # Buscas un buen valor de KP
KD = # Buscas un buen valor de KD
KI = # Buscas un buen valor de KI
    
i = 0
while True:
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cX, cY = 0, 0
    
    M = cv2.moments(contours[0])
  
    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
    
    error = targetX - cX
    sum_error += error
    
    if abs(error) < 0.05:
      sum_error = 0
    
    error_p = error * KP 
    error_i = sum_error * KI
    error_d = (error - prev_error) * KD 

    w = error_p + error_i + error_d
    
    HAL.setV(1)
    HAL.setW(w)
    
    prev_error = error
      
    GUI.showImage(red_mask)
    i += 1