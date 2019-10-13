from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, 
    RadioField, SelectField, TextField, TextAreaField)
from wtforms.validators import DataRequired



#set up my own class for forms by inheriting from class FlaskForm
class infoForm(FlaskForm):
    #define form fields
    
    dataset = SelectField('dataset', choices = [('superficial', 'superficial'), ('bedrock', 'bedrock'), ('bedrock_and_superficial', 'bedrock and superficial'), ('artefacts', 'artefacts'), ('samples_and_artefacts','samples_and_artefacts')])
    visualisation_type = SelectField('visualisation_type', choices = [('tsne', 'tsne'), ('pca', 'pca')])
    submit = SubmitField('submit ')