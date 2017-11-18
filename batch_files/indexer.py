import json
import os
import sched
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def update_indices(sc):
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    for message in consumer:
        some_new_listing = json.loads(message.value.decode('utf-8'))
        if some_new_listing:
            if 'password' in some_new_listing['fields']:
                some_new_listing['fields'].pop('password', None) # Linda was the one who did the extra credit Have multiple topics/indexes in Kafka/elasticsearch for more fine-tune search/indexing functionality. (+3 points)
            if some_new_listing['model'] == 'uc.user':
                es.index(index='main_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
                es.index(index='user_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
            if some_new_listing['model'] == 'uc.item':
                es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
                es.index(index='main_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
    es.indices.refresh(index='listing_index')
    es.indices.refresh(index='main_index')
    es.indices.refresh(index='user_index')
    sch.enter(20, 1, update_indices, (sc,))


# indexing script to read messages from kafka and add them to elasticsearch
if __name__ == '__main__':
    connected = False
    while not connected:
        try:
            consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
            es = Elasticsearch([{'host': 'es', 'port': 9200}])
            connected = True
        except:
            pass
    print('Loading batcher...')
    sch = sched.scheduler(time.time, time.sleep)
    db = {}
    with open('db.json') as f:
        db = json.load(f)
    for some_new_listing in db:
        if 'password' in some_new_listing['fields']:
            some_new_listing['fields'].pop('password', None)
        if some_new_listing['model'] == 'uc.user':
            es.index(index='main_index', doc_type='listing', id=some_new_listing['pk'], body=some_new_listing)
            es.index(index='user_index', doc_type='listing', id=some_new_listing['pk'], body=some_new_listing)
        if some_new_listing['model'] == 'uc.item':
            es.index(index='listing_index', doc_type='listing', id=some_new_listing['pk'], body=some_new_listing)
            es.index(index='main_index', doc_type='listing', id=some_new_listing['pk'], body=some_new_listing)
    es.indices.refresh(index='listing_index')
    es.indices.refresh(index='main_index')
    es.indices.refresh(index='user_index')
    sch.enter(20, 1, update_indices, (sch,))
    sch.run()
