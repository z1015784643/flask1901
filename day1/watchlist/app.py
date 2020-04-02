import os 
import sys

import click
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy  #导入扩展类

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlie:////'

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    #关闭对模型修改的监控
db = SQLAlchemy(app)  #初始化扩展，传入程序实例app

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))

class Movies(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

@app.route('/')
# @app.route('/index')
# @app.route('/home')

def index():
    user = User.query.first()
    movies = Movies.query.all()
    return render_template('index.html',name=user.name,movies=movies)

# # 动态url
# @app.route('/index/<name>')
# def home(name):
#     return "<h1>hello,Flask,%s</h1>" %name


# 自定义命令
# 新建data,db 的数据库初始化命令
@app.cli.command()   #这个装饰器可以注册命令
@click.option('--drop',is_flag = True,help = '删除后再创建')
def initdb(drop):
    if drop:
        db.drop_all()

    db.create_all()
    click.echo('初始化数据库完成')

# 向data.db中写入数据的命令

@app.cli.command()
def forge():
    name = "中国"
    movies = [
        { "title" : "大赢家" , "year" : "2020" },
        { "title" : "叶问四" , "year" : "2020" },
        { "title" : "唐人街探案" , "year" : "2020" },
        { "title" : "囧妈" , "year" : "2020" },
    ]

    user = User(name = name)
    db.session.add(user)
    for m in movies:
        movie = Movies(title = m['title'],year = m['year'])
        db.session.add(movie)
    db.session.commit()




