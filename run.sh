#!/bin/bash

# Download data file (if it does not exist)
FILE="./data.csv"
if test -f "$FILE"; then
  echo "$FILE already exists, skipping download..."
else
  echo "$FILE does not exist, downloading with curl..."
  curl https://s3-us-west-2.amazonaws.com/pcadsassessment/parking_citations.corrupted.csv --output $FILE
  echo "Data downloaded to $FILE"
fi

# Get libaries
echo "Installing required libraries"
pip3 install -q -r requirements.txt

# Run analysis
echo "Starting analysis... Running Jupyter notebook. This can take time"
jupyter nbconvert --execute --to notebook --inplace analysis.ipynb


# Start server
echo "Starting server.. Open new terminal and send requests with requests.py"
python ./server.py