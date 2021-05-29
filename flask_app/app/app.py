from flask import Flask, render_template, request
import os
from flask import send_from_directory, flash, request, redirect, url_for, session, send_file
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField,
    RadioField, SelectField, TextField, TextAreaField)
from flask_dropzone import Dropzone
import pickle
from wtforms.validators import DataRequired
from forms.forms import infoForm
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import os
import sys
from absl import app
from absl import flags

from google.cloud import storage
from io import StringIO




##################################################################
#plotly
# helpful plotly linkhttps://stackoverflow.com/questions/36262748/python-save-plotly-plot-to-local-file-and-insert-into-html
import json
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot, iplot
##################################################################

FLAGS = flags.FLAGS

flags.DEFINE_boolean("dev",
                     False,
                     "defines if running app locally or in google cloud run platform"      
                    )

# code below necessary because cant use absl app because interferes with flasks app
# source: https://medium.com/dive-into-ml-ai/flask-webapi-with-absl-py-flags-for-an-image-based-input-output-model-8f41cf05ce7b
FLAGS(sys.argv)


#__file__ is automatically created when module ran, it takes on the name of the file eg app.py
#so below we are getting the absolute path to the current directory that the app.py file   is in
base_dir = os.path.abspath(os.path.dirname(__file__))
filepath = os.path.join(base_dir, 'uploads')
#instantiate Flask object
app = Flask(__name__)





le = LabelEncoder()


#below sets the secret key for forms
app.config['SECRET_KEY'] = 'mySecretKey'

app.config.update(
    UPLOADED_PATH=filepath,
    # Flask-Dropzone config:

    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE='.csv',
    #DROPZONE_MAX_FILE_SIZE=300,
    DROPZONE_MAX_FILES=30,
    DROPZONE_REDIRECT_VIEW='see_model_results'
)


dropzone = Dropzone(app)


#set route for page where data can be inputted by user
@app.route('/visualisations', methods = ['GET', 'POST'])
def visualisations():

    dataset = False
    visualisation_type = False
    #make instance of class infoForm
    form = infoForm()
    #check it's valid

    if form.validate_on_submit():


        dataset = form.dataset.data
        visualisation_type = form.visualisation_type.data
        if visualisation_type == 'pca':
            if dataset == "bedrock":
                data = pd.read_csv('data/pca_bedrock.csv')
            elif dataset == "superficial":
                data = pd.read_csv('data/pca_superficial.csv')
            elif dataset == "bedrock_and_superficial":
                data = pd.read_csv('data/pca_both.csv')
            elif dataset == "artefacts":
                data = pd.read_csv('data/pca_artefacts.csv')
            elif dataset == 'samples_and_artefacts':
                data = pd.read_csv('data/pca_samples_and_artefacts.csv')
        elif visualisation_type == 'tsne':
            if dataset == "bedrock":
                data = pd.read_csv('data/tsne_bedrock.csv')
            elif dataset == "superficial":
                data = pd.read_csv('data/tsne_superficial.csv')
            elif dataset == "bedrock_and_superficial":
                data = pd.read_csv('data/tsne_both.csv')
            elif dataset == "artefacts":
                data = pd.read_csv('data/tsne_artefacts.csv')
            elif dataset == 'samples_and_artefacts':
                data = pd.read_csv('data/tsne_samples_and_artefacts.csv')

        data['class_numeric'] = le.fit_transform(data['class'])

        colNames = list(data.columns.values)
        col1 = colNames[0]
        col2 = colNames[1]
        col3 = colNames[2]

        # Create a trace
        trace = go.Scatter3d(
            x = data[col1],
            y = data[col2],
            z = data[col3],
            mode = 'markers',
            text = data['class'],
            opacity = 0.7,
            marker = dict(
                size = 7,
                color = data['class_numeric'],
                colorscale = 'Rainbow',
        ))


        layout = go.Layout(autosize=False,width=1000, height=800, title = visualisation_type)
        dataForPlot = [trace]
        fig = dict(data=dataForPlot, layout=layout)
        graphDiv = plot(fig, output_type='div')

        #render html template for form response passing in variables
        return(render_template('form_response.html', form = form, graphDiv = graphDiv))
        #render form template
    return(render_template('visualisations.html', form = form, dataset=dataset, visualisation_type=visualisation_type))


