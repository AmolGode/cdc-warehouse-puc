import os
import json
from confluent_kafka import Consumer

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from warehouse.upserts import handle_event  # we'll define this next

TOPICS = [
    "source.public.orders_city",
    "source.public.orders_distributor",
    "source.public.orders_order",
]

def run():
    consumer = Consumer({
        "bootstrap.servers": "kafka:9092",
        "group.id": "warehouse-sink",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(TOPICS)

    print("Consumer started, listening on:", TOPICS)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error:", msg.error())
                continue

            event = json.loads(msg.value())
            handle_event(msg.topic(), event)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()