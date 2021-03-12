from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

# Create 'my-topic' Kafka topic
try:
        admin = KafkaAdminClient(bootstrap_servers='kafka-1:19093,kafka-2:29093,kafka-3:39093')

        topic = NewTopic(name='demo-single-partition',
                         num_partitions=1,
                         replication_factor=1)
        admin.create_topics([topic])
except Exception:
        pass

producer = KafkaProducer(bootstrap_servers='kafka-1:19093,kafka-2:29093,kafka-3:39093')

for i in range(10):
  print(i)
  producer.send("demo-single-partition", b'msg %d' % i)

producer.close()