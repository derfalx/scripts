import logging
logging.basicConfig(level=logging.DEBUG)
import os
from waveshare_epd import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont
import requests

# additionally requires:
# https://github.com/waveshare/e-Paper

try:
    logging.info("== weatherpaper ==")
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    #font = ImageFont.load_default()
    fontpath = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    font = ImageFont.truetype(os.path.join(fontpath, 'ttf/FiraCode-Regular.ttf'), 13)
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    epd.init(epd.FULL_UPDATE)

    update_count = 0
    while(True):
        r = requests.get('https://wttr.in/Halle(Saale)?0T&lang=de')
        r.encoding = 'utf-8'
        logging.info(r.text)
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        draw.text((0,0), r.text, font=font, fill=0)
        image = image.rotate(180)
        epd.display(epd.getbuffer(image))
        time.sleep(60*15)
except KeyboardInterrupt:
    epd2in13_V2.epdconfig.module_exit()
    exit()
