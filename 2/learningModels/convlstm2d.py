from sys import displayhook
import json
import tensorflow as tf
import numpy as np # linear algebra
import pandas as pd 


def predict():

    data = pd.read_csv('C:/Users/doguk/Desktop/data/data/CA_B8_31_00_00_64_.csv')

    lendata = len(data)

    data.index = pd.to_datetime(data["createdAt"], format = "%Y-%m-%dT%H:%M:%S.%fZ")
    data = data.iloc[:, 8:]
    features_considered = list(data.columns)
    features = data[features_considered]

    denemeicin = 3

    model = tf.keras.models.load_model("C:/Users/doguk/Desktop/Yeni klasör/2/learningModels/multi-output-timesteps.h5")

    predicts = pd.DataFrame(model.predict(np.array(data[lendata-10 - denemeicin:lendata - denemeicin]).reshape(1,10,16,1,1)).reshape(-1,16), columns = features.columns)


    print("Tahmin değerler\n\n")
    displayhook(pd.DataFrame(predicts, columns = features.columns)),

    print("\n\nDoğru olan değerler\n\n")
    displayhook(pd.DataFrame(np.array(data[lendata - denemeicin:lendata]), columns = features.columns))

    result = predicts.to_json(orient="split")
    parsed = json.loads(result)
    json.dumps(parsed) 
    
    return result

predict()