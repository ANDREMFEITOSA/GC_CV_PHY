import numpy as np
import cv2
from PIL import Image #para a obtenção das bordas de caixa

def get_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

def padronizar_imagem(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (500, 400))
    return frame

def padronizar_imagem_hsv(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.resize(frame, (500, 400))
    return frame

yellow = [0, 255, 255] #amarelo em BGR colorspace
green = [0, 128, 0] #verde em BGR colorspace
red = [0, 0, 255] #vermelho em BGR
blue = [255, 0, 0] #vermelho em BGR

# lower_range_r = np.array([126, 188, 47])
# upper_range_r = np.array([179, 255, 255])
# lower_range_g = np.array([66, 155, 40])
# upper_range_g = np.array([98, 255, 255])
# lower_range_y = np.array([88, 176, 70])
# upper_range_y = np.array([133, 255, 255])
# lower_range_b = np.array([110,50,50])
# upper_range_b = np.array([130,255,255])

lower_range_r = np.array([0, 153, 0])
upper_range_r = np.array([17, 255, 200])
lower_range_g = np.array([50, 109, 43])
upper_range_g = np.array([88, 212, 120])
lower_range_y = np.array([0, 191, 0])
upper_range_y = np.array([82, 255, 255])
lower_range_b = np.array([0,222,130])
upper_range_b = np.array([179,255,255])

video = cv2.VideoCapture(0)
#video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

try:
    while(True):
        captura_ok, frame = video.read()
        if captura_ok:
            #frame = padronizar_imagem(frame)
            
            #hsv_frame = padronizar_imagem_hsv(frame)

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


            #lowerLimit_g, upperLimit_g = get_limits(color = yellow)

            #mask_g = cv2.inRange(hsv_frame, lowerLimit_g, upperLimit_g)

            mask_g = cv2.inRange(hsv_frame, lower_range_g, upper_range_g)

            mask_border_g = Image.fromarray(mask_g)

            bbox_g = mask_border_g.getbbox()

           
            #lowerLimit_y, upperLimit_y = get_limits(color = yellow)

            #mask_y = cv2.inRange(hsv_frame, lowerLimit_y, upperLimit_y)

            mask_y = cv2.inRange(hsv_frame, lower_range_y, upper_range_y)

            mask_border_y = Image.fromarray(mask_y)

            bbox_y = mask_border_y.getbbox()


            #lowerLimit_r, upperLimit_r = get_limits(color = red)

            #mask_r = cv2.inRange(hsv_frame, lowerLimit_r, upperLimit_r)

            mask_r = cv2.inRange(hsv_frame, lower_range_r, upper_range_r)

            mask_border_r = Image.fromarray(mask_r)

            bbox_r = mask_border_r.getbbox()


            # lowerLimit_b, upperLimit_b = get_limits(color = blue)

            # mask_b = cv2.inRange(hsv_frame, lowerLimit_b, upperLimit_b)

            mask_b = cv2.inRange(hsv_frame, lower_range_b, upper_range_b)

            mask_border_b = Image.fromarray(mask_b)

            bbox_b = mask_border_b.getbbox()



            #print(bbox)

            if bbox_r is not None:
                x1, y1, x2, y2 = bbox_r
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

            if bbox_g is not None:
                x1, y1, x2, y2 = bbox_g
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 128, 0), 5)

            if bbox_y is not None:
                x1, y1, x2, y2 = bbox_y
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 5)

            if bbox_b is not None:
                x1, y1, x2, y2 = bbox_b
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

            cv2.imshow("Video da Webcam", frame)
            #cv2.imshow("Video da Webcam", mask_r)
                #exibir_video(frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
     
except KeyboardInterrupt:
    video.release()
    cv2.destroyAllWindows()
    print("Interrompido")