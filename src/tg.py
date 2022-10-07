from telethon.sync import TelegramClient, events
from .config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_CHAT_ID, WS_BROKER_HOST, WS_BROKER_QUEUE
import re
import logging
import pika
import json
from datetime import datetime

logger = logging.getLogger('tg-berezka')

def send_order_in_rabbitmq(order, now):
    connection = None
    try:
        logger.debug(f'Попытка отправить сообщение в Rabbitmq')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=WS_BROKER_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=WS_BROKER_QUEUE)
        logger.debug(f'Отправка сообщения (host -> {WS_BROKER_HOST}, queue -> {WS_BROKER_QUEUE}, message -> {order})')
        body = json.dumps({'transport':'telegram', 'order': order, 'date':str(now)})
        channel.basic_publish(exchange='',
                            routing_key=WS_BROKER_QUEUE,
                            body=body)
    except Exception as ex:
        logger.exception(ex)
        raise ex
    finally:
        if connection is not None:
            logger.debug(f'Закрываем соединение с Rabbitmq')
            connection.close()

def start_tg_client():
    with TelegramClient('berezka_bot', TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
        
        @client.on(events.NewMessage(chats=(int(TELEGRAM_CHAT_ID),)))
        async def handler(event):
            now = datetime.now()
            chat = await event.get_chat()
            sender = await event.get_sender()
            chat_id = event.chat_id
            sender_id = event.sender_id
            logger.debug(f'Получил сырое сообщение -> {event.raw_text}')
            r = re.search(r"\d{18}", event.raw_text)
            if  r: 
                logging.info(f'Опубликован новый конкурс -> {r[0]}')
                send_order_in_rabbitmq(r[0], now)

        client.run_until_disconnected()
