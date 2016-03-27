# Note: Run this file from the root directroy like the below.
# > python python/detector.py 

import numpy as np
import cv2
import json, os, csv
from pprint import pprint
from collections import defaultdict


publidDir = os.path.abspath( os.getcwd() + '/public' )
imagePath = publidDir + "/dataset/resizedimage.png"
jsonConfigFile = publidDir + "/data/coordinates.json"
csvFilePath = publidDir + "/data/metrics0.csv"
threshold = {
	'0' :  0.355,
	'1' : 3.3,
	'2' : 0.5
}

class ColorHistogram(object):

	def __init__(self, args):
		self.image = args.get('image', None)

	def getHueHistogram(self, minSaturation=0):
		# Convert the image to HSV space
		hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

		mask = None

		# Mask out the low saturated pixels
		if(minSaturation > 0):
			hue, saturation, value = cv2.split(self.image)
			retval, mask = cv2.threshold(saturation, minSaturation, 255, cv2.THRESH_BINARY)

		# calculate 1D histogram
		hueRanges = [0, 180]
		hist = cv2.calcHist(
			[self.image], # list of images
			[ 0 ],	# compute histogram for the HUE channel('0' index) alone
			mask,	# Mask for elimiating low saturation values
			[ 180 ],	# Number of histogram bins
			hueRanges	# range to compute histogram  
		)
		hist = cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
#		print "hist: {0}".format(str(json.dumps(hist)))

		return hist

class ImageComparator(object):
	def __init__(self, args):
		self.colorReductionFactor = args.get('colorReductionFactor', None)
		self.minSaturation = args.get('minSaturation', 0)

		self.referenceImage = args.get('referenceImage', None)
		self.referenceHistogram = args.get('referenceHistogram', ColorHistogram({
			'image' : self.referenceImage
		}).getHueHistogram(self.minSaturation))


	def compare(self, inputImage, methodDict):
		inputImageHistogram = ColorHistogram({
			'image' : inputImage
		}).getHueHistogram(self.minSaturation)

		print "\t\t--------------"
		for method in xrange(4):
			result = cv2.compareHist(self.referenceHistogram, inputImageHistogram, method)
			methodDict[method].append({'id': method, 'result':round(result, 3)})
			print "Method {0}: {1}".format(method, result)

        def compareDiff(self, referenceImage, inputImage):
            grayscaleBackground = cv2.cvtColor(referenceImage, cv2.COLOR_RGB2GRAY)
            grayscaleImage = cv2.cvtColor(inputImage, cv2.COLOR_RGB2GRAY)
            diff = cv2.absdiff(grayscaleBackground, grayscaleImage)
            return cv2.sumElems(diff)



		

# Does img[y: y + h, x: x + w]
def getPatchFromImage(image, x, y, w, h):
	x, y = x-w/2, y+h/2
	return image[y: y + h, x: x + w]

image = cv2.imread(imagePath, cv2.IMREAD_COLOR)

# Resize the image by exactly half
# resizedImage = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

# read the config json file that contains reference patch and the parking lot informations
# {
# 	'parkingspaces'	: [
#		[x1, y1],	# point(x,y) of the mouse selection which will be the midpoint of the parking patch
#		[x2, y2],
#		....
#	],
# 	'referencespaces' : [
#		[x1, y1], # point(x,y) of the mouse selection which will be the midpoint of the reference patch
#		[x2, y2],
#		....
#	]
#	'patchwidth' : width,
#	'patchheight' : height,
# }

datadict = defaultdict(dict)
imageComparator = None
width, height = (0, 0)
methodDict = {
	0 : [],
	1 : [],
	2 : [],
	3 : [],
}

with open(jsonConfigFile) as data_file:
	coordinatesData = json.load(data_file)

	width, height = (coordinatesData['width'], coordinatesData['height'])
	referenceImage = getPatchFromImage(image, coordinatesData['refX'], coordinatesData['refY'], width, height)

	# load the reference image
	imageComparator = ImageComparator({
		'referenceImage' : referenceImage
	})

	index = 1
        newDict = {}
	for parkingRow in coordinatesData['parkingspaces']:
		patchImage = getPatchFromImage(image, parkingRow['x'], parkingRow['y'], width, height)
		print "No: %d" % (index)
		imageComparator.compare(patchImage, methodDict)
                newDict[index] = imageComparator.compareDiff(referenceImage, patchImage)

		index += 1

        for key in newDict:
            print "No: " + str(key) + " " + str(newDict[key])

	for key in methodDict:
		print "method: %d" %(key)
		for data in methodDict[key]:
			print "{1},".format(data['id'], data['result']),
		print "------\n"

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('method 0', cv2.WINDOW_NORMAL)
cv2.namedWindow('method 1', cv2.WINDOW_NORMAL)
cv2.namedWindow('method 2', cv2.WINDOW_NORMAL)

cv2.imshow('image', image)
cv2.imshow('method 0', image)
cv2.imshow('method 1', image)
cv2.imshow('method 2', image)


cv2.waitKey(0)
cv2.destroyAllWindows()
