import cv2
import numpy as np

#Auxiliary function to the setup_color() function
def nothing(x):
    pass

#Function for capturing HSV color ranges
def setup_color(ip):
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
