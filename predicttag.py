from keras import models
import pandas as pd
import sys

sys.path.append("Job Tag Classifier Tools")
from Pipeline import DataLoader, BatchData
import UpdateClassifier

# ["dbname='job_tag_classifier' host='localhost' port='5432' user='postgres' password='1234'", "select * from job_data;"]
# ["dbname='job_tag_classifier' host='127.0.0.1'", "select * from job_data;"]
sql_import_string = ["dbname='job_tag_classifier' host='127.0.0.1'", "select * from job_data LIMIT 1 OFFSET 20;"]
X, _, Y, _ = DataLoader(sql_import_string, test_size=0)


# encode the Input
encoder = models.load_model("Models/encoder_model")
X_encoded = encoder.predict(X)

# load models
model = models.load_model("Models/classifier_model")
list_of_indices = model.predict(X_encoded)

# decode the target back into text - make sur excepts may rows of data
predicition = tag_decoder(list_of_indices, threshold=.2)

# add the new data to a sql table to save for a training batch
sql_add_new_data_string = ['postgresql://127.0.0.1/job_tag_classifier', "new_data"]
update = BatchData(sql_import_string, sql_add_new_data_string)

# update the model and reset the new_data table
if update:
    update_classifier()