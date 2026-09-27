import random
import time
import uuid

from django.core.management.base import BaseCommand

from orders.models import City, Distributor, Order

SAMPLE_DISTRIBUTORS = [
    ("Acme Distribution", "ACM"),
    ("Global Traders", "GLT"),
    ("Northstar Supply", "NST"),
]

SAMPLE_CITIES = [
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Bengaluru", "Karnataka"),
]


class Command(BaseCommand):
    help = "Inserts one dummy Order per second for 20 seconds."

    def handle(self, *args, **options):
        for name, code in SAMPLE_DISTRIBUTORS:
            Distributor.objects.get_or_create(code=code, defaults={"name": name})

        for name, state in SAMPLE_CITIES:
            City.objects.get_or_create(name=name, defaults={"state": state})

        distributors = list(Distributor.objects.all())
        cities = list(City.objects.all())

        self.stdout.write("Generating dummy orders: 1 record/sec for 20 seconds...")

        for i in range(20):
            order = Order.objects.create(
                customer_id=f"cust-{uuid.uuid4().hex[:8]}",
                distributor=random.choice(distributors),
                city=random.choice(cities),
                amount=round(random.uniform(10, 1000), 2),
                status=random.choice([c[0] for c in Order.STATUS_CHOICES]),
            )
            self.stdout.write(f"[{i + 1}/20] Created Order id={order.id}")
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Done: inserted 20 dummy orders."))
