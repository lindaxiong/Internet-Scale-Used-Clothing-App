from elasticsearch import Elasticsearch 
from kafka import KafkaConsumer


#indexing script to read messages from kafka and add them to elasticsearch
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'], api_version='0.9')
es = Elasticsearch(['es'])

#loop to listen for kafka messages
for message in consumer:
	some_new_listing=json.loads((message.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
	es.indices.refresh(index="listing_index")

		

