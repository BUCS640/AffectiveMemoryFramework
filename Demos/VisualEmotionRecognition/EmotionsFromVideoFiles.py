import modelLoader
import modelDictionary
import imageProcessingUtil
import GUIController
import numpy
import os
import cv2
import PerceptionGWR
import io

def get_img_from_fig(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180)
    buf.seek(0)
    img_arr = numpy.frombuffer(buf.getvalue(), dtype=numpy.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640,480))

    return img


def createPlot(arousal, valence, left):
    import matplotlib.pyplot as plt

    # plot sin wave
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.xlabel('Arousal')
    plt.ylabel('Valence')
    plt.scatter(arousal, valence, color='r')
    if left:
        plt.savefig("plotLeft.png")
    else:
        plt.savefig(
            "plotRight.png")

    # figure = plt.figure()
    # figure.canvas.draw()
    # figure = get_img_from_fig(fig)
    #
    # return figure

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)



finalImageSizeLeft = (1664,1079) # Size of the final image generated by the demo
finalImageSizeRight = (1535,1079) # Size of the final image generated by the demo
faceDetectionMaximumFrequency = 1000 # Frequency that a face will be detected: every X frames.
faceSize = (64,64) # Input size for both models: categorical and dimensional

modelDimensional = modelLoader.modelLoader(modelDictionary.DimensionalModel)

imageProcessing = imageProcessingUtil.imageProcessingUtil(faceDetectionMaximumFrequency)

GUIController = GUIController.GUIController()



videoDirectory = "/home/pablo/Documents/Datasets/Videotest/Anna-Tobii.mp4"
saveInRight = "/home/pablo/Documents/Datasets/Videotest/Anna-Tobii"

arousalLeft = []
valenceLeft = []

arousalRight = []
valenceRight = []

createPlot(arousalLeft, valenceLeft, False)
createPlot(arousalLeft, valenceLeft, True)

cap = cv2.VideoCapture(videoDirectory)

totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
numberOfImages = 0
check = True
flag = True
imageNumber = 0
lastImageWithFaceDetected = 0

numberImg = 0

currentFrame = 0
previousFigure = []
while (check):
        check, img = cap.read()
        if img is not None:
            print ("Frame " + str(numberImg) + "/" + str(totalFrames))
            img = cv2.resize(img, (1024,768))
            img2 = img.copy
            #cv2.imwrite("imgTmp.png", img)
            facePoints, face = imageProcessing.detectFace(img)

            image = numpy.zeros((finalImageSizeRight[1], finalImageSizeRight[0], 3), numpy.uint8)
            image[0:768, 0:1024] = img
            img = image

            img = GUIController.createDetectedFacGUI(img, facePoints, None,[])
            #cv2.imwrite("imgTmp.png", img)
            if not len(face) == 0:
               # print("Processing face")
                face = imageProcessing.preProcess(face, faceSize)
                #print("Dimensional value")
                dimensionalRecognition = modelDimensional.classify(face)
                # if len(arousalLeft) > 50:
                #     arousalLeft[currentFrame] = dimensionalRecognition[0]
                #     valenceRight[currentFrame] = dimensionalRecognition[0]
                #     currentFrame = currentFrame+1
                #     if currentFrame > 50:
                #         currentFrame = 0
                #
                # arousalRight.append(dimensionalRecognition[0])
                # valenceRight.append(dimensionalRecognition[1])

                createPlot(dimensionalRecognition[0], dimensionalRecognition[1], False)


            plotImage = cv2.imread(
                "plotRight.png")
            # print ("Plot shape:", plotImage.shape)
            # input()
            image[0:480, 894:-1] = plotImage
            img = image
            # print("Plot image:", plotImage.shape)
            # input()

            cv2.imwrite(saveInRight + "/" + str(numberImg)+".png", img)
            numberImg = numberImg+1