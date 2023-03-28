import os
from PIL import Image
import pytesseract
from langdetect import detect

from wand.image import Image as wi
from pdf2image import convert_from_path
import io
import matplotlib.pyplot as plt
# import keras_ocr
import re
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# path for the folder
indir = "/home/sunil/Desktop/np/special"

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





















# indir = r'/home/sunil/Desktop/np/uploads/'
#
# for root, dirs, filenames in os.walk(indir):
#     for filename in filenames:
#         print('#####################################' + filename + '#####################################')
#         im = Image.open(indir + filename)
#         text = pytesseract.image_to_string(im, lang='eng')
#         print(text)


# # specify the path to the folder containing the image files
# folder_path = "/home/sunil/Desktop/np/uploads"

# # loop through all the files in the folder
# for filename in os.listdir(folder_path):
#     # check if the file is an image file
#     if filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):
#         # read the image file
#         print(filename)
#         img = cv2.imread(os.path.join(folder_path, filename))

#         # display the image
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         # apply thresholding : used to differentiate the background and foreground
#         thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#         # recognize text with Pytesseract
#         text = pytesseract.image_to_string(thresh)

#         # print the recognized text

# print(text)

# import cv2
# import pytesseract
# import os

# # read the image file
# img = cv2.imread(r'/home/sunil/Desktop/np/uploads/car-service.png')

# # convert the image to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # apply thresholding
# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# # recognize text with Pytesseract
# text = pytesseract.image_to_string(thresh)

# # print the recognized text
# print(text)

