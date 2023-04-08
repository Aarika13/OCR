import os
from PIL import Image
import pytesseract
from langdetect import detect

from wand.image import Image as wi   
from pdf2image import convert_from_path
import io      
import matplotlib.pyplot as plt

text = "aar"
indir = "/home/sunil/Desktop/np/special/"
for root, dirs, filenames in os.walk(indir):
    for filename in filenames:
        print('#######' + filename + '#######')
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            im = Image.open(os.path.join(indir, filename))
            text = pytesseract.image_to_string(im, lang='eng')
            print(text)
          
        elif filename.endswith(".pdf"):
            pdf_path = os.path.join(indir, filename)
            images = convert_from_path(pdf_path)
            for i, image in enumerate(images):
                image.save(f'special/page_{i+1}.jpg', 'JPEG')
        else:
            print("Input the correct file")
    print(text,"asdf")