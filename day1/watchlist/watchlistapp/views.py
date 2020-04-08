from watchlistapp import app,db
from watchlistapp.models import User,Movies
from flask import render_template,flash,redirect,request,url_for
from flask_login import LoginManager,login_user,logout_user,login_required,current_user


# view视图
# @app.route('/')
# @app.route('/index')
# @app.route('/home')
@app.route('/',methods=['GET','POST'])
def index():
    # user = User.query.first()
    # requesr在请求出发才会包含数据
    if request.method == 'POST':
        # if not current_user.is_authenticated
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
@login_required
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
@login_required
def delete(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除完成")
    return redirect(url_for('index'))



# 登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('错误')
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证信息
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功')
            return redirect(url_for('index'))
        flash('验证错误')
        return redirect(url_for('login'))
    return render_template('login.html')



# 登出
@app.route('/logout')
def logout():
    logout_user()
    flash('拜拜')
    return redirect(url_for('login'))

# settings 设置
@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('名称已经更新')
        return redirect(url_for('index'))

    return render_template('settings.html')
# # 动态url
# @app.route('/index/<name>')
# def home(name):
#     return "<h1>hello,Flask,%s</h1>" %name