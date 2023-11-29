from PIL import Image
from random import choice

with Image.open("frame.jpg") as im:
    im.rotate(choice([0,180])).show()
