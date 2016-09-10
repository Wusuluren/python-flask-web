from flask import Flask
from flask import make_response
from flask import redirect
from flask_script import Manager
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import session, url_for
from flask import flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_script import Shell

#表单
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'sqlite/data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#数据库
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,  primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username        


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

@app.route('/bootstrap_form', methods=['GET', 'POST'])
def bootstrap_form():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data        
        return redirect(url_for('bootstrap_form'))
    return render_template('bootstrap_form.html', 
        name=session.get('name'), form=form)

'''
SQLAlchemy数据库
'''
def InitSqlAlchemy():
    db.drop_all()
    db.create_all()
    admin_role = Role(name='Admin')
    user_john = User(username='john', role=admin_role)
    db.session.add_all([admin_role, user_john])
    db.session.commit()

@app.route('/sqlalchemy', methods=['GET', 'POST'])
def sqlalchemy():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('sqlalchemy'))
    return render_template('sqlalchemy.html',
        form=form, name=session.get('name'),
        known=session.get('known', False))

'''
Python shell
'''
def make_shell_contex():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_contex))

'''
main函数
'''
if __name__ == '__main__':
    #app.run(debug=True, port=5002)
    InitSqlAlchemy()
    manager.run()