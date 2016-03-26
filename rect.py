import numpy as np
import cv2
import json
coordList = {'parkingspaces' : []}
globalID = 0
def draw_rectangle(event, x, y, flags, param):
    global globalID 
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(img, (x-13, y+13), (x+13, y-13), (0, 255, 0))
        coordList['parkingspaces'].append({'x': x, 'y': y, 'globalID' : globalID + 1, 'lat': 3.4343, 'long': 4.4353})
        globalID += 1
        cv2.imshow('carlot', img)
    elif event == cv2.EVENT_RBUTTONDOWN:
        coordList['refX'] = x
        coordList['refY'] = y
img = cv2.imread("resizedimage.png", 1)
cv2.imshow('carlot', img)
cv2.setMouseCallback('carlot', draw_rectangle)
key = cv2.waitKey()
print coordList
f = open('jsonCoords', 'w')
jsonDump = json.dumps(coordList) 
f.write(str(jsonDump))
cv2.destroyAllWindows()


