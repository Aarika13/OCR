import shutil
import os
from flask import render_template
from flask import send_from_directory
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import Flask, jsonify
# import json
from pdfreader import PDFDocument, SimplePDFViewer
# import pymongo
from pymongo import MongoClient
# for 500 internal error
from logging import FileHandler, WARNING
# importing file for data extraction
from PyPDF2 import PdfReader
# import PyPDF2
from pdf2image import convert_from_path
import cv2
import pytesseract
import spacy
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
        with open(file_path,'rb') as f:
            viewer = SimplePDFViewer(f)
            viewer.render()
            text = "".join(viewer.canvas.strings)
    else:
        print("Input the correct file")
    return text


def process_directory(input_dir, output_dir):
    # user = request.form.get('comp_select')
    # user = upload_file()
    # user = request.args.get("user")
    print(user)
    data = []
    df = pd.DataFrame(columns=["TYPE_OF_BILL", "DATE", "MOBILE_NO", "ADDRESS", "DESCRIPTION", "STATE", "INVOICE/BILL_NO", "EMAIL", "TIME", "AMOUNT", "RATE", "QUANTITY", "NAME", "COUNTRY"])
    print(type(df))
    for root, dirs, filenames in os.walk(input_dir):
        for filename in filenames:
            input_path = os.path.join(input_dir, filename)
            text = process_file(input_path)
            print("Processed text:")
            doc = nlp(text)
            mylist = []
            for ent in doc.ents:
                print(ent.text, ent.label_)
                mylist.append([ent.text, ent.label_])
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
            # df = df.append({'TYPE_OF_BILL': type_bill, 'NAME': name, 'INVOICE/BILL_NO': invoice, 'EMAIL': email, 'DATE':date, 'DESCRIPTION': description, 'AMOUNT': amount, 'RATE': tax, 'QUANTITY': quantity, 'MOBILE_NO': mobile,'STATE': state, 'ADDRESS': address, 'TIME': time, 'COUNTRY': country}, ignore_index=True)
            # data.append({'TYPE_OF_BILL':type_bill,'NAME':name,'INVOICE/BILL_NO':invoice,'EMAIL':email,'DATE':date,'DESCRIPTION':description,'AMOUNT':amount,'RATE':tax,'QUANTITY':quantity,'MOBILE_NO':mobile,'STATE': state,'ADDRESS':address,'TIME': time,'COUNTRY':country}, ignore_index=True)
            if user == 'zoho':
                # execute some code
                # app.logger.debug(user)
                print("ZOHO")
                df = pd.DataFrame(
                    columns=['NAME', 'INVOICE/BILL_NO', 'EMAIL', 'DATE', 'DESCRIPTION','AMOUNT', 'RATE', 'QUANTITY', 'MOBILE_NO'])
                df = df.append({'NAME': name, 'INVOICE/BILL_NO': invoice, 'EMAIL': email, 'DATE': date, 'DESCRIPTION': description,
                     'AMOUNT': amount, 'RATE': tax, 'QUANTITY': quantity, 'MOBILE_NO': mobile}, ignore_index=True)
                print(df)
                # based onabove is class
            elif user == 'tally':
                # execute some other code
                df = pd.DataFrame(
                    columns=['NAME', 'INVOICE/BILL_NO', 'EMAIL', 'DATE', 'DESCRIPTION', 'AMOUNT', 'RATE', 'QUANTITY',
                             'MOBILE_NO','STATE','ADDRESS'])
                df = df.append(
                    {'NAME': name, 'INVOICE/BILL_NO': invoice, 'EMAIL': email, 'DATE': date, 'DESCRIPTION': description,
                     'AMOUNT': amount, 'RATE': tax, 'QUANTITY': quantity, 'MOBILE_NO': mobile, 'STATE': state,
                     'ADDRESS': address, 'TIME': time, 'COUNTRY': country}, ignore_index=True)
                print(df)
                print("TALLY")
            elif user == 'q-book':
                df = pd.DataFrame(
                    columns=['TYPE_OF_BILL','NAME', 'INVOICE/BILL_NO', 'EMAIL', 'DATE', 'DESCRIPTION', 'AMOUNT', 'RATE', 'QUANTITY',
                             'MOBILE_NO'])
                df = df.append(
                    {'TYPE_OF_BILL': type_bill, 'NAME': name, 'INVOICE/BILL_NO': invoice, 'EMAIL': email, 'DATE': date,
                     'DESCRIPTION': description, 'AMOUNT': amount, 'RATE': tax, 'QUANTITY': quantity,
                     'MOBILE_NO': mobile}, ignore_index=True)
                print(df)
                print("QUICK-BOOK")
            else:
                df = df.append(
                    {'TYPE_OF_BILL': type_bill, 'NAME': name, 'INVOICE/BILL_NO': invoice, 'EMAIL': email, 'DATE': date,
                     'DESCRIPTION': description, 'AMOUNT': amount, 'RATE': tax, 'QUANTITY': quantity,
                     'MOBILE_NO': mobile, 'STATE': state, 'ADDRESS': address, 'TIME': time, 'COUNTRY': country},
                    ignore_index=True)
                print(df)
                print("All options")
            output_path = "output.html"
            with open(output_path, 'w') as f:
                f.write(f'<html><body><img src="{filename}"><br><pre>{text}</pre></body></html>')
            shutil.move(input_path, output_path)
            print(f"Moved file to {output_path}")
    return df

# ######here, it finshes
def insert_data_mongo(data):
    client = MongoClient("mongodb+srv://aarika:ajain%40012023@cluster0.y932s1f.mongodb.net/OCR")  # connect to MongoDB
    db = client["OCR"]  # get the database
    collection = db["my_collection"]  # get the collection
    data = data.to_dict(orient="records")
    if data:
        result = collection.insert_many(data)
        print(result.inserted_ids)
    else:
        print("The list of documents is empty.")
        # print(TypeError)
    # result = collection.insert_many(data)  # insert the data
    # print(f"{len(result.inserted_ids)} documents inserted.")
    # return result
    # return f"{len(result.inserted_ids)} documents inserted"


def test_train():
    pass


UPLOAD_FOLDER = '/home/sunil/Desktop/np/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app = Flask(__name__, template_folder="templates")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global user
    user = request.form.get('comp_select')
    print(user)
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
            return redirect(url_for('process_data_route', name=filename))
            # output_data = "/home/sunil/Desktop/np/templates/output.html"
            # return redirect(url_for(output_data,name=filename))
    return render_template("success.html")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/process_data", methods=['GET', 'POST'])
def process_data_route():
    # print(df)
    input_dir = r"/home/sunil/Desktop/np/uploads/"
    output_dir = r"/home/sunil/Desktop/np/special/"
    df = process_directory(input_dir, output_dir)
    insert_data_mongo(df)
    # return "Data processed and stored in MongoDB!"
    my_data = df.to_html('/home/sunil/Desktop/np/templates/output.html')
    return render_template('output.html', table=my_data)


app.add_url_rule(
    "/<name>/output", endpoint="output.html", build_only=True
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)