# ResumeCV-Classifier-XGBoost

This is my first REPO-POC, welcome. It's an API running a XGBoost model for Resumes/CV classification.
For this POC, I have created a model to classify resumes from 5 distinct areas (Administration/Bussiness, Legal, Sales, Accounting/Finance and Investment).
There are not much real resumes dataset, and all of this project was done by using 500 resumes.

## POC WORKFLOW
Thinking about who have to find on databases or have just scanned tons of resumes/CV. Let's classify all your data, and as bonus, see how it fits in some jobs requeriments.
  - First: Acess http://52.87.98.116/, it is running on cheapest AWS cloud machine. A lightsail 512RAM, 1vCPU.
  - Then, upload a Administration/Bussiness, Legal, Sales, Accounting/Finance or Investment resume/CV.
  - Wait few minutes, and check what is your resume Area and Job Fitting result based on the job proposals listed @ homepage.


### MODEL
The model is all explained at /resumeCV_classifier.ipynb. Using Tensorflow, keras, XGboost, NLTK and spacy.

### API
This is running using Flask's framework, even FastAPI is widely used for AI APIs, I think for this POC it will not receive much requests.

### JOB PROPOSAL FITTING(EXTRA)
I have choose to not use ML or DL models, but use tokens and vectors and some techniques by my own. Here I am using TF-idf for text clustering, and Cosine Similarity, to compare jobs requirements from its resume texts.
To clarify, here I am taking the verbs, and getting its synonymous, and also looking for this words. That's why it takes few minutes to run. To make it faster and better, the word vectores are all sized based on ther requeriments sentence size.
