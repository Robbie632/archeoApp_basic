## ArcheoViz


### This is a web application that allows visualisation of t-SNE and PCA projections of flint sample and artefact data. 

To use this web application you must first install Docker.

* The repository needs to be cloned

* Then change directory into the repo:

`cd archeoApp_basic/`

* The docker image needs to be made:

`docker-compose up` 

* Go to the following URL:

http://0.0.0.0:5000

This is the home page:
![alt text](screenshots/archeo_home.png "Home")

Go to the 'visualisations' page to input which dataset and which transformation you would like to visualise:
![alt text](screenshots/archeo_form.png "form")

This s an example of the types of visualisation that can be visualised and interacted with, hovering of the right hand corner of the visualisation box gives options for how to interact with the plot.
![alt text](screenshots/archeo_viz.png "visualisation")




https://towardsdatascience.com/deploy-a-dockerized-flask-app-to-google-cloud-platform-71d91b39b25e
I created a GCP bucket using the cloud run command line associated with my project and using gsutils

https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-gsutil

gcloud builds submit --tag gcr.io/PROJECT-ID/container-name --project <project name>

gcloud run deploy --image gcr.io/PROJECT-ID/container-name --platform managed --project <project name>

update running container:
https://cloud.google.com/run/docs/deploying

Run build command in folder with dockerfile?


https://cloud.google.com/appengine/docs/flexible/python/using-cloud-storage