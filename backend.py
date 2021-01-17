from googletrans import Translator
import random

translator = Translator()
def translate(sentence):
    detected_lang = translator.detect(sentence).lang
    print(detected_lang)
    if detected_lang == 'ja':
        return translator.translate(sentence, dest = 'zh-tw').text
    elif detected_lang == 'zh-TW' or detected_lang == 'zh-CN':
        return translator.translate(sentence, dest = 'ja').text
    else:
        return '我聽不懂耶喵講中文或日文好嗎 :(\n中国語または日本語を話してくださニャー :('

def gen_sticker():
    package_id = random.randint(11537, 11539)
    if package_id == 11537:
        sticker_id = random.randint(52002734, 52002773)
    elif package_id == 11538:
        sticker_id = random.randint(51626494, 51626533)
    else:
        sticker_id = random.randint(52114110, 52114149)
    return package_id, sticker_id