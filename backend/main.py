from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib, string, re

from fastapi import FastAPI


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    text: str


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


def output_label(n):
    if n == 0:
        return 'Fake News'
    elif n == 1:
        return 'Not A Fake News'
    

@app.post('/predict')
def predict(item: Item):
    text = item.text

    LR = joblib.load('./algorithm/lr.joblib')
    DT = joblib.load('./algorithm/dt.joblib')
    GB = joblib.load('./algorithm/gb.joblib')
    RF = joblib.load('./algorithm/rf.joblib')
    vectorization = joblib.load('./algorithm/vectorization.joblib')

    text_cleaned = wordppt(text)
    new_x_test = [text_cleaned]
    new_xv_test = vectorization.transform(new_x_test)

    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GB = GB.predict(new_xv_test)
    pred_RF = RF.predict(new_xv_test)

    return {
        'LR': output_label(pred_LR[0]),
        'DT': output_label(pred_DT[0]),
        'GB': output_label(pred_GB[0]),
        'RF': output_label(pred_RF[0]),
    }
