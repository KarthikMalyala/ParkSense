# ParkSense Edge Detection
# Karthik Malyala
# 4/20/2022

# Imports the required libraries
import time
import cv2
import numpy as np
import pymongo

#--------------------------MongoDB Connection---------------------------------
client = pymongo.MongoClient("mongodb+srv://client:Hello1234@cluster0.izjuq.mongodb.net/parksense?retryWrites=true&w=majority")
db = client.parksense
demo = db.demolot

#---------------------------Camera Image Capture---------------------------------
def capture():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(2)
    def get():
        retval, frame = cam.read()
        return frame

    print("Capturing Image")
    cameraCap = get()

    file = "curProcess.png"
    cv2.imwrite(file, cameraCap)

#--------------------------Canny Edge Algorithm--------------------------------
def canny(image, sigma=0.90):
    # Computes the median for the pixel intensities of the single channel
    med = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * med))
    upper = int(min(255, (1.0 + sigma) * med))
    edged = cv2.Canny(image, lower, upper)

    # Returns the edged image
    return edged

#-------------------------Count of Edges in an Image------------------
def edgeCount(edges,x1,y1,x2,y2):
    count=0

    for y in range(y1,y2):
        for x in range(x1,x2):
            if edges[y][x] != 0:
                count+=1
    return count

#--------------------------Driver Code-----------------------------------------
while(True):
    capture()
    img = cv2.imread("curProcess.png")
    edges = canny(img)

    # cv2.rectangle(edges, (165, 88), (328, 200), (255,0,0), 2)
    # cv2.rectangle(edges, (165, 202), (325, 330), (255,0,0), 2)
    # cv2.rectangle(edges, (330, 88), (475, 200), (255,0,0), 2)
    # cv2.rectangle(edges, (330, 205), (475, 330), (255,0,0), 2)

    slotOne = edgeCount(edges, 165, 88, 328, 200)
    slotTwo = edgeCount(edges, 165, 202, 325, 330)
    slotThree = edgeCount(edges, 330, 88, 475, 200)
    slotFour = edgeCount(edges, 330, 205, 475, 330)

    slots = [slotOne, slotTwo, slotThree, slotFour]

    for s in slots:
        print(s)
        if s > 2500:
            slots[slots.index(s)] = "full"
        else:
            slots[slots.index(s)] = "empty"

    topRow = [slots[0], slots[2]]
    bottomRow = [slots[1], slots[3]]

    #------------Sends the Data to Database----------------
    demo.insert_one({
        "date": int(time.time()),
        "size": [
            2,
            2
        ],
        "spots": [
            topRow,
            bottomRow
        ],
        "name": "demolot"
    })
    # cv2.imshow("ParkSense", edges)
    # cv2.waitKey(1)
    print(slots)
    time.sleep(2)