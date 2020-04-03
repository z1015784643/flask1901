import os 
import sys

import click
from flask import Flask
from flask import render_template,flash,redirect,request,url_for

from flask_sqlalchemy import SQLAlchemy  #导入扩展类

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlie:////'

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   #关闭对模型修改的监控
app.config['SECRET_KEY'] = 'watchlist_dev'
db = SQLAlchemy(app)  #初始化扩展，传入程序实例app

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))

class Movies(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

# 模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user = user)

# view视图
@app.route('/',methods=['GET','POST'])
# @app.route('/')
# @app.route('/index')
# @app.route('/home')
def index():
    # user = User.query.first()
    # requesr在请求出发才会包含数据
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year)>4 or len(title)>60:
            flash('不能为空或超出最大长度')
            return redirect(url_for('index'))
        # 保存表单的数据
        movie = Movies(title = title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('index'))

    movies = Movies.query.all()
    return render_template('index.html',movies=movies)

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year)>4 or len(title)>10:
            flash('不能为空或超出长度')
            return redirect(url_for('index'))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("更新完成")
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)

# 删除
@app.route('/movie/delete/<int:movie_id>',methods=['GET','POST'])
def delete(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除完成")
    return redirect(url_for('index'))

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


# 错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    # 返回模板和状态码
    return render_template('404.html'),404




