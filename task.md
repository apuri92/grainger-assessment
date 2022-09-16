# Applied Machine Learning Scientist Assessment
This is an assessment to evaluate your approach a typical data science task. It's entirely optional.  However, if you do decide to dig into it, it can help me decide whether you're a good fit for our team.

## Traffic Citations Modeling Pipeline

The goal is to set up a reproduceable set of transformation and modeling operations and deploy a model server.

The final deliverable: A git repo hosted on github containing all component deliverables.  I should be able to clone the repo and reproduce the experiments locally from start to finish including:
getting the data from s3
training the model
launching the model server.  

The repo should contain at least:
* main deliverable: a single bash script named "run.sh" that will allow me to run the entire modeling pipeline and launch the server
note: You can assume I'll run the script from the root directory of the repo.  Don't get fancy with path stuff and directory structure.
* jupyter notebook(s) for exploratory / explanatory components
* all necessary python scripts for generating outputs
* any instructions necessary to ensure that I can reproduce this result or to direct my attention to the right places

* The language must be Python.

## Data

https://s3-us-west-2.amazonaws.com/pcadsassessment/parking_citations.corrupted.csv


## Model Deliverable:

There are about 8 million rows in this dataset.  Some car manufacturers are more common than others.  

The "setup" is: Someone has accidentally deleted the "Make" column from 1/2 of the database, yielding the "parking_citations.corrupted.csv" file.

A business partner has asked you to use the magic of A.I to determine the probability that a user is driving a popular make using the rest of the features trained on the uncorrupted 1/2 of the data.

You've accepted the task.

**Build a model to calculate the probability that a car is made by one of the top 25 manufacturers in this dataset based on the uncorrupted features.**
        
**Deliver an explanation of the quality of this model and feasibility of this task to your imaginary business partner.  Help your business partner understand the strengths and weaknesses of this model.**

## Model Server Deliverable:
        
Deploy a local server (that will only be used locally) to allow a user to submit a corrupted row in some format and receive the probability of a top 25 'Make' in return.

You are free to use your favorite Python server library.

The server should: 
* work with a post request on the route `/predict`
* expect a json of features.  Ex: `{'Color':'GR', 'Latitude':63453.0}` etc.
* return a json with a "prediction" field and the appropriate model output value

I'll test it by launching it myself and querying it from my own machine, so it only needs to work in that context. 

Don't do anything fancy, just get it working.  Your business partner just wants the predictions.  


## Expository / Exploratory Analysis:

Model explanation / analysis should be delivered in a Jupyter notebook.  

Any data analysis, for example your initial data exploration, or anything else of this manner you'd like to share can be delivered as one or more other Jupyter notebooks.



## Advice:

The modeling portion of this is a little open ended.  If you're doing something that feels like a waste of time, it probably is.  Just submit something simple and solid that reflects your typical approach to modeling tasks.  The accuracy isn’t too important.

It’s not necessary to complete everything.  Think of each deliverable as an opportunity.  I know not all of us have a ton of time to waste on assessments.  

If you're having some trouble, please feel free to ask me whatever you want.  I mean this assessment to allow me glimpses both into your work as well as what it might be like to work with you.  

Also: If something about this assessment seems strange, incorrect, unreasonable, or infeasible: please let me know.  
