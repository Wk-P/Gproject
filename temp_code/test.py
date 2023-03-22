import logging, json, os
from kafka import KafkaProducer, KafkaConsumer

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

def kafka_test():
    # producer
    prodecuer = KafkaProducer(bootstrap_servers=["localhost:9092"], debug=True)
    # consumer
    consumer = KafkaConsumer('test_topic', bootstrap_servers=['localhost:9092'], debug=True)

    prodecuer.send('test_topic', b'Hello kafka in python')

    for message in consumer:
        print(message.value)

if __name__ == "__main__":
    # test_log_file_input()
    # test_json_file_read('./exchange/webexchange/views/verify_res_json/test.json')