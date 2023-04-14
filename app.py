from flask import render_template
from flask import send_from_directory
from flask import request, redirect, url_for,flash
from werkzeug.utils import secure_filename
from flask import Flask ,jsonify
import json
import os

from pymongo import MongoClient
# for 500 internal error
from logging import FileHandler,WARNING
# importing file for data extraction
from PyPDF2 import PdfReader 
from pdf2image import convert_from_path
import os
import cv2
import pytesseract
import spacy
import shutil
import pandas as pd

# # #######################here,the text classification is to be done
nlp = spacy.load("/home/sunil/Desktop/np/model-best")  # load the spacy model

def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return pytesseract.image_to_string(thresh, lang='eng')

def process_file(file_path):
    text = ""
    if file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        im = cv2.imread(file_path)
        text = process_image(im)
    elif file_path.endswith(".pdf"):
        images = convert_from_path(file_path)
        for i, image in enumerate(images):
            image.save(f'special/page_{i+1}.jpg', 'JPEG')
            text += process_image(image)
        # with open(file_path, 'rb') as f:
        #     pdf_reader = PyPDF2.PdfReader(f)
        #     for page_num in range(pdf_reader.numPages):
        #         page = pdf_reader.getPage(page_num)
        #         text += page.extractText()
    else:
        print("Input the correct file")
    return text

def process_directory(input_dir, output_dir):
    rows = []
    df = pd.DataFrame(columns=["TYPE_OF_BILL","DATE","MOBILE_NO","ADDRESS","DESCRIPTION","STATE","INVOICE/BILL_NO","EMAIL","TIME","AMOUNT","RATE","QUANTITY","NAME","COUNTRY"])
    for root, dirs, filenames in os.walk(input_dir):
        for filename in filenames:
            # print('#######' + filename + '#######')
            input_path = os.path.join(input_dir, filename)
            text = process_file(input_path)
            print("Processed text:")
#             print(text)
            doc = nlp(text)
            mylist = []
            for ent in doc.ents:
                print(ent.text, ent.label_)
                mylist.append([ent.text,ent.label_])
            type_bill = ','.join(i[0] for i in mylist if i[1] == 'TYPE_OF_BILL')
            name = ','.join(i[0] for i in mylist if i[1] == 'NAME')
            invoice = ','.join(i[0] for i in mylist if i[1] == 'INVOICE/BILL_NO')
            email = ','.join(i[0] for i in mylist if i[1] == 'EMAIL')
            date = ','.join(i[0] for i in mylist if i[1] == 'DATE')
            description = ','.join(i[0] for i in mylist if i[1] == 'DESCRIPTION')
            amount = ','.join(i[0] for i in mylist if i[1] == 'AMOUNT')
            tax = ','.join(i[0] for i in mylist if i[1] == 'RATE')
            quantity = ','.join(i[0] for i in mylist if i[1] == 'QUANTITY')
            mobile = ','.join(i[0] for i in mylist if i[1] == 'MOBILE_No')
            state = ','.join(i[0] for i in mylist if i[1] == 'STATE')
            address = ','.join(i[0] for i in mylist if i[1] == 'ADDRESS')
            time = ','.join(i[0] for i in mylist if i[1] == 'TIME')
            country = ','.join(i[0] for i in mylist if i[1] == 'COUNTRY')
            df = df.append({'TYPE_OF_BILL':type_bill,'NAME':name,'INVOICE/BILL_NO':invoice,'EMAIL':email,'DATE':date,'DESCRIPTION':description,'AMOUNT':amount,'RATE':tax,'QUANTITY':quantity,'MOBILE_NO':mobile,'STATE': state,'ADDRESS':address,'Time': time,'COUNTRY':country}, ignore_index=True)
            print(df)
            # df.to_csv('raw_data.csv', index=False)
            
            output_path = "output.html"
            with open(output_path, 'w') as f:
                f.write(f'<html><body><img src="{filename}"><br><pre>{text}</pre></body></html>')
            
            shutil.move(input_path, output_path)
            print(f"Moved file to {output_path}")
    return df
df = process_directory(r"/home/sunil/Desktop/np/uploads/", r"/home/sunil/Desktop/np/special/")
my_data=df.to_html('/home/sunil/Desktop/np/templates/output.html')         
# ######here, it finshes
    

UPLOAD_FOLDER = '/home/sunil/Desktop/np/uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg','.pdf'}

app = Flask(__name__, template_folder="templates")
#  for mongodb
# client = Mongo
# Client('localhost', 27017)

# db = client.flask_db
# todos = db.todos

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
# df = pd.DataFrame()
# df = pd.read_csv('raw_data.csv')
# df.to_csv('raw_data.csv', index=None)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')  
def upload():  
    return render_template("index.html")  
 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            # windows.alert("Input the correct file")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            return redirect(url_for('output_data',name = filename))
            # output_data = "/home/sunil/Desktop/np/templates/output.html"
            # return redirect(url_for(output_data,name=filename))
    return render_template("success.html")





@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413



# @app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# app.add_url_rule(
#     "/uploads/<name>", endpoint="download_file", build_only=True
# )

@app.route('/<name>/output',methods = ["POST","GET"])
def output_data(name):
    # data = process_directory(df)
    # data = pd.read_csv('raw_data.csv')
    # return render_template('output.html',table = my_data, titles=[''])
    return render_template('output.html',result=my_data)
    # return render_template('output.html',table = my_data,column_names=df.columns.values, row_data=list(df.values.tolist()),  titles=[''])
    #     # assume the form data has been submitted and stored in a DataFrame called `df`

    #     # extract the relevant data from the DataFrame and pass it to the output HTML file
    #     data = df.to_dict(orient='records')
    #     return render_template("output.html", data=data)
    # else:
    #     return render_template("index.html")
#, tables=[df_ds.to_html(classes='data', header="true")]     return redirect("output.html")
app.add_url_rule(
    "/<name>/output", endpoint="output.html", build_only=True
)


if __name__ == '__main__':
    # app.run(debug=True)
    
    app.run(host='0.0.0.0' , port=5000,debug = True)