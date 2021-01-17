from googletrans import Translator
from bs4 import BeautifulSoup
import random, requests

translator = Translator()
def translate(sentence):
    detected_lang = translator.detect(sentence).lang

    if detected_lang == 'ja':
        return translator.translate(sentence, dest = 'zh-tw').text + '喵'
    elif detected_lang == 'zh-TW' or detected_lang == 'zh-CN':
        return translator.translate(sentence, dest = 'ja').text + 'ニャー'
    else:
        return '我聽不懂耶喵講中文或日文好喵 :(\n中国語または日本語を話してくださニャー :('

def gen_sticker():
    package_id = random.randint(11537, 11539)
    if package_id == 11537:
        sticker_id = random.randint(52002734, 52002773)
    elif package_id == 11538:
        sticker_id = random.randint(51626494, 51626533)
    else:
        sticker_id = random.randint(52114110, 52114149)
    return package_id, sticker_id

def find_cat_image():
    image_list = []
    image_search_keyword = ['可愛貓咪', '貓咪可愛', 'cute cat', 'cat cute', 'かわいいねこ', 'かわいい猫']
    target_url = f'https://www.google.com/search?q={target_search_keyword[random.randint(0, len(target_search_keyword - 1))]}&tbm=isch'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')
    images = soup.findAll('img', class_ = 't0fcAb')
    for image in images:
        image_list.append(image['src'])
    return image_list[random.randint(0, len(image_list) - 1)]