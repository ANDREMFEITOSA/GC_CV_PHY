import numpy as np 
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation

array_colors_h = [0, 0, 0, 0]

array_colors = ['Red', 'Green', 'Blue', 'Yellow']

array_categories = ['A', 'B', 'C', 'D']

lower_range_r = np.array([0, 0, 0])
upper_range_r = np.array([0, 0, 0])
lower_range_b = np.array([0, 0, 0])
upper_range_b = np.array([0, 0, 0])
lower_range_y = np.array([0, 0, 0])
upper_range_y = np.array([0, 0, 0])
lower_range_o = np.array([0, 0, 0])
upper_range_o = np.array([0, 0, 0])

#Função para plotar gráfico tipo bar
def plotar_grafico(colors, heights):
    df = pd.DataFrame(heights, index=colors)
    fig, ax = plt.subplots(figsize=(5, 5))
    g = ax.bar(colors, heights, width=0.25, color=array_colors)
    ax.grid()
    ax.set_title('Bar Height x Color', fontsize=20)
    ax.set_ylabel('Height (cm)', fontsize=14)
    ax.set_xlabel('Color', fontsize=14)
    ax.set_frame_on(True)
    ax.tick_params(axis='both', which='both', length=0)
    ax.bar_label(g, fmt='{:,.1f}', padding = 3)
    plt.show()

#Função para plotar gráfico tipo stacked bar
def plotar_grafico_stacked(categories, heights, colors):
    df = pd.DataFrame(heights, index=categories)
    fig, ax = plt.subplots(figsize=(5, 5))
    g_red = ax.bar(categories[0], heights[0], width=0.10, align='center', color=array_colors[0])
    g_blue = ax.bar(categories[0], heights[1], width=0.10, bottom=heights[0], align='center', color=array_colors[1])
    g_yellow = ax.bar(categories[1], heights[2], width=0.10, align='center', color=array_colors[2])
    g_orange = ax.bar(categories[1], heights[3], width=0.10, bottom=heights[2], align='center', color=array_colors[3])
    ax.grid()
    ax.set_title('Stacked Bar', fontsize=20)
    ax.set_ylabel('Height (cm)', fontsize=14)
    ax.set_xlabel('Categoria', fontsize=14)
    ax.set_frame_on(True)
    ax.tick_params(axis='both', which='both', length=0)
    ax.bar_label(g_red, fmt='{:,.1f}', label_type='center', padding = 3)
    ax.bar_label(g_blue, fmt='{:,.1f}', label_type='center', padding = 3)
    ax.bar_label(g_yellow, fmt='{:,.1f}', label_type='center', padding = 3)
    ax.bar_label(g_orange, fmt='{:,.1f}', label_type='center', padding = 3)
    plt.show()

def nothing(x):
    pass

#Função para captura de intervalos de cores HSV
def setup_color():
    #ip = "https:/192.168.0.26:8080/video"
    ip = "https:/192.168.41.55:8080/video"

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

        lowerRegion = np.array([hL,sL,vL],np.uint8)
        upperRegion = np.array([hH,sH,vH],np.uint8)

        redObject = cv2.inRange(hsv,lowerRegion,upperRegion)

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
        
    return (lowerRegion, upperRegion)

#Captura dos intervalos de cores HSV
lower_range_r, upper_range_r = setup_color()

lower_range_b, upper_range_b = setup_color()

lower_range_y, upper_range_y = setup_color()

lower_range_o, upper_range_o = setup_color()

# lower_range_r = np.array([0, 218, 230])
# upper_range_r = np.array([6, 251, 255])
# lower_range_b = np.array([96,196, 198])
# upper_range_b = np.array([131,255,255])
# lower_range_y = np.array([18, 66, 246])
# upper_range_y = np.array([30, 128, 253])
# lower_range_o = np.array([13, 134, 255])
# upper_range_o = np.array([24, 182, 255])

#Utilizando a câmera do smartphone e o App IP Webcan
#ip = "https:/192.168.0.26:8080/video"
ip = "https:/192.168.41.55:8080/video"

#Algoritmo para detecção dos objetos e geração de gráficos digitais
video = cv2.VideoCapture()

video.open(ip)

try:
    while(True):
        captura_ok, frame = video.read()
        if captura_ok:
            
            frame = cv2.resize(frame, (300, 500))
            
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            #Red

            mask_r = cv2.inRange(hsv_frame, lower_range_r, upper_range_r)

            mask_border_r = Image.fromarray(mask_r)

            bbox_r = mask_border_r.getbbox()

            #Blue

            mask_b = cv2.inRange(hsv_frame, lower_range_b, upper_range_b)

            mask_border_b = Image.fromarray(mask_b)

            bbox_b = mask_border_b.getbbox()
            
            #Yellow
            
            mask_y = cv2.inRange(hsv_frame, lower_range_y, upper_range_y)

            mask_border_y = Image.fromarray(mask_y)

            bbox_y = mask_border_y.getbbox()

            #Orange
                         
            mask_o = cv2.inRange(hsv_frame, lower_range_o, upper_range_o)

            mask_border_o = Image.fromarray(mask_o)

            bbox_o = mask_border_o.getbbox()

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

                if bbox_r is not None:
                    x1, y1, x2, y2 = bbox_r
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[0] = round(object_height - 0.18, 1) #Desconto da altura do pino da peça de lego

                    cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

                if bbox_b is not None:
                    x1, y1, x2, y2 = bbox_b
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[1] = round(object_height - 0.18, 1)

                    cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                
                if bbox_y is not None:
                    x1, y1, x2, y2 = bbox_y
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[2] = round(object_height - 0.18, 1)

                    cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
                    
                if bbox_o is not None:
                    x1, y1, x2, y2 = bbox_o
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0,69,255), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[3] = round(object_height - 0.18, 1)

                    cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0,69,255), 2)
                    
            cv2.imshow("Video da Webcam", frame)
            
            key = cv2.waitKey(1)
            if key == 49: #1
                plotar_grafico(array_colors, array_colors_h)
                break
            if key == 50: #2
                plotar_grafico_stacked(array_categories, array_colors_h, array_colors)
                break
                
except KeyboardInterrupt:
    video.release()
    cv2.destroyAllWindows()
    print("Interrompido")