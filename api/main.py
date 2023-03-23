from __future__ import unicode_literals, print_function
from fastapi import FastAPI
import spacy
import joblib
from mangum import Mangum
from flair.data import Sentence
from flair.models import TextClassifier

app = FastAPI()

nlp_custom = joblib.load("sureter_ner.pkl")
nlp_NER = spacy.load("en_core_web_lg")
classifier = TextClassifier.load('en-sentiment')
# python -m spacy download en
# uvicorn main:app --reload


@app.get("/pre_process_query/")
async def pre_process_query(text: str):
    doc = nlp_custom(text)
    nlp_custom_entities = [(ent.text, ent.label_) for ent in doc.ents]
    output = extract_query_sentiment(nlp_custom_entities)
    doc = nlp_NER(text)
    nlp_ner_entities = [(ent.text, ent.label_) for ent in doc.ents]
    for word, tag in nlp_ner_entities:
        if tag == 'ORG' or tag == 'LOC':
            output.append({"review_type": "Restaurant_name", "text": word, "sentiment_text": "",
                           "sentiment": ""})
    return output

handler = Mangum(app=app)

def get_word_sentiment(word):
    sentence = Sentence(word)
    classifier.predict(sentence)
    output = sentence.labels[0].value
    return output


def extract_query_sentiment(arr):
    review = []
    i = 0
    while i < len(arr):
        if arr[i][1] == 'VAL' or arr[i][1] == 'REC':
            entity_sentiment = get_word_sentiment(arr[i][0])
            review.append({"review_type": arr[i][1], "text": arr[i][0], "sentiment_text": "",
                           "sentiment": entity_sentiment})
            del arr[i]
        elif arr[i][1] != 'SEN':
            if i > 0 and arr[i - 1][1] == 'SEN':
                entity_sentiment = get_word_sentiment(arr[i - 1][0])
                review.append({"review_type": arr[i][1], "text": arr[i][0], "sentiment_text": arr[i - 1][0],
                               "sentiment": entity_sentiment})
                del arr[i - 1:i + 1]
            else:
                review.append(
                    {"review_type": arr[i][1], "text": arr[i][0], "sentiment_text": "", "sentiment": ""})
                del arr[i]
        else:
            i += 1
    return review
