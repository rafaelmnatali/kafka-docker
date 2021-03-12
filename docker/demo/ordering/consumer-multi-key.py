from kafka import KafkaConsumer
consumer = KafkaConsumer(bootstrap_servers='kafka-1:19093,kafka-2:29093,kafka-3:39093',
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=10000)
consumer.subscribe(['demo-multi-partition-key'])

for msg in consumer:
    if msg.key == b'even':
        print ("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
                                          msg.offset, msg.key,
                                          msg.value))

consumer.close()