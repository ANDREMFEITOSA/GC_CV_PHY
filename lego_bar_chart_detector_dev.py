import numpy as np 
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation
import colorsys

list_bar_h = []
list_bar_colors_rgb = []
list_bar_colors_rgb_ = []
list_bar_colors_rgb_string = []
list_bar_colors_hsv = []
list_h = []
list_s = []
list_v = []
pixel_cm_ratio = 1
array_categories = ['A', 'B', 'C', 'D']

list_lower_hsv = []
list_upper_hsv = []

list_mask = []
list_mask_border = []
list_bbox = []

#Função para detectar barras

def bar_detector():
    ip = "https:/192.168.0.26:8080/video"
    #ip = "https:/192.168.115.44:8080/video"

    video = cv2.VideoCapture()

    video.open(ip)
    
    while(True):
        captura_ok, frame = video.read()
        if captura_ok:
            
            frame = cv2.resize(frame, (300, 500))
            
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            mask = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)
            
            list_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            #cv2.drawContours(frame, list_contours, -1, (0, 255, 0), 1)
            
            bar_contours = []
            
            for cnt in list_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                #area = (x+w)*(y+h)
                
                area = cv2.contourArea(cnt)
                if area > 1000 and area < 10000:
                    bar_contours.append(cnt)
                    rect = cv2.minAreaRect(cnt)
                    #(x, y), (w, h), angle = rect
                    x, y, w, h = cv2.boundingRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    print(box)
                    #cv2.polylines(frame, [box], True, (255, 0, 0), 2)
                    #frame = cv2.rectangle(frame, (box[0][0], box[0][1]), (box[3][0], box[3][1]), (255, 0, 0), 2)
                    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                
                # if list_contours[i] is not None:
                #     x1, y1, x2, y2 = list_contours[i]
                    
                #     frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    
            cv2.imshow("Video da Webcam", frame)
            
            key = cv2.waitKey(1)
            if key == 13: #Enter
                return len(bar_contours) - 1
                break

#Função para plotar gráfico tipo bar
def plotar_grafico(colors_string, heights, colors):
    df = pd.DataFrame([heights], index = [colors_string])
    fig, ax = plt.subplots(figsize=(5, 5))
    g = ax.bar(np.array(colors_string), np.array(heights), width=0.25, color=np.array(colors))
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
    #ip = "https:/192.168.115.44:8080/video"

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
        # hL = (cv2.getTrackbarPos('H Lower','SETUP_COLOR'))/256
        # hH = (cv2.getTrackbarPos('H Higher','SETUP_COLOR'))/256
        # sL = (cv2.getTrackbarPos('S Lower','SETUP_COLOR'))/256
        # sH = (cv2.getTrackbarPos('S Higher','SETUP_COLOR'))/256
        # vL = (cv2.getTrackbarPos('V Lower','SETUP_COLOR'))/256
        # vH = (cv2.getTrackbarPos('V Higher','SETUP_COLOR'))/256

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

#n = int(input())
n = bar_detector()
print(n)

if n > 0:

    #Captura dos intervalos de cores HSV

    for i in range(n):
        
        l, u = setup_color()
        list_lower_hsv.append(l)
        list_upper_hsv.append(u)
        list_h.append(round((list_lower_hsv[i][0] + list_upper_hsv[i][0]*2)/3))
        list_s.append(round((list_lower_hsv[i][1] + list_upper_hsv[i][1]*2)/3))
        list_v.append(round((list_lower_hsv[i][2] + list_upper_hsv[i][2]*2)/3))
        # list_h.append(list_upper_hsv[i][0])
        # list_s.append(list_upper_hsv[i][1])
        # list_v.append(list_upper_hsv[i][2])
        list_bar_colors_hsv.append((list_h[i], list_s[i], list_v[i]))
        list_bar_colors_rgb.append(colorsys.hsv_to_rgb(round((list_h[i])/256, 2), round((list_s[i])/256, 2), round((list_v[i])/256, 2)))
        list_bar_colors_rgb_.append(colorsys.hsv_to_rgb(round(list_h[i]), round(list_s[i]), round(list_v[i])))
        #list_bar_colors_rgb_string.append("("+", ".join(map(str, list_bar_colors_rgb[i]))+")")
        list_bar_colors_rgb_string.append("(" + '{:,.1f}'.format(list_bar_colors_rgb[i][0]) + ", " + '{:,.1f}'.format(list_bar_colors_rgb[i][1]) + ", " + '{:,.1f}'.format(list_bar_colors_rgb[i][2]) + ")")

    #Utilizando a câmera do smartphone e o App IP Webcan  '{:,.1f}'.format()
    ip = "https:/192.168.0.26:8080/video"
    #ip = "https:/192.168.115.44:8080/video"

    #Algoritmo para detecção dos objetos e geração de gráficos digitais
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
                    #cv2.polylines(frame, int_corners, True, list_bar_colors_rgb[i], 3)

                    # Aruco Perimeter
                    aruco_perimeter = cv2.arcLength(corners[0],True)
                    
                    # Pixel to cm ratio
                    pixel_cm_ratio = aruco_perimeter / 20
                
                for i in range(n):
                    if list_bbox[i] is not None:
                        x1, y1, x2, y2 = list_bbox[i]
                        
                        #r, g, b = colorsys.hsv_to_rgb(list_h[i], list_s[i], list_v[i])
                        
                        #frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (r, g, b), 2)
                        # frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), list_bar_colors_rgb_[i], 2)

                        w = x2 - x1
                        h = y2 - y1
                        object_width = w / pixel_cm_ratio
                        object_height = h / pixel_cm_ratio
                        
                        list_bar_h.append(round(object_height - 0.18, 1)) #Desconto da altura do pino da peça de lego

                        cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                                        cv2.FONT_HERSHEY_PLAIN, 1, list_bar_colors_rgb_[i], 2)
                        # cv2.putText(frame, "{}".format(round(object_height - 0.18, 1)), (int(x1), int(y1 - 15)),
                        #                 cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

                print(list_bar_h)
                print(list_bar_colors_rgb_string)
                cv2.imshow("Video da Webcam", frame)
                key = cv2.waitKey(1)
                if key == 49: #1
                    plotar_grafico(list_bar_colors_rgb_string, list_bar_h, list_bar_colors_rgb)
                    break
                if key == 50: #2
                    plotar_grafico_stacked(array_categories, list_bar_h, list_bar_colors_rgb)
                    break
                #cv2.imshow("Video da Webcam", frame)
                
    except KeyboardInterrupt:
        video.release()
        cv2.destroyAllWindows()
        print("Interrompido")
else:
    print("Nehum fisicalização identificada")
