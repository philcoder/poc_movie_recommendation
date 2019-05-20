from flask import render_template
from app import app

'''
route exemple: http://localhost:16000/webui/login
'''

@app.route('/webui/hello')
def hello_world():
    return 'hello world inside docker'

@app.route('/webui/rota2')
def rota2():
    return 'usando uma rota2'

@app.route('/webui/pagetest')
def pagetest():
    import datetime
    userdata = {
        'username' : 'Philipp',
        'date' : datetime.datetime.utcnow()
    }
    return render_template('home.html', data=userdata)

@app.route('/webui/login')
def login():
    return render_template('login.html', disablemenu=True)