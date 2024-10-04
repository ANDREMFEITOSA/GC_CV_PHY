import cv2
import numpy as np

#Função para detectar barras
def bar_detector(ip):
    
    video = cv2.VideoCapture()

    video.open(ip)
    
    while(True):
        captura_ok, frame = video.read()
        if captura_ok:
            
            frame = cv2.resize(frame, (300, 500))
            
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            mask = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)
            
            list_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            bar_contours = []
            
            for cnt in list_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = cv2.contourArea(cnt)
                if area > 1000 and area < 10000:
                    bar_contours.append(cnt)
                    rect = cv2.minAreaRect(cnt)
                    x, y, w, h = cv2.boundingRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    
            cv2.imshow("Video da Webcam", frame)
            
            key = cv2.waitKey(1)
            if key == 13: #Enter
                return len(bar_contours) - 1
                break

