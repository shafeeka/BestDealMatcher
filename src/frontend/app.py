from flask import Flask,request,send_file,render_template,url_for,abort,session, flash
from werkzeug.utils import secure_filename

import pandas as pd
import datetime as dt
import sys,os


sys.path.insert(0, os.path.abspath("../predictionModel"))
import matchingModel 

app = Flask(__name__)

@app.route('/reccomendations', methods =['POST','GET'])
def getRecommendation():
    if request.method == "GET":
        print("in GET request")
        try:
            name=getName()
            dfReturned = matchingModel.matchingModel(name)
            print(dfReturned)
            print(len(dfReturned.index))
            return dfReturned.iloc[: , :-1].to_html(index=False)
        except:
            abort(400)

@app.route('/')
def getstarted():
    return render_template('getstarted.html')

@app.route('/home')
def home():
    # if not session.get('logged_in'):
    #     return render_template('signin.html')
    # else:
    #     return render_template('home.html')
    return render_template('home.html')

@app.route('/signin')
def sigin():
    return render_template('signin.html')

@app.route('/signin', methods=['POST'])
def do_admin_login():
  login = request.form

  userName = login.get('username')
  password = login.get('password')

#   account = True

#   cur = mariadb_connect.cursor(buffered=True)
#   data = cur.execute('SELECT * FROM Login WHERE username=%s', (userName))
#   data = cur.fetchone()[2]

  if userName=='Richard Roberts' and password=='123':
    account = True

  if account:
    session['logged_in'] = True
  else:
    flash('wrong password!')
  return home()

@app.errorhandler(400)
def page_not_found(e):
    # note that we set the 400 status explicitly
    return render_template('400.html'), 400
def getName():
    return "Richard Roberts"

if __name__ == '__main__':
    app.run(debug=True)