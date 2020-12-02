from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


log_model = load('model.joblib') 


vectorizer = load('vectorizer.joblib') 

features = vectorizer.transform(
    ['No he visto el video, pero de seguro Jacobo va a decir otra de sus pendejadas sin fundamento jaja']
)
features_nd = features.toarray()


y_pred = log_model.predict(features)

print(y_pred)

