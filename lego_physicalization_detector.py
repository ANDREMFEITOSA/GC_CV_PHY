import numpy as np
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation

array_colors_h = [0, 0, 0, 0]
array_colors = ['r', 'g', 'y', 'b']

lower_range_r = np.array([0, 156, 102])
upper_range_r = np.array([10, 255, 255])
lower_range_g = np.array([46, 102, 59])
upper_range_g = np.array([85, 255, 76])
lower_range_y = np.array([24, 215, 108])
upper_range_y = np.array([61, 255, 255])
lower_range_b = np.array([100,200,125])
upper_range_b = np.array([118,255,199])

def plotar_grafico(colors, heights):
    df = pd.DataFrame(heights, index=colors)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(colors, heights, width=0.5, color=array_colors)
    ax.grid()
    ax.set_title('Lego dimensions', fontsize=20)
    ax.set_ylabel('Height', fontsize=14)
    ax.set_xlabel('Color', fontsize=14)
    ax.set_frame_on(False)
    ax.tick_params(axis='both', which='both', length=0)
    plt.show()

#Utilizando a câmera do smartphone e o App IP Webcan

ip = "https:/192.168.0.26:8080/video"

video = cv2.VideoCapture()

video.open(ip)

try:
    while(True):
        captura_ok, frame = video.read()
        if captura_ok:
            
            frame = cv2.resize(frame, (800, 400))
            
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            #

            mask_r = cv2.inRange(hsv_frame, lower_range_r, upper_range_r)

            mask_border_r = Image.fromarray(mask_r)

            bbox_r = mask_border_r.getbbox()
            
            #

            mask_g = cv2.inRange(hsv_frame, lower_range_g, upper_range_g)

            mask_border_g = Image.fromarray(mask_g)

            bbox_g = mask_border_g.getbbox()

            #

            mask_b = cv2.inRange(hsv_frame, lower_range_b, upper_range_b)

            mask_border_b = Image.fromarray(mask_b)

            bbox_b = mask_border_b.getbbox()
            
            #
            
            mask_y = cv2.inRange(hsv_frame, lower_range_y, upper_range_y)

            mask_border_y = Image.fromarray(mask_y)

            bbox_y = mask_border_y.getbbox()

            #

            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
            parameters = cv2.aruco.DetectorParameters()
            detector_2 = cv2.aruco.ArucoDetector(dictionary, parameters)

            corners, _, _ = detector_2.detectMarkers(frame)

            if corners:
                int_corners = np.intp(corners)
                print(int_corners)
                cv2.polylines(frame, int_corners, True, (0, 255, 0), 3)

                # Aruco Perimeter
                # A imagem capturada deve conter o QR Code para rodar
                aruco_perimeter = cv2.arcLength(corners[0],True)
                
                # Pixel to cm ratio
                pixel_cm_ratio = aruco_perimeter / 20

                if bbox_r is not None:
                    x1, y1, x2, y2 = bbox_r
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[0] = float(object_height)

                    cv2.putText(frame, "W {} cm".format(round(object_width, 1)), (int(x1), int(y1 - 30)),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                    cv2.putText(frame, "H {} cm".format(round(object_height, 1)), (int(x1), int(y1 - 15)),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

                if bbox_g is not None:
                    x1, y1, x2, y2 = bbox_g
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 128, 0), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[1] = float(object_height)

                    cv2.putText(frame, "W {} cm".format(round(object_width, 1)), (int(x1), int(y1 - 30)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 128, 0), 2)
                    cv2.putText(frame, "H {} cm".format(round(object_height, 1)), (int(x1), int(y1 - 15)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 128, 0), 2)

                if bbox_b is not None:
                    x1, y1, x2, y2 = bbox_b
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[3] = float(object_height)

                    cv2.putText(frame, "W {} cm".format(round(object_width, 1)), (int(x1), int(y1 - 30)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                    cv2.putText(frame, "H {} cm".format(round(object_height, 1)), (int(x1), int(y1 - 15)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                
                if bbox_y is not None:
                    x1, y1, x2, y2 = bbox_y
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[2] = float(object_height)

                    cv2.putText(frame, "W {} cm".format(round(object_width, 1)), (int(x1), int(y1 - 30)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
                    cv2.putText(frame, "H {} cm".format(round(object_height, 1)), (int(x1), int(y1 - 15)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
                    
            cv2.imshow("Video da Webcam", frame)
            
            key = cv2.waitKey(1)
            if key == 27:
                plotar_grafico(array_colors, array_colors_h)
                break
                
except KeyboardInterrupt:
    video.release()
    cv2.destroyAllWindows()
    print("Interrompido")