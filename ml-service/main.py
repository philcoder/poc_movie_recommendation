#!/usr/bin/python3

import os
from multiprocessing import Process

import json

from app.client import Consumer
from app.engine import Engine

def main():
    cpu_count = os.cpu_count()
    processes = [Process(target=start_consumers) for x in range(cpu_count)]

    for proc in processes:
        proc.start()

    print("Created {} rabbitmq consumers".format(cpu_count))

    print(' [*] Waiting for messages. To exit press CTRL+C or kill process')
    #finish when all consumers die
    for proc in processes:
        proc.join()
    
    print("The all rabbitmq consumers is down")

def start_consumers():
    client = Consumer()   
    client.start_consuming(callback)

#for each consume use this callback
def callback(ch, method, properties, body):
    engine = Engine()
    engine.test(json.loads(body.decode()))


main()