# import os
# import pandas as pd
# import cv2
# from PIL import Image
# import pytesseract
# # from langdetect import detect
# import shutil
# from wand.image import Image as wi   
# from pdf2image import convert_from_path
# import io  

# # all the files imported


# nlp = spacy.load("/home/sunil/Desktop/np/model-best")  # load the spacy model

# def process_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#     return pytesseract.image_to_string(thresh, lang='eng')

# def process_file(file_path):
#     text = ""
#     if file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
#         im = cv2.imread(file_path)
#         text = process_image(im)
#     elif file_path.endswith(".pdf"):
#         images = convert_from_path(file_path)
#         for i, image in enumerate(images):
#             image.save(f'special/page_{i+1}.jpg', 'JPEG')
#             text += process_image(image)
#     else:
#         print("Input the correct file")
#     return text

# def process_directory(input_dir, output_dir):
#     rows = []
#     for root, dirs, filenames in os.walk(input_dir):
#         for filename in filenames:
#             print('#######' + filename + '#######')
#             input_path = os.path.join(input_dir, filename)
#             text = process_file(input_path)
#             print("Processed text:")
# #             print(text)
#             doc = nlp(text)
#             mylist = []
#             for ent in doc.ents:
#                 print(ent.text, ent.label_)
#                 mylist.append([ent.text,ent.label_])
#             type_bill = ','.join(i[0] for i in mylist if i[1] == 'TYPE_OF_BILL')
#             name = ','.join(i[0] for i in mylist if i[1] == 'NAME')
#             invoice = ','.join(i[0] for i in mylist if i[1] == 'INVOICE_NO./BILL_NO.')
#             email = ','.join(i[0] for i in mylist if i[1] == 'EMAIL')
#             date = ','.join(i[0] for i in mylist if i[1] == 'ORDER_DATE')
#             description = ','.join(i[0] for i in mylist if i[1] == 'DESCRIPTION')
#             amount = ','.join(i[0] for i in mylist if i[1] == 'TOTAL_AMOUNT')
#             tax = ','.join(i[0] for i in mylist if i[1] == 'TAX_RATE')
#             quantity = ','.join(i[0] for i in mylist if i[1] == 'QUANTITY')
#             mobile = ','.join(i[0] for i in mylist if i[1] == 'MOBILE_No.')
#             df = pd.DataFrame(columns=['TYPE_OF_BILL', 'NAME', 'INVOICE_NO./BILL_NO.', 'EMAIL', 'ORDER_DATE', 'DESCRIPTION', 'TOTAL_AMOUNT', 'TAX_RATE', 'QUANTITY', 'MOBILE_NO.'])
#             df = df.append({'TYPE_OF_BILL':type_bill,'NAME':name,'INVOICE_NO./BILL_NO.':invoice,'EMAIL':email,'ORDER_DATE':date,'DESCRIPTION':description,'TOTAL_AMOUNT':amount,'TAX_RATE':tax,'QUANTITY':quantity,'MOBILE_NO.':mobile}, ignore_index=True)
#             print(df)
#             output_path = "output.html"
            
#             result = df.to_html()
#             print(result)
#             html = df.to_html()
#             text_file = open("output.html", "w")
#             text_file.write(html)
#             text_file.close()
#             text_file = open("output.html", "w")
# #             text_file.write(html)
# #             text_file.close()
#             shutil.move(input_path, output_path)
#             print(f"Moved file to {output_path}")
            
            
# process_directory(r"/home/sunil/Desktop/np/uploads/", r"/home/sunil/Desktop/np/special/")