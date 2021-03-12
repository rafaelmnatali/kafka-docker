from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

# Create 'my-topic' Kafka topic
try:
        admin = KafkaAdminClient(bootstrap_servers='kafka-1:19093,kafka-2:29093,kafka-3:39093')

        topic = NewTopic(name='demo-multi-partition-key',
                         num_partitions=3,
                         replication_factor=3)
        admin.create_topics([topic])
except Exception:
        pass

producer = KafkaProducer(bootstrap_servers='kafka-1:19093,kafka-2:29093,kafka-3:39093')

for i in range(10):
  print(i)
  if i % 2 == 0:
      producer.send("demo-multi-partition-key", key=b'even', value=b'number %d is even' % i)
  else:
      producer.send("demo-multi-partition-key", b'msg %d' % i)

producer.close()