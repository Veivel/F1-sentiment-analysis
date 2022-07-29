import pandas as pd
import numpy as np

from sklearn import feature_extraction, model_selection, metrics
from sklearn.model_selection import train_test_split
from sklearn import naive_bayes, ensemble, tree

import xgboost

classifiers = {
    'xgb': xgboost.XGBClassifier(),
    'gaussian_nb': naive_bayes.GaussianNB(),
    'multi_nb': naive_bayes.MultinomialNB(),
    'rforest': ensemble.RandomForestClassifier(),
    'entropy_rforest': ensemble.RandomForestClassifier(criterion='entropy'),
    'decision_tree': tree.DecisionTreeClassifier()
    }    

class sklearn_model:
    """A basic SK-learn classifier model made for sentiment analysis. 
    Init args: (array of texts, array of target)"""
    
    def __init__(self, text, y):
        self.cv = feature_extraction.text.CountVectorizer()
        self.x = self.cv.fit_transform(text).toarray()
        self.y = y
    
    def evaluate_models(self, dict_classifiers=None):
        """Run through dict_classifiers to evaluate scores by 5-fold cross validation."""
        if dict_classifiers == None:
            dict_classifiers = classifiers
        str = ""
        for name in dict_classifiers:
            clf = dict_classifiers[name]
            scores = scores = model_selection.cross_val_score(clf, self.x, self.y, cv=5)
            score = np.average(scores)
            str += f"Score of {name}: {score}\n"
        return str
    
    def __train(self, clf):
        clf.fit(self.x, self.y)
        return "Classifier fit success."
    
    def train(self, classifier):
        """Train (fit) the chosen classifier.
        clf can take: a string (according to the dict), or an object of sk-learn classifier model"""
        if isinstance(classifier, str):
            self.clf = classifiers[classifier]
        else:
            self.clf = classifier
            self.__train(classifier)
    
    def predict(self, x):
        """Predict the target variable of x.
        x must be in bag of words (CV fit-transformed) model."""
        self.x_test = x
        self.y_pred = self.clf.predict(self.x_test)
        
        return self.y_pred
    
# make room for bert model!