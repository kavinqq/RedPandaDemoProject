from django.urls import path
from redpanda.views import DemoProducerView, DemoConsumerView

urlpatterns = [
    path('demo-producer/', DemoProducerView.as_view(), name='demo-producer'),
    path('demo-consumer/', DemoConsumerView.as_view(), name='demo-consumer'),
]