from flask import Flask


UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set('*.doc','*.png','*.jpeg')

app = Flask(__name__)
app.config.from_object('config')
