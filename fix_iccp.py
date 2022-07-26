import os
from PIL import Image

for file in os.listdir('.'):
    if file.endswith('.png'):
        image = Image.open(file)
        image.save(file, icc_profile=None)
