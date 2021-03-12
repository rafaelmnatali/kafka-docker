from kafka import KafkaConsumer
consumer = KafkaConsumer(bootstrap_servers='kafka-1:19093,kafka-2:29093,kafka-3:39093',
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=10000)
consumer.subscribe(['demo-single-partition'])

for msg in consumer:
    print ("%s:%d:%d: value=%s" % (msg.topic, msg.partition,
                                    msg.offset, msg.value))

consumer.close()