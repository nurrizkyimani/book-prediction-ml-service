from fastapi import FastAPI
import uvicorn
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from redis_om import get_redis_connection
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080'],
    allow_methods=['*'],
    allow_headers=['*']
)


redis = get_redis_connection(
    host="redis-16079.c299.asia-northeast1-1.gce.cloud.redislabs.com",
    port=16079,
    password="9E4RzDu2edr8QdyFOH8aSWaBrVl5hCSi",
    decode_responses=True
)

key = 'test_union'
group = 'inventory-group'


@app.get("/")
async def root():
    return {"message": "This is empty root"}

example_dict = {'name': 'ricky', 'age': 12}


@app.get("/random_streamline")
async def streaming_prediction_to_database():
    results = redis.xreadgroup(group, key, {key: '>'}, None)
    print(results)
    return {"message": "send a data to redis pipeline :)"}


@app.get("/book_prediction")
async def get_book_prediction():

    url_rating = './ratings.csv'
    url_books = './books.csv'

    rating = pd.read_csv(url_rating)
    books = pd.read_csv(url_books)

    book_data = np.array(list(set(rating.book_id)))
    user = np.array([101 for i in range(len(book_data))])
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

    redis.xadd("test_union", lit[0], "*")

    return {
        "status": 200,
        "docs": lit
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
