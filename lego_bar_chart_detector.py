import numpy as np 
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
import colorsys
import bar_detector
import setup_hsv
import plot_bar_charts
import color_name

list_bar_h = []
list_h = []
list_s = []
list_v = []
list_bar_colors_hsv = []
list_bar_colors_rgb = []
list_bar_colors_rgb_percent = []
list_bar_colors_rgb_string = []
list_bar_color_name = []
list_lower_hsv = []
list_upper_hsv = []
list_mask = []
list_mask_border = []
list_bbox = []
pixel_cm_ratio = 1
#ip = "https:/192.168.0.26:8080/video"
ip = "https:/192.168.167.38:8080/video"


#Bar detection
n = bar_detector.bar_detector(ip)
print(n)

if n > 0:
    for i in range(n):
        #Capturing HSV color ranges
        l, u = setup_hsv.setup_color(ip)
        list_lower_hsv.append(l)
        list_upper_hsv.append(u)
        list_h.append(round((list_lower_hsv[i][0] + list_upper_hsv[i][0]*2)/3))
        list_s.append(round((list_lower_hsv[i][1]*2 + list_upper_hsv[i][1])/3))
        list_v.append(round((list_lower_hsv[i][2] + list_upper_hsv[i][2]*2)/3))
        list_bar_colors_hsv.append((list_h[i], list_s[i], list_v[i]))
        list_bar_colors_rgb_percent.append(colorsys.hsv_to_rgb(round((list_h[i])/256, 2), round((list_s[i])/256, 2), round((list_v[i])/256, 2)))
        list_bar_colors_rgb.append(colorsys.hsv_to_rgb(round(list_h[i]), round(list_s[i]), round(list_v[i])))
        list_bar_color_name.append(color_name.get_color_name(colorsys.hsv_to_rgb(round(list_h[i]), round(list_s[i]), round(list_v[i]))))
        list_bar_colors_rgb_string.append("(" + '{:,.1f}'.format(list_bar_colors_rgb_percent[i][0]) + ", " + '{:,.1f}'.format(list_bar_colors_rgb_percent[i][1]) + ", " + '{:,.1f}'.format(list_bar_colors_rgb_percent[i][2]) + ")")

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
                    print(int_corners)
                    cv2.polylines(frame, int_corners, True, (0, 255, 0), 3)
                    
                    # Aruco Perimeter
                    aruco_perimeter = cv2.arcLength(corners[0],True)
                    
                    # Pixel to cm ratio
                    pixel_cm_ratio = aruco_perimeter / 20
                
                for i in range(n):
                    if list_bbox[i] is not None:
                        x1, y1, x2, y2 = list_bbox[i]
                        
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), list_bar_colors_rgb[i], 2)

                        w = x2 - x1
                        h = y2 - y1
                        object_width = w / pixel_cm_ratio
                        object_height = h / pixel_cm_ratio
                        #Lego piece stud height discount
                        list_bar_h.append(round(object_height - 0.18, 1))

                        cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                        cv2.FONT_HERSHEY_PLAIN, 1, list_bar_colors_rgb[i], 2)
                        
                print(list_bar_h)
                print(list_bar_colors_rgb_string)
                cv2.imshow("Video da Webcam", frame)
                key = cv2.waitKey(1)
                if key == 13: #Enter
                    #Generating digital graphics
                    #plot_bar_charts.plotar_graficos(n, list_bar_color_rgb_string, list_bar_h, list_bar_colors_rgb_percent)
                    plot_bar_charts.plotar_graficos(n, list_bar_color_name, list_bar_h)
                    break
                
    except KeyboardInterrupt:
        video.release()
        cv2.destroyAllWindows()
        print("Interrupted")
else:
    print("No physicalization identified")
