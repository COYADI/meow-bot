from googletrans import Translator

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
