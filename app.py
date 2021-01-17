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

@app.route('/cat-meow', methods = ['GET'])
def meow():
     path_to_file = "/meow.m4a"

     return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=True, 
         attachment_filename="meow.m4a")


@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):
    if event.message.text == '喵喵歌':
        pass
    elif event.message.text == '喵喵叫':
        pass
    elif event.message.text == '喵喵圖':
        image_url = find_cat_image()
        return_message = ImageSendMessage(original_content_url = image_url, preview_image_url = image_url)
        line_bot_api.reply_message(
            event.reply_token,
            return_message
        )
    else:
        return_message = TextSendMessage(text = translate(event.message.text))
        line_bot_api.reply_message(
            event.reply_token,
            return_message
        )

@handler.add(MessageEvent, message = StickerMessage)
def handle_sticker_message(event):
    return_message = TextSendMessage(text = 'Meow!')
    line_bot_api.reply_message(
        event.reply_token,
        return_message
    )

@handler.add(MessageEvent, message = FileMessage)
def handle_file_message(event):
    if event.message.file_name.endswith('.txt'):
        content = line_bot_api.get_message_content(event.message.id)
        content_message = ''
        for chunk in content.iter_content():
            content_message += translate(chunk.decode('UTF-8'))
        
        return_message = TextSendMessage(text = content_message)
    else:
        return_message = [TextSendMessage(text = '這是什麼呀?能吃喵?'), ImageSendMessage(original_content_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png', preview_image_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png')]

    line_bot_api.reply_message(
        event.reply_token,
        return_message
    )

@handler.add(MessageEvent, message = StickerMessage)
def handle_sticker_message(event):
    package_id, sticker_id = gen_sticker()
    return_message = StickerSendMessage(package_id = package_id, sticker_id = sticker_id)
    line_bot_api.reply_message(
        event.reply_token,
        return_message
    )

@handler.add(MessageEvent, message = VideoMessage)
def handle_video_message(event):
    return_message = [TextSendMessage(text = '這是什麼呀?能吃喵?'), ImageSendMessage(original_content_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png', preview_image_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png')]
    line_bot_api.reply_message(
        event.reply_token,
        return_message
    )

@handler.add(MessageEvent, message = ImageMessage)
def handle_image_message(event):
    return_message = [TextSendMessage(text = '這是什麼呀?能吃喵?'), ImageSendMessage(original_content_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png', preview_image_url = 'https://maoup.com.tw/wp-content/uploads/2015/07/114.png')]
    line_bot_api.reply_message(
        event.reply_token,
        return_message
    )




if __name__ == "__main__":
    app.run()