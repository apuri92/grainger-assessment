# Grainger Assessment


# Files
The repository includes the following files:
* `source.run`: This script will run the full analysis chain.
* `requirements.txt`: This contains a list of the required packages.
* `analysis.ipynb`: The jupyter notebook that contains the code to conduct EDA and produce the model.
* `PipelineObjects.py`: This contains definitions for some custom transformers.
* `server.py`: This sets up the model server.
* `request.py`: This has a sample of how to run a prediction.


# Instructions

## Setup
Run the `source.run` file as below:
```sh
source ./source.run
```

This will do the following:
* Download the data if it is not already available as `./data.csv` in the top level directory (this can take time depending on your internet speed).
* Install the packages listed in `requirements.txt`.
* Run the `analysis.ipynb` to produce the `model.pkl` (this can take several minutes to load the data and train the model).
* Run `server.py` to load the model and start the server.

Once the server starts, open a new terminal and navigate to the repoistory folder and run `requests.py` to send a request with features to receive a prediction probability.

## Predictions
Predictions can be made by sending a request to the model server in the following format:
```python
url = 'http://localhost:5000/predict'
r = requests.post(url,json={'Color':'BK', 'BodyStyle': 'PA', 'StatePlate': 'CA'})
```

Running the `server.py` file returns a response as below:
```sh
{'prediction': 0.9189022476315752}
```

Note: The name of the input features may be different from the column name as specified in the csv provided.


# Analysis
The original dataset contained a missing `'Make'` field. Once these were removed, the dataset contained approximately 4M records. Of these, approximately 91% were from the top 25 manufacterers.

The EDA revealed a dataset with a number data-quality issues ranging from minor (column names needed re-naming) to major (dates and times had numerous inconsistencies).

Based on the task of predicting a record as being from a top 25 manufacturer, the features that seemed most promising were the following:
* RP State Plate (encoded as 'StatePlate')
* Body Style (encoded as 'BodyStyle')
* Color

Initial analysis showed that these were high cardinality features, taking up to ~50 variations. The high-cardinality features were dealt with by aggregating them as described in the next section

## Aggregating High Cardinality Features
One Hot Encoding is not preferred when dealing with high cardinality features since it will result in sparse matrices and a large dataset. Instead, the following approach was taken:
* For a given high-cardinality feature, pick a threshold.
* Get a list of the values that feature can take, sorted in descending order by frequency.
* Cumulatively add the frequencies until the threshold percentage is reached, these values are left as is.
* The remaining values are combined into an 'Other' category.

The aggregated feature can then be simply one hot encoded using standard methods.

Optional: Replace the values with their frequency to obtain a numeric feature

NOTE: Unknown categories seen when predicting a probability are treated as belonging to 'Other'

## Model Pipeline
The pipeline comprised of the following steps:
* `FeatureSelector()`: Pick out the necessary features from a given input
* `CategoryAggregator()`: Perform the aggregation as outlined above
* `NumericTransformer()`: Performs an imputation and scaling for numeric data
* `CategoricalTransformer()`: Performs an imputation and OneHotEncoding for categorical data
* `RandomForestClassifier()`: The model chosen for the classification task

Performing all the pre-processing in the pipeline ensures that the model can be used directly on a minimally processed dataset.

## Training/Testing
The dataset was split into a training/test set, where the training data was used to train the model. This can take upto 10 minutes on the full dataset (using a 2.7 GHz Dual-Core Intel Core i5).

The test set was then used to determine model performance as shown below:
* ROC: 0.66
* Average Precision: 0.94


# Future Work
* The top 25 manufacturers can change over time, making it important that the model is re-trained on a regular basis. It is also important to keep track of what model version is used for which predictions. This can be achieved with MLFlow.
* Hyperparameter tuning needs to be done to ensure optimum model performance. This can be achieved with the `sklearn` functions `GridSearchCV()`, `RandomizedSearchCV()` or the `hyperopt` library.
* Since this model is dealing with an imbalanced dataset, it is important to understand the business requirements and adjust the prediction threshold appropriately. This can be done by calculating the f-beta score after weighting the precision / recall as needed.
* The model can potentially be improved by considering the following:
  * Location: This would involve cleaning the locations as specified in the dataset and performing an aggregation as outlined.
  * Date/Time features: This requires substantial effort as these features have a number of inconsistencies.