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
import os



##################################################################
#plotly
# helpful plotly linkhttps://stackoverflow.com/questions/36262748/python-save-plotly-plot-to-local-file-and-insert-into-html
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot, iplot
##################################################################
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
    DROPZONE_ALLOWED_FILE_TYPE='.mp4',
    #DROPZONE_MAX_FILE_SIZE=300,
    DROPZONE_MAX_FILES=30,
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
        col1 = colNames[1]
        col2 = colNames[2]
        col3 = colNames[3]

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

@app.route('/model_results')
def model_results():
	return(render_template('model_results.html'))

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':


        f = request.files.get('file')

        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

    return(render_template('model_results.html'))


#the below code runs the app only when it is being run from command line instead of from within a module
if __name__ ==	'__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port, debug = True)
