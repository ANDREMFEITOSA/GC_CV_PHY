import cv2
import numpy as np
#import dlib
import matplotlib.pyplot as plt

from scipy.spatial import distance as dist

from object_detector import *

from io import BytesIO
from IPython.display import clear_output, Image, display
from PIL import Image as Img

def padronizar_imagem(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (500, 400))
    return frame

def exibir_video(frame):
    img = Img.fromarray(frame, "RGB")
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    display(Image(data=buffer.getvalue()))
    clear_output(wait=True)

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

try:
    while(True):
        captura_ok, frame = video.read()
        if captura_ok:
            frame = padronizar_imagem(frame)

            #img = cv2.imread('C:/Users/User/Projetos/OpenCV/phone_aruco_marker.jpg')
            #img = cv2.imread(frame)

            detector = HomogeneousBgDetector()

            print(detector)

            contours = detector.detect_objects(frame)
            #contours = detector.detect_objects(img)

            print(contours)

            # Draw objects boundaries
            for cnt in contours:
                # Get rect
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect
                # Display rectangle
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                # box = np.int0(box)

                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.polylines(frame, [box], True, (255, 0, 0), 2)

                #cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                #cv2.polylines(img, [box], True, (255, 0, 0), 2)

            dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
            parameters = cv2.aruco.DetectorParameters()
            detector_2 = cv2.aruco.ArucoDetector(dictionary, parameters)

            corners, _, _ = detector_2.detectMarkers(frame)
            #corners, _, _ = detector_2.detectMarkers(img)

            if corners:
                # Draw polygon around the marker
                int_corners = np.intp(corners)
                print(int_corners)
                cv2.polylines(frame, int_corners, True, (0, 255, 0), 5)
                #cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

                # Aruco Perimeter
                aruco_perimeter = cv2.arcLength(corners[0],True)  # a imagem capturada deve conter o objeto aruco para funcionar
                # Pixel to cm ratio
                pixel_cm_ratio = aruco_perimeter / 20

                # Draw objects boundaries
                for cnt in contours:
                    # Get rect
                    rect = cv2.minAreaRect(cnt)
                    (x, y), (w, h), angle = rect
                    # Get Width and Height of the Objects by applying the Ratio pixel to cm
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio

                #cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
                            #cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                #cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                            #cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

                cv2.putText(frame, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                cv2.putText(frame, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

                cv2.imshow("Video da Webcam", frame)
                #exibir_video(frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break
except KeyboardInterrupt:
    video.release()
    cv2.destroyAllWindows()
    print("Interrompido")