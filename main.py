from fastapi import FastAPI
from flask import jsonify, request
import uvicorn
from random import seed
import random
import numpy as np
import pickle


app = FastAPI()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)

model_pick = pickle.load(open('model.pkl', 'rb'))


@app.get("/")
async def root():
    return {"message": "Empty root"}


@app.post("/salary_predict")
async def predict():
    data = request.get_json(force=true)
    prediction = model_pick.prediction([[np.array(data['exp'])]])
    output = prediction[0]
    return jsonify(output)


@app.get("/book_prediction")
def get_book_prediction():

    url_rating = './ratings.csv'
    url_books = './books.csv'

    rating = pd.read_csv(url_rating)

    books = pd.read_csv(url_books)

    book_data = np.array(list(set(rating.book_id)))
    user = np.array([100 for i in range(len(book_data))])
    model = keras.models.load_model('models')
    # model.summary()

    predictions = model.predict([[user], [book_data]])
    predictions = np.array([a[0] for a in predictions])
    recommended_book_ids = (-predictions).argsort()[:5]

    bb = books[books['id'].isin(recommended_book_ids)]

    bi = bb.to_dict('index')
    lit = []
    for key, value in bi.items():
        lit.append(value)

    return {
        "status": 200,
        "docs": lit
    }


@app.get()
