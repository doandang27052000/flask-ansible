from flask import Flask, render_template, redirect, request, session
from models import model
import pandas as pd
import os

app = Flask(__name__, template_folder='templates', static_folder = 'static')



@app.route('/')
def welcome():
    return redirect('/index.html')

@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/logout', methods=['GET'])
def getLogout():
    session.pop('username')
    return render_template('index.html')


@app.route('/view_data.html', methods = ['GET', 'POST'])
def data():
    files = os.listdir("data")
    if request.method == "POST":
       data1 = request.form.get('comp_select')
       full_data = pd.read_csv('data/%s' %data1)
       return render_template('view_data.html', tables=[full_data.to_html(classes='data')], titles=full_data.columns.values, files = files)
    return render_template('view_data.html', files = files)

@app.route('/upload_data.html', methods=['GET','POST'])  
def uploadFile():
    files = os.listdir("data")
    if request.method == "POST":
        file = request.files['file']
        file.save(os.path.join('data', file.filename))
        return render_template('upload_data.html', message = "success")
    return render_template('upload_data.html')
@app.route('/detection.html', methods=['GET', 'POST'])
def detection():
    files = os.listdir("data")
    if request.method == "POST":
        data1 = request.form.get('comp_select')
        df = pd.read_csv('data/%s' % data1)
        predictions = model.pre_carinsurance(df)
        return render_template('detection.html', tables=[predictions.to_html(classes='data')], titles=predictions.columns.values, files = files)
    return render_template('detection.html', files = files)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
