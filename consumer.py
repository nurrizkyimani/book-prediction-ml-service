from main import redis
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


key = 'test_union'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                print(obj)

                data = {
                    u'id': obj['id'],
                    u'original_title': obj['original_title'],
                    u'authors': obj['authors'],
                    u'average_rating': obj['average_rating'],
                    u'ratings_count': obj['ratings_count'],
                    u'image_url': obj['image_url'],
                    u'isbn': obj['isbn'],
                }

                # Add a new doc in collection 'cities' with ID 'LA'
                db.collection(u'books').document(u'first').set(data)

    except Exception as e:
        print(str(e))
    time.sleep(1)
