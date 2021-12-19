# -*- coding:utf-8 -*-
import urllib2
import urllib
import time
import cv2
img = cv2.imread("timg.jpg")
cv2.namedWindow('original')
cv2.imshow('original', img)
http_url='https://api-cn.faceplusplus.com/humanbodypp/beta/detect'
key = "NXmXboI0SV-ueLXhToLHuHCtGJAi1cad"
secret = "DebehXM7hLcARZoU64zSQRO6lMGqR7NT"
filepath = r"timg.jpg"
boundary = '----------%s' % hex(int(time.time() * 1000))
data = []
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
data.append(key)
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
data.append(secret)
data.append('--%s' % boundary)
fr=open(filepath,'rb')
data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
data.append('Content-Type: %s\r\n' % 'application/octet-stream')
data.append(fr.read())
fr.close()
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
data.append('1')
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
data.append("")
data.append('--%s--\r\n' % boundary)

http_body='\r\n'.join(data)
#buld http request
req=urllib2.Request(http_url)
#header
req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
req.add_data(http_body)
try:
	#req.add_header('Referer','http://remotserver.com/')
	#post data to server
	resp = urllib2.urlopen(req, timeout=5)
	#get response
	qrcont=resp.read()
	#print qrcont

except urllib2.HTTPError as e:
    print e.read()

mydict = eval(qrcont)
humanbodies = mydict["humanbodies"]
faceNum = len(humanbodies)
print("识别到了%d个人"%(faceNum))

for i in range(faceNum):
    humanbody_rectangle = humanbodies[i]['humanbody_rectangle']
    width =  humanbody_rectangle['width']
    top =  humanbody_rectangle['top']
    left =  humanbody_rectangle['left']
    height =  humanbody_rectangle['height']
    start = (left, top)
    end = (left+width, top+height)
    color = (55,255,155)
    thickness = 3
    cv2.rectangle(img, start, end, color, thickness)

cv2.namedWindow('recognition')
cv2.imshow('recognition', img)

cv2.waitKey(0)
cv2.destroyAllWindows()