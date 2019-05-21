import pika
import traceback

#Publisher client to rabbitmq broker
class Consumer:

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
    
    def start_consuming(self, method_callback):
        connection = None
        try:
            connection = self.create_connection()
            
            routing_key   = 'ml.engine.queue'
            channel = connection.channel()
            channel.queue_declare(queue=routing_key, durable=True)
            channel.basic_consume(
                queue=routing_key, on_message_callback=method_callback, auto_ack=True
            )

            channel.start_consuming()
            print(' [*] Waiting for messages. To exit press CTRL+C or kill process')
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise e
        finally:
            if connection:
                connection.close()