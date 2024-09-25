import numpy as np 
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
import colorsys

list_bar_h = []
list_bar_colors = []
list_h = []
list_s = []
list_v = []

array_categories = ['A', 'B', 'C', 'D']

list_lower_hsv = []
list_upper_hsv = []

list_mask = []
list_mask_border = []
list_bbox = []

n = int(input())

#Função para plotar gráfico tipo bar
def plotar_grafico(colors, heights):
    df = pd.DataFrame([heights], index = [colors])
    fig, ax = plt.subplots(figsize=(5, 5))
    g = ax.bar(colors, heights, width=0.25, color=colors)
    ax.grid()
    ax.set_title('Bar Height x Color', fontsize=20)
    ax.set_ylabel('Height (cm)', fontsize=14)
    ax.set_xlabel('Color', fontsize=14)
    ax.set_frame_on(True)
    ax.tick_params(axis='both', which='both', length=0)
    ax.bar_label(g, fmt='{:,.1f}', padding = 3)
    plt.show()

#Função para plotar gráfico tipo stacked bar
def plotar_grafico_stacked(n_bars, categories, heights, colors):
    df = pd.DataFrame(heights, index=categories)
    fig, ax = plt.subplots(figsize=(5, 5))
    list_g = []
    for i in range(n_bars): 
        list_g.append(ax.bar(categories[i], heights[i], width=0.10, align='center', color=colors[i]))
        list_g.append(ax.bar(categories[i+1], heights[i+1], width=0.10, align='center', color=colors[i+1]))
    
    for i in range(n_bars):
        ax.bar_label(list_g[i], fmt='{:,.1f}', label_type='center', padding = 3)
    
    ax.grid()
    ax.set_title('Stacked Bar', fontsize=20)
    ax.set_ylabel('Height (cm)', fontsize=14)
    ax.set_xlabel('Categoria', fontsize=14)
    ax.set_frame_on(True)
    ax.tick_params(axis='both', which='both', length=0)
    
    plt.show()

def nothing(x):
    pass

#Função para captura de intervalos de cores HSV
def setup_color():
    ip = "https:/192.168.0.26:8080/video"
    #ip = "https:/192.168.41.55:8080/video"

    video = cv2.VideoCapture()

    video.open(ip)

    cv2.namedWindow('SETUP_COLOR')

    cv2.createTrackbar('H Lower','SETUP_COLOR',0,179,nothing)
    cv2.createTrackbar('S Lower','SETUP_COLOR',0,255,nothing)
    cv2.createTrackbar('V Lower','SETUP_COLOR',0,255,nothing)
    cv2.createTrackbar('H Higher','SETUP_COLOR',179,179,nothing)
    cv2.createTrackbar('S Higher','SETUP_COLOR',255,255,nothing)
    cv2.createTrackbar('V Higher','SETUP_COLOR',255,255,nothing)

    while(1):
        _,img = video.read()
        img = cv2.flip(img,1)
        img = cv2.resize(img, (300, 500))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hL = cv2.getTrackbarPos('H Lower','SETUP_COLOR')
        hH = cv2.getTrackbarPos('H Higher','SETUP_COLOR')
        sL = cv2.getTrackbarPos('S Lower','SETUP_COLOR')
        sH = cv2.getTrackbarPos('S Higher','SETUP_COLOR')
        vL = cv2.getTrackbarPos('V Lower','SETUP_COLOR')
        vH = cv2.getTrackbarPos('V Higher','SETUP_COLOR')

        lower_region = np.array([hL,sL,vL],np.uint8)
        upper_region = np.array([hH,sH,vH],np.uint8)

        redObject = cv2.inRange(hsv,lower_region,upper_region)

        kernal = np.ones((1,1),"uint8")

        red = cv2.morphologyEx(redObject,cv2.MORPH_OPEN,kernal)
        red = cv2.dilate(red,kernal,iterations=1)

        res1=cv2.bitwise_and(img, img, mask = red)

        cv2.imshow("SETUP_COLOR",res1)

        key = cv2.waitKey(1)

        if key == 13: #Enter
            video.release()
            cv2.destroyAllWindows()
            break
        
    return (lower_region, upper_region)

#Captura dos intervalos de cores HSV

for i in range(n):
    
    l, u = setup_color()
    list_lower_hsv.append(l)
    list_upper_hsv.append(u)
    list_h.append((list_lower_hsv[i][0] + list_upper_hsv[i][0])/2)
    list_s.append((list_lower_hsv[i][1] + list_upper_hsv[i][1])/2)
    list_v.append((list_lower_hsv[i][2] + list_upper_hsv[i][2])/2)
    list_bar_colors.append((list_h[i], list_s[i], list_v[i]))
    

#Utilizando a câmera do smartphone e o App IP Webcan
ip = "https:/192.168.0.26:8080/video"
#ip = "https:/192.168.41.55:8080/video"

#Algoritmo para detecção dos objetos e geração de gráficos digitais
video = cv2.VideoCapture()

video.open(ip)

try:
    while(True):
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
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                        w = x2 - x1
                        h = y2 - y1
                        object_width = w / pixel_cm_ratio
                        object_height = h / pixel_cm_ratio
                        
                        list_bar_h.append(round(object_height - 0.18, 1)) #Desconto da altura do pino da peça de lego

                        cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                        cv2.FONT_HERSHEY_PLAIN, 1, colorsys.hsv_to_rgb(list_h[i], list_s[i], list_v[i]), 2)
    
            cv2.imshow("Video da Webcam", frame)
            
            key = cv2.waitKey(1)
            if key == 49: #1
                plotar_grafico(list_bar_colors, list_bar_h)
                break
            if key == 50: #2
                plotar_grafico_stacked(n, array_categories, list_bar_h, list_bar_colors)
                break
                
except KeyboardInterrupt:
    video.release()
    cv2.destroyAllWindows()
    print("Interrompido")