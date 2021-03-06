# import os 
# import sys

# import click
# from flask import Flask
# # from flask import render_template,flash,redirect,request,url_for
# from werkzeug.security import generate_password_hash,check_password_hash

# from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user

# login_manager = LoginManager(app)  #实例化登录扩展类


# # model
# class User(db.Model,UserMixin):
#     id = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(20))
#     username = db.Column(db.String(20))
#     password_hash = db.Column(db.String(128))
#     def set_password(self,password):
#         self.password_hash = generate_password_hash(password)
#     def validate_password(self,password):
#         return check_password_hash(self.password_hash,password)


# class Movies(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     title = db.Column(db.String(20))
#     year = db.Column(db.String(4))

# view视图
# @app.route('/')
# @app.route('/index')
# @app.route('/home')
# @app.route('/',methods=['GET','POST'])
# def index():
#     # user = User.query.first()
#     # requesr在请求出发才会包含数据
#     if request.method == 'POST':
#         # if not current_user.is_authenticated
#         title = request.form.get('title')
#         year = request.form.get('year')
#         if not title or not year or len(year)>4 or len(title)>60:
#             flash('不能为空或超出最大长度')
#             return redirect(url_for('index'))
#         # 保存表单的数据
#         movie = Movies(title = title,year=year)
#         db.session.add(movie)
#         db.session.commit()
#         flash('创建成功')
#         return redirect(url_for('index'))

#     movies = Movies.query.all()
#     return render_template('index.html',movies=movies)

# @app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
# @login_required
# def edit(movie_id):
#     movie = Movies.query.get_or_404(movie_id)
#     if request.method == 'POST':
#         title = request.form['title']
#         year = request.form['year']
#         if not title or not year or len(year)>4 or len(title)>10:
#             flash('不能为空或超出长度')
#             return redirect(url_for('index'))
#         movie.title = title
#         movie.year = year
#         db.session.commit()
#         flash("更新完成")
#         return redirect(url_for('index'))
#     return render_template('edit.html',movie=movie)

# # 删除
# @app.route('/movie/delete/<int:movie_id>',methods=['GET','POST'])
# @login_required
# def delete(movie_id):
#     movie = Movies.query.get_or_404(movie_id)
#     db.session.delete(movie)
#     db.session.commit()
#     flash("删除完成")
#     return redirect(url_for('index'))



# # 登录
# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if not username or not password:
#             flash('错误')
#             return redirect(url_for('login'))
#         user = User.query.first()
#         # 验证信息
#         if username == user.username and user.validate_password(password):
#             login_user(user)
#             flash('登录成功')
#             return redirect(url_for('index'))
#         flash('验证错误')
#         return redirect(url_for('login'))
#     return render_template('login.html')



# # 登出
# @app.route('/logout')
# def logout():
#     logout_user()
#     flash('拜拜')
#     return redirect(url_for('login'))

# # settings 设置
# @app.route('/settings',methods=['GET','POST'])
# @login_required
# def settings():
#     if request.method == 'POST':
#         name = request.form['name']
#         if not name or len(name)>20:
#             flash('输入错误')
#             return redirect(url_for('settings'))
#         current_user.name = name
#         db.session.commit()
#         flash('名称已经更新')
#         return redirect(url_for('index'))

#     return render_template('settings.html')
# # 动态url
# @app.route('/index/<name>')
# def home(name):
#     return "<h1>hello,Flask,%s</h1>" %name





# 自定义命令
# 新建data,db 的数据库初始化命令
# @app.cli.command()   #这个装饰器可以注册命令
# @click.option('--drop',is_flag = True,help = '删除后再创建')
# def initdb(drop):
#     if drop:
#         db.drop_all()

#     db.create_all()
#     click.echo('初始化数据库完成')

# 向data.db中写入数据的命令

# @app.cli.command()
# def forge():
#     name = "中国"
#     movies = [
#         { "title" : "大赢家" , "year" : "2020" },
#         { "title" : "叶问四" , "year" : "2020" },
#         { "title" : "唐人街探案" , "year" : "2020" },
#         { "title" : "囧妈" , "year" : "2020" },
#     ]

#     user = User(name = name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movies(title = m['title'],year = m['year'])
#         db.session.add(movie)
#     db.session.commit()
#     flash('导入数据完成')


# 生成管理员账号
# @app.cli.command()
# @click.option('--username',prompt=True,help="管理员账号")
# @click.option('--password',prompt=True,help="管理员密码" ,hide_input=True,confirmation_prompt=True)
# def admin(username,password):
#     db.create_all()
#     user = User.query.first()
#     if user is not None:
#         click.echo('更新用户信息')
#         user.username = username 
#         user.set_password(password)
#     else:
#         click.echo('创建用户信息')
#         user = User(username=username,name='Admin')
#         user.set_password(password)
#         db.session.add(user)
#     db.session.commit()
#     click.echo('管理员创建完成')

# # 错误处理函数
# @app.errorhandler(404)
# def page_not_found(e):
#     user = User.query.first()
#     # 返回模板和状态码
#     return render_template('404.html'),404




