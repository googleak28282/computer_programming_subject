import weather_api
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from google_func import search_area
import random
import threading

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('emyMxwWz62PJu576SNhqXSNMjs4hWxr5evy4bBO6YYYjjCRcMonFEf6vBFCoJbg0Qy+POZ7VwIax7yC7Ra6kelQ7dEqE89X78h9WgfwDcM5LYaGe4VUjOccegOFxV7Z1IhFPhD5UofJkI1X/msL3/wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3010a3e5da9e71f34759591665e6d789')
#功能編寫
def request_choose(locate, day):
    request = [day for i in range(5)]
    result = weather_api.get_data(locate, request)
    weather_now = result[0]['parameter']['parameterName']
    raining_rate = result[1]['parameter']['parameterName']
    lowest_temp = result[2]['parameter']['parameterName']
    feeling = result[3]['parameter']['parameterName']
    highest_temp = result[4]['parameter']['parameterName']
    return (locate+"的天氣爲"+weather_now+"\n降雨機率: "+raining_rate +
            "%\n最低溫度: "+lowest_temp+"C 最高溫度: "+highest_temp+"C \n舒適度爲"+feeling)
def get_request(locate, update):
    request = [1, 1, 1, 1, 1]
    result = weather_api.get_data(locate, request)
    weather_now = result[0]['parameter']['parameterName']
    raining_rate = result[1]['parameter']['parameterName']
    lowest_temp = result[2]['parameter']['parameterName']
    feeling = result[3]['parameter']['parameterName']
    highest_temp = result[4]['parameter']['parameterName']
    update.message.reply_text(locate+"的天氣爲"+weather_now+"\n降雨機率: "+raining_rate +"%\n最低溫度: "+lowest_temp+"C 最高溫度: "+highest_temp+"C \n舒適度爲"+feeling, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(time, callback_data='{}-{}'.format(index, locate)) for index, time in [(2, '12小時後'), (3, '24小時後')]]]))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