#set path to home page
@app.route('/')
def home():
	return(render_template('home.html'))
#set path to form response page
@app.route('/submitted')
def form_response():
    return(render_template('form_response.html'))

#set path to contact page
@app.route('/contact')
def contact():
    return(render_template('contact.html'))


#set path to model details page
@app.route('/visualisation_details')
def visualisation_details():
	return(render_template('visualisation_details.html'))

#set path to about the developer page
@app.route('/about_the_developer')
def about_the_developer():
	return(render_template('about_the_developer.html'))

@app.route('/run_model')
def run_model():
	return(render_template('run_model.html'))

#set path to modle origins page
@app.route('/research')
def research():
	return(render_template('research.html'))

@app.route('/get_dropzone')
def get_dropzone():
	return(render_template('dropzone.html'))

@app.route('/see_model_results')
def see_model_results():
    return(render_template('see_model_results.html'))



@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        predict_data = {}
        status = "success"
        prediction_number = ["NA"]

        #run model here and save results to json for now

        f = request.files.get('file')

        if not f:
          return "No file uploaded", 400

        if not FLAGS.dev:

          gcs = storage.Client()

          bucket = gcs.get_bucket("gs://archeo_uploads")

          blob = bucket.blob(f.filename)

          blob.upload_from_string(
              f.read(),
              content_type=f.content_type
          )
        else:

          #save uploaded file
          f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))


        #makes predictions and returns results
        encodings = {0: 'FH',
        1: 'ER',
        2: 'WW',
        3: 'TC',
        4: 'CS',
        5: 'KQ',
        6: 'AR',
        7: 'SL',
        8: 'FG',
        9: 'WB',
        10: 'PF',
        11: 'WH',
        12: 'SQ',
        13: 'WN',
        14: 'BH',
        15: 'PH',
        16: 'LB',
        'NA':'NA'
        }

        
        #load model
        loaded_model = pickle.load(open('models/rfc_model.sav', 'rb'))
        if FLAGS.dev:
          data = pd.read_csv(os.path.join(app.config['UPLOADED_PATH'], f.filename))
        else:
          
          #this code from video https://www.youtube.com/watch?v=ED5vHa3fE1Q
          blob = bucket.get_blob(f.filename)
          bt = blob.download_as_string()
          s = str(bt, "utf-8")
          s = StringIO(s)
          data = pd.read_csv(s)
   


        features = ['Zr90', 'Ba137', 'Sr88', 'Ge72', 'Cr52', 'S33', 'U238', 'Al27', 'B11', 'Mg24', 'Nd146', 'Sc45', 'K39', 'Pr141', 'Li7']
        
        read_feats = [c for c in data.columns.values if c in features or c.lower() in features or c.upper() in features]
        try:
          data_feats = data[read_feats]
        except ():
          status = "bad column names"
          
        try:
          prediction_number = loaded_model.predict(data_feats)
        except:
          status = "corrupt data"

        predicted_class = encodings[prediction_number[0]]
        
        predict_data["prediction"] = predicted_class
        #write results to json file
        predict_data["status"] = status

        if FLAGS.dev:
          with open("results.json", "w") as f:
            json.dump(predict_data, f)
        else:

          'code below from https://medium.com/analytics-vidhya/how-to-write-and-get-a-json-file-in-google-cloud-storage-when-deploying-flask-api-in-google-app-9121fa936d85'
          blob = bucket.blob("results.json")

          blob.upload_from_string(
              predict_data,
              content_type="'application/json'"
          )

          # write to bucket

@app.route('/model_run')
def model_run():

    # read json file containing predictions then render in html
    if FLAGS.dev:
      with open("results.json", "r") as f:
        data = json.load(f)
    else:
      gcs = storage.Client()

      bucket = gcs.get_bucket("gs://archeo_uploads")
      blob = bucket.blob("results.json")
      #read bucket
      data = json.loads(blob.download_as_string())


    return(render_template('see_classification.html', predicted_class=data["prediction"], status = data["status"]))


#the below code runs the app only when it is being run from command line instead of from within a module
if __name__ ==	'__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port, debug = True)
