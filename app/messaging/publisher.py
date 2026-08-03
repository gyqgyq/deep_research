"""RabbitMQ 发布空壳 API。"""

from __future__ import annotations

import aio_pika

from app.messaging.client import get_channel


async def publish(
    queue_name: str,
    body: bytes | str,
    *,
    durable: bool = True,
) -> None:
    """声明队列并向默认 exchange 投递消息（调用方自行序列化 body）。"""
    channel = get_channel()
    queue = await channel.declare_queue(queue_name, durable=durable)
    payload = body if isinstance(body, bytes) else body.encode("utf-8")
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=payload,
            delivery_mode=(
                aio_pika.DeliveryMode.PERSISTENT
                if durable
                else aio_pika.DeliveryMode.NOT_PERSISTENT
            ),
        ),
        routing_key=queue.name,
    )
