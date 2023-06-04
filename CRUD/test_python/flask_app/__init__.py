# __init__.py
from flask import Flask
app = Flask(__name__)
app.secret_key = "hello"
DATABASE = "table_of_appointement"