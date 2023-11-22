import logging
logging.basicConfig(level=logging.DEBUG)
import os
from waveshare_epd import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont
import requests
import sys


def weatherpaper(location, language, minutes):
    # Main try-except is used to intercept keyboardinterrupts to properly
    # shut down the script.
    try:
        logging.info("== weatherpaper ==")
        # Preparing and cleaning the Display
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        # Loading the font and creating an initial, empty screen.
        fontpath = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        font = ImageFont.truetype(os.path.join(fontpath, 'ttf/FiraCode-Regular.ttf'), 13)
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        # Everytime an update is done, it will be a full (instead of a partial) update.
        epd.init(epd.FULL_UPDATE)

        while(True):
            try:
                r = requests.get(f'https://wttr.in/{location}?0T&lang={language}')
                # In case r.status_code is not a successful status, raise an exception
                r.raise_for_status()
                # Setting proper encoding, so the text can be display correct
                r.encoding = 'utf-8'
                logging.info(r.text)
                image = Image.new('1', (epd.height, epd.width), 255)
                draw = ImageDraw.Draw(image)
                draw.text((0,0), r.text, font=font, fill=0)
                # Rotating the image is needed in my case, since I use the display bottom up.
                # In case you use it the other way round, remove this line.
                image = image.rotate(180)
                epd.display(epd.getbuffer(image))
            except requests.exceptions.RequestException as e:
                logging.warn(f'An exception occurred while requesting wttr.in. Maybe it returned != 200. Skipping update.')

            time.sleep(60 * minutes)
    except KeyboardInterrupt:
        epd2in13_V2.epdconfig.module_exit()
        exit()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage: python weatherpaper.py <location> <language> <minutes>")
        exit()

    weatherpaper(sys.argv[1], sys.argv[2], int(sys.argv[3]))
