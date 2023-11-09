import pika, sys, os, time, threading
from scraper import Scraper

class Worker:
    def __init__(self, queue_name, name, db):
        self.queue_name = queue_name
        self.name = name
        self.db = db

    def start(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            channel.queue_declare(queue=self.queue_name, durable=True)

            def callback(ch, method, properties, body):
                url = body.decode()
                print(f'Received URL: {url}')

                ch.basic_ack(
                    delivery_tag=method.delivery_tag
                )

                s = Scraper()
                parsed_data = s.parse_page(url)
                
                self.db.insert(parsed_data)
                # print(parsed_data)

                print('Done.')

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=callback
            )

            print(f' [{self.name}] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except KeyboardInterrupt:
            print(f'Interrupted at {self.name}')

            sys.exit(0)
        


# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted.')

#         try:
#             sys.exit(0)
#         except SystemExit:
#             sys.exit(0)