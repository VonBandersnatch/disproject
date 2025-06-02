from flask import Flask
from database import init_db
from controllers import todo, category, bills, ft
import psycopg2
import os
import pandas as pd


init_db()

app = Flask(__name__)

#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"



#app.register_blueprint(todo.bp)
#app.register_blueprint(category.bp)
app.register_blueprint(bills.bp)
#app.register_blueprint(ft.bp)
