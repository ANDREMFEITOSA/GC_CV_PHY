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

list_lower_hsv = []
list_upper_hsv = []
list_h = []
list_s = []
list_v = []
list_bar_colors_rgb_percent = []
list_bar_color_name = []
list_bar_colors_rgb_string = []

list_lower_rgb = []
list_upper_rgb = []
list_average_rgb = []
list_bar_color_name_ = []
list_bar_colors_rgb_string_ = []

list_mask = []
list_mask_border = []
list_bbox = []
pixel_cm_ratio = 1
list_bar_h = []
ip = "https:/192.168.0.26:8080/video"
#ip = "https:/192.168.167.38:8080/video"
#ip = "https:/10.16.0.204:8080/video"

#Bar detection
n = 4
list_lower_hsv = [(0, 230, 185), (60, 235, 160), (95, 125, 205), (20, 80, 235)]
list_upper_hsv = [(5, 255, 255), (75, 255, 210), (120, 255, 255), (35, 255, 255)]
            
list_lower_rgb.append(np.array(colorsys.hsv_to_rgb(0/255, 230/255, 185/255)))
list_lower_rgb.append(np.array(colorsys.hsv_to_rgb(60/255, 235/255, 160/255)))
list_lower_rgb.append(np.array(colorsys.hsv_to_rgb(95/255, 125/255, 205/255)))
list_lower_rgb.append(np.array(colorsys.hsv_to_rgb(20/255, 80/255, 235/255)))
        
list_upper_rgb.append(np.array(colorsys.hsv_to_rgb(5/255, 255/255, 255/255)))
list_upper_rgb.append(np.array(colorsys.hsv_to_rgb(75/255, 255/255, 210/255)))
list_upper_rgb.append(np.array(colorsys.hsv_to_rgb(120/255, 255/255, 255/255)))
list_upper_rgb.append(np.array(colorsys.hsv_to_rgb(35/255, 255/255, 255/255)))

# n = bar_detector.bar_detector(ip)
# print(n)

if n > 0:
    for i in range(n):
        #Capturing HSV color ranges
        # l, u = setup_hsv.setup_color(ip)
        
        # list_lower_hsv.append(l)
        # list_upper_hsv.append(u)
        list_h.append(round((list_lower_hsv[i][0] + list_upper_hsv[i][0])/2, 2))
        list_s.append(round((list_lower_hsv[i][1] + list_upper_hsv[i][1])/2, 2))
        list_v.append(round((list_lower_hsv[i][2] + list_upper_hsv[i][2])/2, 2))
        list_bar_colors_rgb_percent.append(colorsys.hsv_to_rgb(round((list_h[i])/255, 2), round((list_s[i])/255, 2), round((list_v[i])/255, 2)))
        list_bar_color_name.append(color_name.get_color_name((list_bar_colors_rgb_percent[i][0]*255, list_bar_colors_rgb_percent[i][1]*255, list_bar_colors_rgb_percent[i][2]*255)))
        list_bar_colors_rgb_string.append("(" + '{:,.1f}'.format(list_bar_colors_rgb_percent[i][0]) + ", " + '{:,.1f}'.format(list_bar_colors_rgb_percent[i][1]) + ", " + '{:,.1f}'.format(list_bar_colors_rgb_percent[i][2]) + ")")
       
        # list_lower_rgb.append(colorsys.hsv_to_rgb(l[0]/255, l[1]/255, l[2]/255))
        # list_upper_rgb.append(colorsys.hsv_to_rgb(u[0]/255, u[1]/255, u[2]/255))
        list_average_rgb.append([(list_lower_rgb[i][0]+list_upper_rgb[i][0])/2, (list_lower_rgb[i][1]+list_upper_rgb[i][1])/2, (list_lower_rgb[i][2]+list_upper_rgb[i][2])/2])
        list_bar_color_name_.append(color_name.get_color_name((list_average_rgb[i][0]*255, list_average_rgb[i][1]*255, list_average_rgb[i][2]*255)))
        list_bar_colors_rgb_string_.append("(" + '{:,.1f}'.format(list_average_rgb[i][0]) + ", " + '{:,.1f}'.format(list_average_rgb[i][1]) + ", " + '{:,.1f}'.format(list_average_rgb[i][2]) + ")")

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
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (list_average_rgb[i][0]*255, list_average_rgb[i][1]*255, list_average_rgb[i][2]*255, 2))
                        w = x2 - x1
                        h = y2 - y1
                        object_width = w / pixel_cm_ratio
                        object_height = h / pixel_cm_ratio
                        
                        #Lego piece stud height discount
                        list_bar_h.append(round(object_height - 0.18, 1))

                        cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (list_average_rgb[i][0]*255, list_average_rgb[i][1]*255, list_average_rgb[i][2]*255, 2))
                        
                print('Height: ', list_bar_h)
                print('Average RGB: ', list_average_rgb)
                print('Average RGB Color name:', list_bar_color_name_)
                print('Percent RGB', list_bar_colors_rgb_percent)
                print('HSV to RGB Color Name: ', list_bar_color_name)
                cv2.imshow("Video da Webcam", frame)
                key = cv2.waitKey(1)
                if key == 13: #Enter
                    
                    #Generating digital graphics
                    #plot_bar_charts.plotar_graficos_(n, list_bar_color_name_, list_bar_h)
                    plot_bar_charts.plotar_graficos_(n, list_bar_color_name, list_bar_h)
                    break
                
    except KeyboardInterrupt:
        video.release()
        cv2.destroyAllWindows()
        print("Interrupted")
else:
    print("No physicalization identified")
