import pika
import traceback
import json

#Publisher client to rabbitmq broker
class Publisher:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        credentials = pika.PlainCredentials('root', 'phil.poc.ia')
        return pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq-service',
                                        5672,
                                        '/',
                                        credentials
                                    )
        )

    def publish(self, userdata):
        connection = None
        try:
            connection = self.create_connection()
            
            routing_key   = 'ml.engine.queue'
            channel = self.connection.channel()
            channel.queue_declare(queue=routing_key, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=routing_key,
                body=json.dumps(userdata),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise e
        finally:
            if connection:
                connection.close()