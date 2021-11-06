# Home Surveillance Using Raspberry PI and PI Camera.

This project lets the user to capute the image of any object or person after detecting the motion. After detecting the motinon it can send the images to users via Telegram messenger. 

For recording the videos in 24/7 hours and storing them to analyze in future is required huge amount of storage and time. Besides, that in this IoT era, it's very mendatory to surveilance remotely. For the aformentioned reasons, we have captured the image when we found the motions and send them to user via Telegram Messenger. 
For detecting the motion we analyze the live videos using the OpenCV. Moreover, if the system fails to shared the images to Telegram, then it will save them locally. For saving the storage of the Raspberry PI, system will automatically delete the images which has been send to users.  


## Languages and Tools


- OpenCV
- Raspberry PI
- PI Camera
- Telegram
- PIR Motion Sensor

## Installation

First clone the repo using the terminal. 
```bash
pip install foobar
```
