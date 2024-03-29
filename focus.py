import numpy as np
import cv2
 
VIDEO = 'cle9-1_1_1_1_U.avi'
DILATION = 5
DILATION_ITER = 5
BLURSIZE = 101
 
cap = cv2.VideoCapture(VIDEO)


HEAT = None
HEATDIV = None
iter = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    if iter == 0:
        HEAT = np.zeros_like(frame[:,:,0]).astype('float64')
        HEATDIV = np.zeros_like(frame[:,:,0]).astype('float64')
    if ret == False:
	    break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
    edges = cv2.Canny(image=gray, threshold1=90, threshold2=90)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(DILATION,DILATION))
    edges = cv2.dilate(edges,kernel,iterations = DILATION_ITER)
    blur = cv2.GaussianBlur(edges,(BLURSIZE,BLURSIZE),0)
	
    frame[:,:,0] = blur[:,:]
    blur = blur.astype('float64')/255

    MASK = (HEATDIV < blur)

    HEAT[MASK] = np.zeros_like(HEAT)[MASK]+iter

    HEATDIV[MASK] = blur[MASK]

    cv2.imshow('heatmap', HEAT/np.max(HEAT))
    cv2.imshow('frame', frame)
	
    iter += 1	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.imwrite(VIDEO.replace('.avi','_heat.png'), (HEAT/np.max(HEAT)*255).astype("uint8"))

cap = cv2.VideoCapture(VIDEO)
OUT = None
iter = 0
while True:
    ret, frame = cap.read()
    if iter == 0:
        OUT = frame[:,:,0].astype('float64')/255
    if ret == False:
	    break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype('float64')/255
    MASK = (HEAT==iter)
    OUT[MASK] = gray[MASK]
	
    #cv2.imshow('mask', MASK.astype("float64"))
    cv2.imshow('frame', OUT)
    iter += 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


cv2.imwrite(VIDEO.replace('.avi','.png'), (OUT*255).astype("uint8"))
