from django.core.management.base import BaseCommand
from warehouse.consumer import run


class Command(BaseCommand):
    help = "Runs the Kafka consumer that syncs CDC events into the warehouse."

    def handle(self, *args, **options):
        run()