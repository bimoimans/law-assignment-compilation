"""Notification channels for django-notifs."""

from json import dumps

import pika

from notifications.channels import BaseNotificationChannel
from pika.spec import Queue


class BroadCastWebSocketChannel(BaseNotificationChannel):
    """Fanout notification channel with RabbitMQ."""

    def _connect(self):
        """Connect to the RabbitMQ server."""
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()

        return connection, channel

    def construct_message(self):
        """Construct the message to be sent."""
        extra_data = self.notification_kwargs['extra_data']

        return dumps(extra_data['message'])

    def notify(self, message):
        """put the message of the RabbitMQ queue."""
        connection, channel = self._connect()
        uri = self.notification_kwargs['extra_data']['uri']
        print("im trying to send something")
        channel.queue_declare(queue=uri)
        channel.exchange_declare(exchange=uri, exchange_type='fanout')
        channel.queue_bind(exchange=uri, queue=uri)
        #TODO Set routing key bind dll
        channel.basic_publish(exchange=uri, routing_key='', body=message)
        channel.queue_unbind(exchange=uri, queue=uri)

        connection.close()
        