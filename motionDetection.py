import datetime
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import numpy as np # Import NumPy library
import os
import schedule
from subprocess import call 
import telepot
from telepot.loop import MessageLoop # Library function to communicate with telegram bot
from threading import Thread
from time import sleep  # Importing the time library to provide the delays in progra

bot = telepot.Bot('your_bot_id')
globalChatId = your_chat_id
 
# Initialize the camera
camera = PiCamera()

camera.vflip = True
 
# Set the camera resolution
camera.resolution = (640, 480)
 
# Set the number of frames per second
camera.framerate = 4
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(640, 480))
 
# Create the background subtractor object
# Feel free to modify the history as you see fit.
back_sub = cv2.createBackgroundSubtractorMOG2(history=150,
  varThreshold=25, detectShadows=False)
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.25)

now = datetime.datetime.now()

photoQueue = []
messageQueue = []

retyring = 72000
retyringAfter = 2

commandList = '/hi /time /date /photoList /deletePhotos /commands' 
 
# Create kernel for morphological operation. You can tweak
# the dimensions of the kernel.
# e.g. instead of 20, 20, you can try 30, 30
kernel = np.ones((20,20),np.uint8)


def getPhotoDirectory():
    directory = '/home/pi/Documents/mypi/homeSurveillanceUsingOpenCvAndTelegram/photos/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def getFileName():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.%f")

def connectToBoot():
    print('Connecting to bot...')
    try:
        print(bot.getMe())
        print('connected to bot')
    except:
        print('Could not connect to boot')
def sendTheTextMessage(bot, chat_id):
    while len(messageQueue):
        message = messageQueue.pop(0)
        for tryCount in range(0, retyring):
            try:
                bot.sendMessage(chat_id, message)
            except:
                print('could not send the text message')
                sleep(retyringAfter)
                continue
            break

        
def sendMessage(bot, chat_id, msg):
    messageQueue.append(str(msg))
    textThred = Thread(target = sendTheTextMessage, args = (bot, chat_id))
    textThred.start()

# Delete all the files. But not delete the last `notDeletedFileCount` files
def deleteImages(bot, chat_id, directory, notDeletedFileCount):
    files = os.listdir(directory)
    totalFiles = len(files)
    files.sort()
    
    for fileIndex in range(0, totalFiles - notDeletedFileCount):
        try:
            os.remove(os.path.join(directory, files[fileIndex]))
        except:
            print('Could not delete the video' + files[fileIndex])
        
    print('Total deleted videos: '+ str(totalFiles - notDeletedFileCount))
    sendMessage(bot, chat_id, str(totalFiles - notDeletedFileCount) + str(' files has been deleted.'))

def sendThePhoto(bot, chat_id):
    while len(photoQueue):
        photo = photoQueue.pop(0)
        print(photo)
        for tryCount in range(0, retyring):
            try:
                bot.sendPhoto(chat_id, photo=open(photo, 'rb'))
                try:
                    #deleteImages(bot, chat_id, getPhotoDirectory(), 5)
                    os.remove(photo)
                except:
                    print('Could not delete the photo')
            except:
                print('could not send the photo')
                sleep(retyringAfter)
                continue
            break
        
def sendPhoto(bot, chat_id, photo):
    photoQueue.append(photo)
    textThred = Thread(target = sendThePhoto, args = (bot, chat_id))
    textThred.start()
    
connectToBoot()

def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message
    
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        sendMessage(bot, chat_id, str("Hi! Pioneer"))
    elif command == '/time':
        sendMessage(bot, chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        sendMessage(bot, chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/photoList':
        directory = getPhotoDirectory()
        sendMessage(bot, chat_id, str(os.listdir(directory)))
    elif command == '/deletePhotos':
        deleteAllPhotos(bot, chat_id)
    elif command == '/commands':
        sendMessage(bot, chat_id, commandList)
    else:
        sendMessage(bot, chat_id, str("Please write a right command. Please send the write commands from the list") + commandList)

def startLiseningMessages():
    try:
        MessageLoop(bot, handle).run_as_thread()
        print ('Listening....')
    except:
        print('MessageLoop error')

def detectMotionUsingOpenCv():
    # Capture frames continuously from the camera
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
     
        # Grab the raw NumPy array representing the image
        image = frame.array
 
        # Convert to foreground mask
        fg_mask = back_sub.apply(image)
     
        # Close gaps using closing
        fg_mask = cv2.morphologyEx(fg_mask,cv2.MORPH_CLOSE,kernel)
       
        # Remove salt and pepper noise with a median filter
        fg_mask = cv2.medianBlur(fg_mask,5)
       
        # If a pixel is less than ##, it is considered black (background). 
        # Otherwise, it is white (foreground). 255 is upper limit.
        # Modify the number after fg_mask as you see fit.
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)
 
        # Find the contours of the object inside the binary image
        contours, hierarchy = cv2.findContours(fg_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
        areas = [cv2.contourArea(c) for c in contours]
  
        # If there are no countours
        if len(areas) < 1:
  
          # Display the resulting frame
          cv2.imshow('Frame',image)
  
          # Wait for keyPress for 1 millisecond
          key = cv2.waitKey(1) & 0xFF
  
          # Clear the stream in preparation for the next frame
          raw_capture.truncate(0)
     
          # If "q" is pressed on the keyboard, 
          # exit this loop
          if key == ord("q"):
            break
     
          # Go to the top of the for loop
          continue
  
        else:
         
          # Find the largest moving object in the image
          max_index = np.argmax(areas)
      
      
        # Draw the bounding box
        cnt = contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
  
        # Draw circle in the center of the bounding box
        x2 = x + int(w/2)
        y2 = y + int(h/2)
        cv2.circle(image,(x2,y2),4,(0,255,0),-1)
  
        # Print the centroid coordinates (we'll use the center of the
        # bounding box) on the image
        text = "x: " + str(x2) + ", y: " + str(y2)
        cv2.putText(image, text, (x2 - 10, y2 - 10),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
        #save the image
        photo = getPhotoDirectory() + getFileName() + '.jpg'
        try:
            cv2.imwrite(photo, image)
            try:
                sendPhoto(bot, globalChatId, photo)
            except:
                print('Could not send the photo')
        except:
            print('Could not save the file')
          
        # Display the resulting frame
        cv2.imshow("Frame",image)
     
        # Wait for keyPress for 1 millisecond
        key = cv2.waitKey(1) & 0xFF
  
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)
     
        # If "q" is pressed on the keyboard, 
        # exit this loop
        if key == ord("q"):
          break
 
    # Close down windows
    cv2.destroyAllWindows()


def main():
    connectToBoot()
    # Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
    try:
        startLiseningMessages()
    except:
        print('startLiseningMessages')
    try:
        detectMotionUsingOpenCv()
    except:
        print("Error from detectMotionUsingOpenCv")

if __name__ == "__main__":
    main()