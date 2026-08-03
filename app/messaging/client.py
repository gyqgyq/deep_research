"""RabbitMQ 连接与 channel 生命周期。"""

from __future__ import annotations

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

from app.core.settings import settings

_connection: AbstractRobustConnection | None = None
_channel: AbstractChannel | None = None


async def connect() -> None:
    """建立到 RabbitMQ 的稳健连接并打开 channel。"""
    global _connection, _channel
    if _connection is not None and not _connection.is_closed:
        return
    _connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    _channel = await _connection.channel()


async def disconnect() -> None:
    """关闭 channel 与连接。"""
    global _connection, _channel
    if _channel is not None and not _channel.is_closed:
        await _channel.close()
    _channel = None
    if _connection is not None and not _connection.is_closed:
        await _connection.close()
    _connection = None


async def ping() -> None:
    """探测连接是否可用；未连接则先 connect。"""
    await connect()
    if _connection is None or _connection.is_closed:
        raise RuntimeError("RabbitMQ 连接不可用")
    if _channel is None or _channel.is_closed:
        raise RuntimeError("RabbitMQ channel 不可用")


def get_channel() -> AbstractChannel:
    """返回当前 channel；未初始化则抛错。"""
    if _channel is None or _channel.is_closed:
        raise RuntimeError("RabbitMQ channel 未就绪，请先调用 connect()")
    return _channel
