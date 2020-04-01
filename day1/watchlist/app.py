from flask import Flask
app = Flask(__name__)

@app.route('/')
# @app.route('/index')
# @app.route('/home')

def index():
    return "<h1>hello,Flask,00</h1>"

# 动态url
@app.route('/index/<name>')
def home(name):
    return "<h1>hello,Flask,%s</h1>" %name
