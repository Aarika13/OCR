import keras_ocr
import cv2
import pytesseract
import os
from PIL import Image
# path for the folder
indir = r'/home/sunil/Desktop/np/uploads/'

for root, dirs, filenames in os.walk(indir):
    for filename in filenames:
        print('#####################################' + filename + '#####################################')
        im = Image.open(indir + filename)
        text = pytesseract.image_to_string(im, lang='eng')
        print(text)


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

