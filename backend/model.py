# main.py# %%
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import re
import string

# %%
data_fake = pd.read_csv('./algorithm/content/Fake.csv')
data_true = pd.read_csv('./algorithm/content/True.csv')

# %%
data_fake.head()

# %%
data_true.head()

# %%
data_fake['class'] = 0
data_true['class'] = 1

# %%
data_fake.shape, data_true.shape

# %%
data_fake_manual_testing = data_fake.tail(10)

# Data cleansing
for i in range(23480, 23470, -1):
    data_fake.drop([i], axis = 0, inplace = True)

data_true_manual_testing = data_true.tail(10)
for i in range(21416, 21406, -1):
    data_fake.drop([i], axis = 0, inplace = True)

# %%
data_fake.shape, data_true.shape

# %%
data_fake_manual_testing['class'] = 0
data_true_manual_testing['class'] = 0

# %%
data_fake_manual_testing.head(10)

# %%
data_true_manual_testing.head(10)

# %%
# merge data fake and real
data_merge = pd.concat([data_fake, data_true], axis = 0)
data_merge.head(10)

# %%
data_merge.columns

# %%
data = data_merge.drop(['title', 'subject', 'date'], axis = 1)

# %%
data.isnull().sum()


# %%
data = data.sample(frac = 1)

# %%
data.head()

# %%
data.reset_index(inplace = True)
data.drop(['index'], axis = 1, inplace = True)

# %%
data.columns

# %%
data.head()

# %%
# Remove unrequired chars and words such as links, blank space, etc.
def wordppt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

# %%
data['text'] = data['text'].apply(wordppt)

# %%
x = data['text']
y = data['class']

# %%
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25)

# %%
from sklearn.feature_extraction.text import TfidfVectorizer

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)

# %%
# Implementing Logistic Regression

# from sklearn.linear_model import LogisticRegression

# LR = LogisticRegression()
# # Train the model
# LR.fit(xv_train, y_train)

# # %%
# # Predicting the data
# pred_lr = LR.predict(xv_test)

# # %%
# # Checking the accuracy
# LR.score(xv_test, y_test)

# # %%
# print(classification_report(y_test, pred_lr))

# # %%
# # Implementing Decision Tree Classifier

# from sklearn.tree import DecisionTreeClassifier

# DT = DecisionTreeClassifier()

# # Train the model
# DT.fit(xv_train, y_train)

# # %%
# pred_dt = DT.predict(xv_test)

# # %%
# DT.score(xv_test, y_test)

# # %%
# print(classification_report(y_test, pred_dt))

# # %%
# from sklearn.ensemble import GradientBoostingClassifier

# GB = GradientBoostingClassifier(random_state=0)

# GB.fit(xv_train, y_train)

# # %%
# pred_gb = GB.predict(xv_test)

# # %%
# GB.score(xv_test, y_test)

# # %%
# print(classification_report(y_test, pred_gb))

# # %%
# from sklearn.ensemble import RandomForestClassifier

# RF = RandomForestClassifier(random_state=0)
# RF.fit(xv_train, y_train)

# # %%
# pred_rf = RF.predict(xv_test)

# # %%
# RF.score(xv_test, y_test)

# # %%
# print(classification_report(y_test, pred_rf))

import joblib
LR = joblib.load('./algorithm/lr.joblib')
DT = joblib.load('./algorithm/dt.joblib')
GB = joblib.load('./algorithm/gb.joblib')
RF = joblib.load('./algorithm/rf.joblib')

# %%
def output_label(n):
    if n == 0:
        return 'Fake News'
    elif n == 1:
        return 'Not A Fake News'

def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordppt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GB = GB.predict(new_xv_test)
    pred_RF = RF.predict(new_xv_test)

    return print("\n\nLR Prediction: {} \nDT Prediction: {} \nGB Prediction: {} \nRF Prediction: {}".format(output_label(pred_LR[0]), output_label(pred_DT[0]), output_label(pred_GB[0]), output_label(pred_RF[0])))

# %%
# news = str(input('Enter the news'))
# manual_testing(news)

# %%
# import joblib

# joblib.dump(LR, "lr.joblib")
# joblib.dump(DT, "dt.joblib")
# joblib.dump(GB, "gb.joblib")
# joblib.dump(RF, "rf.joblib")

# %%



