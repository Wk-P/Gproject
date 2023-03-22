from kafka import KafkaConsumer
from kafka import TopicPartition
import time

def kafka_consumer():
    consumer = KafkaConsumer('quickstart-events', bootstrap_servers=['localhost:9092'], 
                             auto_offset_reset='latest')
    print("接受信息...")
    # print(consumer.subscription())
    # while True:
    
    # while True:
    for msg in consumer:
        print(msg.value.decode(encoding='utf-8'))

if __name__ == "__main__":
    kafka_consumer()