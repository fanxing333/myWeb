from flask import Flask, url_for, render_template, flash, request, redirect
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',	'dev')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/flask')
def flask():
    return render_template('flask.html')

@app.route('/bigdata')
def bigdata():
    return render_template('bigdata.html')

@app.route('/cplex')
def cplex():
    return render_template('cplex.html')

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')





@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)