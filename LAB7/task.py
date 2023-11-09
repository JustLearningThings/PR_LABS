import pika, sys, time, threading

from scraper import Scraper
from worker import Worker
from database import Database

QUEUE_NAME = '999_task'

def start_worker(queue_name, worker_name):
    w = Worker(
        queue_name=queue_name,
        name=worker_name,
        db=db,)
    w.start()


def start_workers(num_workers):
    for i in range(num_workers):
        name = f'worker_{i + 1}'
        thread = threading.Thread(target=start_worker, args=(QUEUE_NAME, name))
        thread.start()

# connect and empty the database
db = Database()
db.empty()

# extract the number of threads from the flag
threads = 1
if len(sys.argv) > 1 and (sys.argv[1].lower() == '-threads' or sys.argv[1].lower() == '-t') and sys.argv[2].isnumeric():
    threads = int(sys.argv[2])

# extract URLs
s = Scraper()
urls = s.parse_from(
    url='https://999.md/ro/list/real-estate/apartments-and-rooms?o_30_241=893&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776',
    num_pages_to_scrape=1,
)
# urls = ['https://999.md/ro/82632782', 'https://999.md/ro/84501481', 'https://999.md/ro/64941772', 'https://999.md/ro/84521715', 'https://999.md/ro/79562870', 'https://999.md/ro/84459732', 'https://999.md/ro/84684219', 'https://999.md/ro/84909209']

print(f'Found {len(urls)} pages.')

if urls is None or urls == '' or len(urls) == 0:
    print('No URLs found')
    
    sys.exit(0)

# start workers
start_workers(num_workers=threads)

# distribute work
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(
    queue=QUEUE_NAME,
    durable=True    
)

for url in urls:
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=url,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )

print(f'Tasks distributed to {threads} workers.')

connection.close()