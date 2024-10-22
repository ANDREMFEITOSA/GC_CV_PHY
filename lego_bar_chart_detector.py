import numpy as np 
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
import colorsys
import webcolors
import bar_detector
import setup_hsv
import plot_graphs
import color_name

list_lower_hsv = []
list_upper_hsv = []
list_lower_rgb = []
list_upper_rgb = []
list_average_rgb = []
list_bar_color_name = []

list_mask = []
list_mask_border = []
list_bbox = []
pixel_cm_ratio = 1
list_bar_h = []
ip = "https:/192.168.64.65:8080/video"

#Bar detection
n = bar_detector.bar_detector(ip)
print(n)

if n > 0:
    for i in range(n):
        #Capturing HSV color ranges
        l, u = setup_hsv.setup_color(ip)
        list_lower_hsv.append(l)
        list_upper_hsv.append(u)
       
        list_lower_rgb.append(colorsys.hsv_to_rgb(l[0]/255, l[1]/255, l[2]/255))
        list_upper_rgb.append(colorsys.hsv_to_rgb(u[0]/255, u[1]/255, u[2]/255))
        list_average_rgb.append([round((list_lower_rgb[i][0]+list_upper_rgb[i][0])*255/2), round((list_lower_rgb[i][1]+list_upper_rgb[i][1])*255/2), round((list_lower_rgb[i][2]+list_upper_rgb[i][2])*255/2)])
        list_bar_color_name.append(color_name.get_color_name((list_average_rgb[i][0], list_average_rgb[i][1], list_average_rgb[i][2])))

    #Module for detecting objects by color
    video = cv2.VideoCapture()
    video.open(ip)
    
    try:
        while(True):
            list_mask.clear()
            list_mask_border.clear()
            list_bbox.clear()
            list_bar_h.clear()
            captura_ok, frame = video.read()
            
            if captura_ok:
                frame = cv2.resize(frame, (300, 500))
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                for i in range(n):
                    list_mask.append(cv2.inRange(hsv_frame, list_lower_hsv[i], list_upper_hsv[i]))
                    list_mask_border.append(Image.fromarray(list_mask[i]))
                    list_bbox.append(list_mask_border[i].getbbox())

                #Aruco detector
                dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
                parameters = cv2.aruco.DetectorParameters()
                detector_2 = cv2.aruco.ArucoDetector(dictionary, parameters)
                corners, _, _ = detector_2.detectMarkers(frame)

                if corners:
                    int_corners = np.intp(corners)
                    cv2.polylines(frame, int_corners, True, (0, 255, 0), 3)
                    
                    # Aruco Perimeter
                    aruco_perimeter = cv2.arcLength(corners[0],True)
                    
                    # Pixel to cm ratio
                    pixel_cm_ratio = aruco_perimeter / 20
                
                for i in range(n):
                    if list_bbox[i] is not None:
                        x1, y1, x2, y2 = list_bbox[i]
                        r, g, b = webcolors.name_to_rgb(list_bar_color_name[i])
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (b, g, r, 2))
                        w = x2 - x1
                        h = y2 - y1
                        object_width = w / pixel_cm_ratio
                        object_height = h / pixel_cm_ratio
                        
                        #Lego piece stud height discount
                        list_bar_h.append(round(object_height - 0.18, 2))

                        cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)),
                                    (int(x1), int(y1 - 15)), cv2.FONT_HERSHEY_PLAIN, 1, (b, g, r, 2))
                        
                print('Height: ', list_bar_h)
                print('Average RGB: ', list_average_rgb)
                print('Average RGB Color name:', list_bar_color_name)
                cv2.imshow("Video da Webcam", frame)
                key = cv2.waitKey(1)
                if key == 13: #Enter
                    
                    #Generating digital graphics
                    plot_graphs.plot_bar_pie_graphs(list_bar_h, list_bar_color_name)
                    break
    except KeyboardInterrupt:
        video.release()
        cv2.destroyAllWindows()
        print("Interrupted")
else:
    print("No physicalization identified")
