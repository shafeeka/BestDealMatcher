from flask import Flask,request,send_file,render_template,url_for,abort
from werkzeug.utils import secure_filename

import pandas as pd
import joblib
import datetime as dt
import sys,os

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn import preprocessing
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.abspath("../predictionModel"))
import matchingModel 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/signin')
def sigin():
    return render_template('signin.html')

@app.route('/recommendation', methods =['POST','GET'])
def getRecommendation():
    if request.method == "POST":
        try:
            name="Richard Roberts"
            dfReturned = matchingModel.matchingModel(name)
            # return df
            return render_template("reccomendations.html", df=dfReturned)
        except:
            abort(400)

@app.errorhandler(400)
def page_not_found(e):
    # note that we set the 400 status explicitly
    return render_template('400.html'), 400

if __name__ == '__main__':
    app.run(debug=True)