from kafka import KafkaConsumer
import json

connected = False
while not connected:
    try:
        consumer = KafkaConsumer('viewed-items-topic', group_id='viewed_items', bootstrap_servers=['kafka:9092'])
        connected = True
    except:
        pass

for message in consumer:
    listing_data=(message.value).decode('utf-8')
    with open("logs.txt", "a") as log_file:
        log_file.write(listing_data)
