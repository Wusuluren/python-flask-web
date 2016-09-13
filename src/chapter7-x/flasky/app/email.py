from flask import render_template
from flask_mail import Message
from threading import Thread
from flask import current_app

from . import mail
from .main import main

'''
#测试
def TestSendMail():
    msg = Message('test subject', sender=MAIL_SENDER,
        recipients=[MAIL_RECEIVER])
    msg.body = 'test body'
    msg.html = '<b>HTML</b> body'
    with app.app_context():
        mail.send(msg)

#同步
def send_email(to, subject, template, **kwargs):
    msg = Message(MAIL_SUBJECT_PREFIX+subject,
        sender=MAIL_SENDER,
        recipients=[to])
    msg.body = render_template(template + '.text', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@main.route('/email_index')
def email_index():
    if MAIL_RECEIVER is not None:
        send_email(MAIL_RECEIVER, 'new email',
        'mail/email_index')
    return render_template('mail/email_sent.html', 
        msg='A email has been sent!')
'''

#异步
def send_async_email_thread(app, msg):
    with app.app_context():
        mail.send(msg)

def send_async_email(app, to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX']+subject,
        sender=app.config['MAIL_SENDER'],
        recipients=[to])
    msg.body = render_template(template + '.text', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email_thread, args=[app, msg])
    thr.start()
    return thr
    
@main.route('/email_async')
def email_async():
    app = current_app._get_current_object()
    if app.config['MAIL_RECEIVER']:
        send_async_email(app, app.config['MAIL_RECEIVER'], 'new async email',
        'mail/email_index')
    return render_template('mail/email_sent.html', 
        msg='A async email has been sent!')