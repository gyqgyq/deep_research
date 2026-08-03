"""RabbitMQ 消费空壳 API。"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aio_pika.abc import AbstractIncomingMessage

from app.messaging.client import get_channel

MessageHandler = Callable[[AbstractIncomingMessage], Awaitable[Any]]


async def consume(
    queue_name: str,
    handler: MessageHandler,
    *,
    durable: bool = True,
    prefetch: int = 1,
) -> Any:
    """声明队列、设置 QoS 并注册消费者；不在 lifespan 中自动启动。

    返回 aio-pika 的 consumer tag / 消费句柄，由调用方决定生命周期。
    """
    channel = get_channel()
    await channel.set_qos(prefetch_count=prefetch)
    queue = await channel.declare_queue(queue_name, durable=durable)
    return await queue.consume(handler)
