import numpy as np
import cv2
import json, os

publidDir = os.path.abspath( os.getcwd() + '/public' )
imagePath = publidDir + "/dataset/resizedimage.png"
jsonConfigFile = publidDir + "/data/coordinates.json"


width, height = (26, 26)
coordList = {'parkingspaces' : [], 'width': width, 'height': height}
globalID = 0

def draw_rectangle(event, x, y, flags, param):
	global globalID 
	if event == cv2.EVENT_LBUTTONDOWN:
		cv2.rectangle(img, (x-width/2, y+height/2), (x+width/2, y-height/2), (0, 255, 0))
		coordList['parkingspaces'].append({'x': x, 'y': y, 'globalID' : globalID + 1, 'lat': 3.4343, 'long': 4.4353})
		globalID += 1
		cv2.imshow('carlot', img)
	elif event == cv2.EVENT_RBUTTONDOWN:
		cv2.rectangle(img, (x-width/2, y+height/2), (x+width/2, y-height/2), (0, 0, 255))
		coordList['refX'] = x
		coordList['refY'] = y
		cv2.imshow('carlot', img)

img = cv2.imread(imagePath, 1)
cv2.imshow('carlot', img)

cv2.setMouseCallback('carlot', draw_rectangle)
key = cv2.waitKey()
f = open(jsonConfigFile, 'w')

jsonDump = json.dumps(coordList) 
f.write(str(jsonDump))
cv2.destroyAllWindows()

