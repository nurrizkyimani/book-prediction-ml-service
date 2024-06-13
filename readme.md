# Book Prediction Machine Learning Service

This is a project that combine machine learning and microservice example using message queue with redis stream. the machine learning predicts books and send the data to redis. Consumer will consume the data and send it to database (firestore). The implementation of the message queue by consuming the data when the user trigger `/book_prediction`. It then send the data to the redis stream in the cloud. Then the consumer here `consumer.py` consume the redis stream, and send it to the database. Thinking as the second microservice. 

# Tech Stack 
- Fastapi
- Tensorflow
- Firestore
- Redis Stream 

# How to 

install requirement.txt
``` pip3 install requirement.txt```

run the main.py 
``` python3 main.py```

run consumer.py 
``` python3 consumer.py```

the result data send, is in the firebase
