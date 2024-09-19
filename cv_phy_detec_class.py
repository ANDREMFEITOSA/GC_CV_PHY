import numpy as np 
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import animation

array_colors_h = [0, 0, 0]

array_colors = ['r', 'b', 'y']

lower_range_r = np.array([0, 0, 0])
upper_range_r = np.array([0, 0, 0])
lower_range_b = np.array([0, 0, 0])
upper_range_b = np.array([0, 0, 0])
lower_range_y = np.array([0, 0, 0])
upper_range_y = np.array([0, 0, 0])

def plotar_grafico(colors, heights):
    df = pd.DataFrame(heights, index=colors)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(colors, heights, width=0.5, color=array_colors)
    ax.grid()
    ax.set_title('Bar dimensions', fontsize=20)
    ax.set_ylabel('Height', fontsize=14)
    ax.set_xlabel('Color', fontsize=14)
    ax.set_frame_on(False)
    ax.tick_params(axis='both', which='both', length=0)
    plt.show()

def nothing(x):
    pass

def setup():
    ip = "https:/192.168.0.26:8080/video"
    #ip = "https:/192.168.0.100:8080/video"

    video = cv2.VideoCapture()

    video.open(ip)

    ###

    cv2.namedWindow('marking')

    cv2.createTrackbar('H Lower','marking',0,179,nothing)
    cv2.createTrackbar('S Lower','marking',0,255,nothing)
    cv2.createTrackbar('V Lower','marking',0,255,nothing)
    cv2.createTrackbar('H Higher','marking',179,179,nothing)
    cv2.createTrackbar('S Higher','marking',255,255,nothing)
    cv2.createTrackbar('V Higher','marking',255,255,nothing)

    while(1):
        _,img = video.read()
        img = cv2.flip(img,1)
        img = cv2.resize(img, (300, 500))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hL = cv2.getTrackbarPos('H Lower','marking')
        hH = cv2.getTrackbarPos('H Higher','marking')
        sL = cv2.getTrackbarPos('S Lower','marking')
        sH = cv2.getTrackbarPos('S Higher','marking')
        vL = cv2.getTrackbarPos('V Lower','marking')
        vH = cv2.getTrackbarPos('V Higher','marking')

        lowerRegion = np.array([hL,sL,vL],np.uint8)
        upperRegion = np.array([hH,sH,vH],np.uint8)

        redObject = cv2.inRange(hsv,lowerRegion,upperRegion)

        kernal = np.ones((1,1),"uint8")

        red = cv2.morphologyEx(redObject,cv2.MORPH_OPEN,kernal)
        red = cv2.dilate(red,kernal,iterations=1)

        res1=cv2.bitwise_and(img, img, mask = red)

        cv2.imshow("Masking ",res1)

        if cv2.waitKey(10) & 0xFF == ord('q'): #Enter
            video.release()
            cv2.destroyAllWindows()
            break    
    return (lowerRegion, upperRegion)

lower_range_r, upper_range_r = setup()

lower_range_b, upper_range_b = setup()

lower_range_y, upper_range_y = setup()

#Utilizando a câmera do smartphone e o App IP Webcan

ip = "https:/192.168.0.26:8080/video"

video = cv2.VideoCapture()

video.open(ip)

try:
    while(True):
        captura_ok, frame = video.read()
        if captura_ok:
            
            frame = cv2.resize(frame, (300, 500))
            
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            #

            mask_r = cv2.inRange(hsv_frame, lower_range_r, upper_range_r)

            mask_border_r = Image.fromarray(mask_r)

            bbox_r = mask_border_r.getbbox()

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

                if bbox_b is not None:
                    x1, y1, x2, y2 = bbox_b
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    w = x2 - x1
                    h = y2 - y1
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio
                    
                    array_colors_h[2] = float(object_height)

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
                    
                    array_colors_h[3] = float(object_height)

                    cv2.putText(frame, "W {} cm".format(round(object_width, 1)), (int(x1), int(y1 - 30)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
                    cv2.putText(frame, "H {} cm".format(round(object_height, 1)), (int(x1), int(y1 - 15)),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
                    
            cv2.imshow("Video da Webcam", frame)
            
            key = cv2.waitKey(1)
            if key == 27: #Esc
                plotar_grafico(array_colors, array_colors_h)
                break
                
except KeyboardInterrupt:
    video.release()
    cv2.destroyAllWindows()
    print("Interrompido")