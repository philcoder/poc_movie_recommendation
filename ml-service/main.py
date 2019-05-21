#!/usr/bin/python3

import json

from app.client import Consumer
from app.engine import Engine

def main():
    client = Consumer()
    client.start_consuming(callback)

#for each consume use this callback
def callback(ch, method, properties, body):
    engine = Engine()
    engine.test(json.loads(body.decode()))


main()