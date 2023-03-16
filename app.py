from flask import render_template
from flask import send_from_directory
from flask import request, redirect, url_for,flash
from werkzeug.utils import secure_filename
from flask import Flask ,jsonify
import json
import os

UPLOAD_FOLDER = '/home/sunil/Desktop/np/uploads'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Vendor = [
#     {
#         "id ": 1,
#         "bill_no." : 0001
#         "name" : "Minal",
#         "company" : "Aspire",
#         "Mobile Number" : 1234567890,
#         "E-mail" : "aar@gmail.com",
#         "Date" : 12/01/2012,
#         "Type_of_bill" : "",
#         "Quantity" : 1,
#         "Description" : "",
#         "Amount" : 4234567.00

#     }
# ]

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
            return redirect(url_for('download_file', name=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form  method =post enctype=multipart/form-data>  
                <input type=file name=file>  
                <input type =submit value=Upload>  
        </form>'''
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

if __name__ == '__main__':
    app.run(debug=True)