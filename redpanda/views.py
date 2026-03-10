import json
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from confluent_kafka import Producer
from confluent_kafka import Consumer

from redpanda.serializers import DemoProducerSerializer


class DemoProducerView(GenericAPIView):
    serializer_class = DemoProducerSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        messages = serializer.validated_data.get('messages')
        delivery_errors = []

        producer = Producer({
            'bootstrap.servers': f'{settings.REDPANDA_HOST}:{settings.REDPANDA_PORT}',
        })

        for data in messages:
            producer.produce(
                settings.REDPANDA_POCKETFAN_NAMELIST_TOPIC,
                json.dumps(data).encode('utf-8'),
                callback=lambda err, msg, errors=delivery_errors: self._delivery_report(err, msg, errors),
            )

        producer.flush()

        if delivery_errors:
            return Response(
                {
                    'detail': 'Message delivery failed (broker may be unreachable).',
                    'errors': [str(e) for e in delivery_errors],
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delivery_report(self, err, msg, errors):
        """Called once per produced message. Appends any error to errors list."""
        if err is not None:
            errors.append(err)
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
            
            
class DemoConsumerView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request, *args, **kwargs) -> Response:

        consumer = Consumer({
            'bootstrap.servers': f'{settings.REDPANDA_HOST}:{settings.REDPANDA_PORT}',
            'group.id': 'demo-consumer',
            'auto.offset.reset': 'earliest',
        })

        consumer.subscribe([settings.REDPANDA_POCKETFAN_NAMELIST_TOPIC])

        collected = []
        none_count, max_none_count = 0, 3

        try:
            while True:
                msg = consumer.poll(1.0)

                if msg is None:
                    none_count += 1
                    if none_count >= max_none_count:
                        break
                    continue

                if msg.error():
                    print(f'Consumer error: {msg.error()}')
                    continue

                none_count = 0
                collected.append(json.loads(msg.value().decode('utf-8')))
                consumer.commit()
        finally:
            consumer.close()

        result = {
            "code": 0,
            "msg": "從Redpanda取得資料成功",
            "data": collected,
        }

        return Response(result, status=status.HTTP_200_OK)
            