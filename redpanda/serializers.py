from rest_framework import serializers


class DemoProducerSerializer(serializers.Serializer):
    messages = serializers.ListField(child=serializers.JSONField())
