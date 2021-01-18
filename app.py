from flask import Flask, request, abort, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from backend import *
# from pydub import AudioSegment
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

# @app.route('/meow.m4a', methods = ['GET'])
# def meow_voice():
#      meow_file = AudioSegment.from_file('./meow.m4a')

#      return send_file(
#          meow_file, 
#          mimetype="audio/x-m4a", 
#          as_attachment=True, 
#          attachment_filename="meow.m4a")

# handle message event
@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):
    if event.message.text == '喵喵歌':
        return_message = TextSendMessage(text = 'https://www.youtube.com/watch?v=ySv4IlpqF0E')
    elif event.message.text == '喵喵叫':
        return_message = [AudioSendMessage(original_content_url = 'https://drive.google.com/uc?export=download&id=19E-yhLuu0wjIstQB1JyZP9mzm1LXfV3Y', duration = 1500), TextSendMessage(text = meow())]
    elif event.message.text == '喵喵圖':
        image_url = find_cat_image()
        return_message = ImageSendMessage(original_content_url = image_url, preview_image_url = image_url)
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

# handle follow event
@handler.add(FollowEvent)
def handle_follow_event(event):
    return_message = TextSendMessage(text = '嗨嗨你好我是喵爸 !\n我可以進行中文以及日文的雙向翻譯喵 !\n也可以試試看下方的選單喵 !')
    line_bot_api.reply_message(
        event.reply_token,
        return_message
    )

# handle join event
@handler.add(JoinEvent)
def handle_join_event(event):
    return_message = TextSendMessage(text = '嗨嗨大家我是喵爸 !\n我會對所有訊息進行中文以及日文的雙向翻譯噢喵 !\n也可以上傳txt檔案給我吃喵 !')
    line_bot_api.reply_message(
        event.reply_token,
        return_message
    )




if __name__ == "__main__":
    app.run()