from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from backend import *

import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):
    return_message = translate(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = return_message))

@handler.add(MessageEvent, message = StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = 'Meow!')
    )

@handler.add(MessageEvent, message = FileMessage)
def handle_file_message(event):
    print(event)
    if event.message.fileName.endswith('.txt'):
        content = line_bot_api.get_message_content(event.message.id)
        content_message = ''
        for chunk in content.iter_content():
            content_message += chunk
        
        print(content_message)
        return_message = translate(content_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = return_message)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text = '這是什麼呀?能吃嗎?'), ImageSendMessage(original_content_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png', preview_image_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png')]
        )

if __name__ == "__main__":
    app.run()