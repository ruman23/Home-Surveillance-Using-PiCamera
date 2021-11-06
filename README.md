# Home Surveillance

This project lets the user to capture the image of any object or person after detecting the motion. After detecting the motion it can send the images to users via Telegram Messenger. 

For recording the videos in 24/7 hours and storing them to analyze in future is required huge amount of storage and time. Besides that, in this IoT era, it's mendatory to surveillance remotely. For the aformentioned reasons, it captures the image when it detects the motions and sends them to user via Telegram Messenger. 
For detecting the motion it analyzes the live videos using the OpenCV. Moreover, if the system fails to share the images to Telegram, then it will save them locally. For saving the storage of the Raspberry PI, it will automatically delete the images after sending them to users. 


## Languages and Tools


- OpenCV
- Raspberry PI
- PI Camera
- Telegram
- PIR Motion Sensor
- Python

## Installation
- ### Clone the Repository

For cloning the repository, please paste the following command to your terminal/command line and the press enter. 
```bash
git clone https://github.com/ruman23/Home-Surveillance-Using-PiCamera.git
```
Or you may directly download this project from the following link. After downloading the project please unzip it. 

https://github.com/ruman23/Home-Surveillance-Using-PiCamera/archive/refs/heads/main.zip


After cloning or downloading the project, please go to the project directory folder `Home-Surveillance-Using-PiCamera`.

- ### Connect to Telegram

For connecting to Telegram you need to create `botId`(access token). For crating the `botId`, please follow the following link. 
https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot

You will also need to create `chatId` for connecting to Telegram. To find out the `chatId` of Telegram please check the following link.
https://www.alphr.com/find-chat-id-telegram/

Now, please open the `motionDetection.py` and then replace the `your_bot_id` by  your newly created `botId` and `your_chat_id` by your newly created `chatId`.

```bash
bot = telepot.Bot('your_bot_id')
globalChatId = `your_chat_id`
``` 

- ### Connect to camera

Please physically connect your `PI Camera` to your raspbery PI if you haven't connected it yet. :) 
 
- ### Start Surveillancing
For starting surveillance, just execute the `motionDetection.py` using terminal or from python IDE. 

If you have followed the aforementioned instruction correctly and started to move infront of the camera, then I'm hopping that you have received a notification to your Telegram Messenger with your image. :) 
