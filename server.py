# Import libraries
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model
model = pickle.load(open('model.pkl','rb'))

@app.route('/predict',methods=['POST'])
def predict():
    # Get the data from the POST request and convert it to a dataframe.
    data = request.get_json(force=True)
    df = pd.DataFrame(data,index=['i',])
    
    # Make prediction using model loaded from disk as per the data.
    output = model.predict_proba(df)[0,1]
    
    return jsonify({'prediction': output})

if __name__ == '__main__':
    app.run(port=5000, debug=True)