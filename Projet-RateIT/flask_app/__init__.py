from flask import Flask
from datetime import date
app = Flask(__name__)
DATABASE = "rateit_db"
TODAY = date.today()
UPLOAD_FOLDER = '/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key ="ThisIsASecretMat9oulL7ad"