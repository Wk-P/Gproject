import logging, json, os, sys, queue, threading
from kafka import KafkaProducer
def test_log_file_input():
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    log_file_name = "logs.log"
    logging.basicConfig(filename=log_file_name, filemode='a', format=log_format, level=logging.ERROR)
    logger = logging.getLogger()
    logger.error('hshshshsh')

def test_json_file_read(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        for item in data:
            print(item, "|", data[item])
            for elems in data[item]:
                print(elems)
                for elem in elems:
                    print(elem, "|", elems[elem])

def kafka_producer():
    # producer
    prodecuer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    # consumer
    # consumer = KafkaConsumer('quickstart-events', bootstrap_servers=['localhost:9092'])

    while True:
        msg = input("Enter : ")
        # msg = "Happy!\n"
        future = prodecuer.send('quickstart-events', bytes(msg.encode('utf-8')))
        result = future.get(timeout = 10)
        print(f"消息已发送，分区: {result.partition}, 偏移量: {result.offset}")
            # for message in consumer:
                # print(message.value)


if __name__ == "__main__":
    kafka_producer()