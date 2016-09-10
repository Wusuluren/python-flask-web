from flask import Flask
from flask import make_response
from flask import redirect
from flask_script import Manager
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

@app.route('/bad')
def bad():
    return '<h1>Bad Request</h1>', 400

@app.route('/response')
def response():
    response = make_response('<h1>This document carries a cookies!</h1>')
    response.set_cookie('answer', '42')
    return response    

@app.route('/baidu')
def baidu():
    return redirect('http://www.baidu.com')

'''
Jinja2模板
'''
@app.route('/jinja2')
def jinja2_index():
    return render_template('jinja2.html')

age = {'nano':18, 'post':24, 'wusu':30}
#age = {'nano':'<h1>18</h1>', 'post':'<h1>24</h1>', 'wusu':'<h1>30</h1>'}
comments = ['This', 'is', 'a', 'comment']
@app.route('/jinja2_user/<name>')
def jinja2_user(name):
    return render_template('jinja2_user.html', 
        name=name, age=age, comments=comments)

'''
bootstrap模板
'''
@app.route('/bootstrap')
def bootstrap_index():
    return render_template('bootstrap_index.html', 
        current_time=datetime.utcnow())

@app.route('/bootstrap_user/<name>')
def bootstrap_user(name):
    return render_template('bootstrap_user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('bootstrap_404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('bootstrap_500.html'), 500


'''
main函数
'''
if __name__ == '__main__':
    #app.run(debug=True, port=5002)
    manager.run()