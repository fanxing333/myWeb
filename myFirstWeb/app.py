from flask import Flask, url_for, render_template, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import click
import os
import sys



#基本配置
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',	'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.context_processor
def	inject_user():
    user = User.query.first()
    return dict(user=user)

#命令配置
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login')
def admin(username, password):
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
def forge():
    '''db.create_all()'''
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    todos = [
        {'text': '今日计划A', 'date': datetime.date(2020, 3, 25), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划B', 'date': datetime.date(2020, 3, 24), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划C', 'date': datetime.date(2020, 3, 23), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划D', 'date': datetime.date(2020, 3, 22), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划E', 'date': datetime.date(2020, 3, 21), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划F', 'date': datetime.date(2020, 3, 20), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划G', 'date': datetime.date(2020, 3, 19), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划H', 'date': datetime.date(2020, 3, 18), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划I', 'date': datetime.date(2020, 3, 17), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '今日计划J', 'date': datetime.date(2020, 3, 16), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'day'},
        {'text': '本周计划K', 'date': datetime.date(2020, 3, 16), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'week'},
        {'text': '本周计划L', 'date': datetime.date(2020, 3, 18), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'week'},
        {'text': '长期计划M', 'date': datetime.date(2020, 3, 18), 'is_important': True,
         'is_urgent': True, 'ps': '这是备注', 'status': 'long-term'},

    ]
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    for t in todos:
        todo = Todo(text=t['text'], date=t['date'], status=t['status'], is_important=t['is_important'], is_urgent=t['is_urgent'], ps=t['ps'])
        db.session.add(todo)
    db.session.commit()
    click.echo('Done.')
# 数据库配置
db = SQLAlchemy(app)
#用户表
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
#电影表
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
#计划表
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    status = db.Column(db.String(10))
    is_important = db.Column(db.Boolean)
    is_urgent = db.Column(db.Boolean)
    is_done = db.Column(db.Boolean)
    is_giveup = db.Column(db.Boolean)
    ps = db.Column(db.Text)
#博客表
class blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    text = db.Column(db.Text)
    time = db.Column(db.DateTime)


#注册
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for(login))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye')
    return redirect(url_for('home'))

@app.route('/flask')
def flask():
    return render_template('flask.html')

@app.route('/bigdata')
def bigdata():
    return render_template('bigdata.html')

@app.route('/cplex')
def cplex():
    return render_template('cplex.html')

@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            title = request.form.get('title')
            year = request.form.get('year')
            if not title or not year or len(year) > 4 or len(title) > 60:
                flash('Invalid input.')
                return redirect(url_for('watchlist'))

            movie = Movie(title=title, year=year)
            db.session.add(movie)
            db.session.commit()
            flash('Item created.')
            return redirect(url_for('watchlist'))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('watchlist.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
        # 重定向回对应的编辑页面
        movie.title = title # 更新标题
        movie.year = year # 更新年份
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('watchlist')) # 重定向回主页
    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('watchlist'))



@app.route('/plan')
def plan():
    todos = Todo.query.filter(Todo.status=='day').all()
    weeks = Todo.query.filter(Todo.status=='week').all()
    longterms = Todo.query.filter(Todo.status=='long-term').all()

    today = datetime.date.today()
    weekday = DayOfWeek(today)

    todolist=[]
    for i in range(7):
        nextday = datetime.date.today() + datetime.timedelta(-1*i+1)
        preday = nextday + datetime.timedelta(-1)
        todolist.append(Todo.query.filter(Todo.date.between(preday,nextday)))

    return render_template('plan.html', todos=todos, weeks=weeks, longterms=longterms, weekday=weekday,
                           todolist=todolist)

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')





@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')

'''if __name__ == '__main__':
    app.run(port=5000, debug=True)'''

def DayOfWeek(time):
    week = [
        '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天'
    ]
    weeks = ['今日']
    for i in range(6):
        weeks.append(week[(time.weekday()-i-1)%7])
    return weeks

'''time = datetime.datetime.now()
print(DayOfWeek(time)[0])'''
'''time = Todo.query.first().date
print(time)

tom = today + timedelta.days(-1)
todos = Todo.query.filter(Todo.date.between('today', 'tom')).all()'''
'''today = datetime.date.today()
todos = Todo.query.filter(db.cast(Todo.date, db.DATE) == db.cast(datetime.datetime.now(), db.DATE)).all()
print(todos)'''
#todos=Todo.query.filter(db.cast(Todo.date, db.DATE) == db.cast(datetime.datetime.now(), db.DATE)).all()
