# Telebot

#GET STARTED 

This API is tested with Python 3.6-3.10 and Pypy 3. There are two ways to install the library:

Installation using pip (a Python package manager):
$ pip install pyTelegramBotAPI

While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling.

pip install pytelegrambotapi --upgrade

#SOME OF THE BASIC CODE SNNAPITS

import telebot

TOKEN = '<token_string>'
tb = telebot.TeleBot(TOKEN)	#create a new Telegram Bot object

- Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
- interval: int (default 0) - The interval between polling requests
- timeout: integer (default 20) - Timeout in seconds for long polling.
- allowed_updates: List of Strings (default None) - List of update types to request 
tb.infinity_polling(interval=0, timeout=20)

# getMe
user = tb.get_me()

# setWebhook
tb.set_webhook(url="http://example.com", certificate=open('mycert.pem'))
# unset webhook
tb.remove_webhook()

# getUpdates
updates = tb.get_updates()
# or
updates = tb.get_updates(1234,100,20) #get_Updates(offset, limit, timeout):

# sendMessage
tb.send_message(chat_id, text)

# editMessageText
tb.edit_message_text(new_text, chat_id, message_id)

# forwardMessage
tb.forward_message(to_chat_id, from_chat_id, message_id)

# sendPhoto
photo = open('/tmp/photo.png', 'rb')
tb.send_photo(chat_id, photo)
tb.send_photo(chat_id, "FILEID")

# sendAudio
audio = open('/tmp/audio.mp3', 'rb')
tb.send_audio(chat_id, audio)
tb.send_audio(chat_id, "FILEID")

## sendAudio with duration, performer and title.
tb.send_audio(CHAT_ID, file_data, 1, 'eternnoir', 'pyTelegram')

# sendVoice
voice = open('/tmp/voice.ogg', 'rb')
tb.send_voice(chat_id, voice)
tb.send_voice(chat_id, "FILEID")

# sendDocument
doc = open('/tmp/file.txt', 'rb')
tb.send_document(chat_id, doc)
tb.send_document(chat_id, "FILEID")

# sendSticker
sti = open('/tmp/sti.webp', 'rb')
tb.send_sticker(chat_id, sti)
tb.send_sticker(chat_id, "FILEID")

# sendVideo
video = open('/tmp/video.mp4', 'rb')
tb.send_video(chat_id, video)
tb.send_video(chat_id, "FILEID")

# sendVideoNote
videonote = open('/tmp/videonote.mp4', 'rb')
tb.send_video_note(chat_id, videonote)
tb.send_video_note(chat_id, "FILEID")

# sendLocation
tb.send_location(chat_id, lat, lon)

# sendChatAction
- action_string can be one of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
- 'record_audio', 'upload_audio', 'upload_document' or 'find_location'.
tb.send_chat_action(chat_id, action_string)

# getFile
# Downloading a file is straightforward
# Returns a File object
import requests
file_info = tb.get_file(file_id)

file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))

