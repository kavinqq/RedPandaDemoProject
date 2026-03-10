import json

from django.conf import settings
from django.core.management.base import BaseCommand
from confluent_kafka import Consumer


class Command(BaseCommand):
    help = '持續消費 RedPanda topic 的 messages（Ctrl+C 停止）'

    def handle(self, *args, **options):
        consumer = Consumer({
            'bootstrap.servers': f'{settings.REDPANDA_HOST}:{settings.REDPANDA_PORT}',
            'group.id': 'demo-consumer',
            'auto.offset.reset': 'earliest',
        })

        consumer.subscribe([settings.REDPANDA_POCKETFAN_NAMELIST_TOPIC])

        self.stdout.write(self.style.SUCCESS(
            f'Listening on topic: {settings.REDPANDA_POCKETFAN_NAMELIST_TOPIC} ... (Ctrl+C to stop)'
        ))

        try:
            while True:
                msg = consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    self.stderr.write(self.style.ERROR(f'Consumer error: {msg.error()}'))
                    continue

                data = json.loads(msg.value().decode('utf-8'))
                self.stdout.write(f'Received: {data}')
                consumer.commit()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nShutting down...'))
        finally:
            consumer.close()
            self.stdout.write(self.style.SUCCESS('Consumer closed.'))
