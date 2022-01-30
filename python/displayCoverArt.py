import time
import sys
import logging
from logging.handlers import RotatingFileHandler
from getSongInfo import getSongInfo
import requests
from io import BytesIO
from PIL import Image
import sys,os
import configparser
from sense_hat import SenseHat

if len(sys.argv) > 2:
    username = sys.argv[1]
    token_path = sys.argv[2]

    # Configuration file    
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../config/rgb_options.ini')

    # Configures logger for storing song data    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='spotipy.log',level=logging.INFO)
    logger = logging.getLogger('spotipy_logger')

    # automatically deletes logs more than 2000 bytes
    handler = RotatingFileHandler('spotipy.log', maxBytes=2000,  backupCount=3)
    logger.addHandler(handler)

     # Configuration for the matrix
    config = configparser.ConfigParser()
    config.read(filename)
    default_image = os.path.join(dir, config['DEFAULT']['default_image'])
    print(default_image)
    
    try:
      while True:
        try:
          imageURL = getSongInfo(username, token_path)[1]
          response = requests.get(imageURL)
          img = Image.open(BytesIO(response.content))
          img.thumbnail([8, 8], Image.ANTIALIAS)

          # Generate rgb values for image pixels
          rgb_img = img.convert('RGB')
          image_pixels = list(rgb_img.getdata())

          # Get the 64 pixels you need
          pixel_width = 1
          image_width = pixel_width*8
          sense_pixels = []
          start_pixel = 0
          while start_pixel < (image_width*8):
              sense_pixels.extend(image_pixels[start_pixel:(
          start_pixel+image_width):pixel_width])
              start_pixel += (image_width*pixel_width)

          # Display the image
          sense = SenseHat()
          sense.set_rotation(r=180)
          sense.set_pixels(sense_pixels)
          time.sleep (1)

        except:
          img = Image.open(default_image)
          img.thumbnail([8, 8], Image.ANTIALIAS)

          # Generate rgb values for image pixels
          rgb_img = img.convert('RGB')
          image_pixels = list(rgb_img.getdata())

          # Get the 64 pixels you need
          pixel_width = 1
          image_width = pixel_width*8
          sense_pixels = []
          start_pixel = 0
          while start_pixel < (image_width*8):
              sense_pixels.extend(image_pixels[start_pixel:(
          start_pixel+image_width):pixel_width])
              start_pixel += (image_width*pixel_width)

          # Display the image
          sense = SenseHat()
          sense.set_rotation(r=180)
          sense.set_pixels(sense_pixels)
          time.sleep (1)
    except KeyboardInterrupt:
      sys.exit(0)

else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()