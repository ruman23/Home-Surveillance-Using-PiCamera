# Home Surveillance

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
- ### Clone the repository

For cloning the repository, please paste the following text to your terminal/command line and the press enter. 
```bash
git clone https://github.com/ruman23/Home-Surveillance-Using-PiCamera.git
```
Or you may directly download this project from the following link. After downloading the project please upzip it. 

https://github.com/ruman23/Home-Surveillance-Using-PiCamera/archive/refs/heads/main.zip


After cloning or downloading the project, please go to the project `Home-Surveillance-Using-PiCamera` folder

- ### Connect to Telegram

For connecting to Telegram you will needed to create botId (access token). For crating the botId, please follow the following link. 
https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot

You will also be needed the chat id for your. For finding out the chatId of Telegram please check the following link.
https://www.alphr.com/find-chat-id-telegram/

Now, please open the `motionDetection.py` and then replace the  `your_bot_id` by  your newly created `botId` and `your_chat_id` by your newly created `chatId`.

```bash
bot = telepot.Bot('your_bot_id')
globalChatId = your_chat_id
``` 

- ### Connect to camera

Please connect your PI camera to your raspbery PI. :) 
 
- ### Start Surveillancing
For startign to surveillance, just run execute the  `motionDetection.py` using terminal or python IDE. 

If you have followed the aforementioned instruction correctly and started to move infron of the camera, then I'm hopping that your have recevied an Notification to your Telegram Messenger. 
