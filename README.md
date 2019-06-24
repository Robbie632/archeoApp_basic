## ArcheoViz


### This is a website-application that allows visualisation of t-SNE and PCA projections of flint sample and artefact data. This work was originally presented in the paper (ref), link below. 


* First the repository needs to be cloned

* Then change directory into the repo:
`cd archeoApp_basic/`

* The docker image needs to be made:
`docker build -t archeoapp .`

* The container needs to be run from the docker image:

`docker run -p 5000:5000 -d archeoapp`

*Go to the following URL:

http://0.0.0.0:5000









