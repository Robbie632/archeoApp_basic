from pymongo import MongoClient


#connect to 'mongo' container, port 27017 comes exposed by default in the mongo
#image

client = MongoClient('mongodb://root:example@mongo:27017')

#create or access my datbase
mydb = client['artefacts']

#create or access my collection
mycollection = mydb['mass_spec_data']

#data to write to db
my_dict = {'artefact_name':'test_name', 'location':'test_location', 'Mg':'12', 'Cs':'24'}

#insert data into collection as a document and store automatically generated
#id as a variable here
insertedID = mycollection.insert_one(my_dict).inserted_id
