import asyncio
from aiokafka import AIOKafkaConsumer
import json

async def consume_notifications():
    consumer = AIOKafkaConsumer(
        "voter_notifications",
        bootstrap_servers='localhost:9092',
        group_id="notification_group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    # Start the consumer
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received notification: {msg.value}")
            # Logic to send SMS/Email/Push
            # await send_email(msg.value['email'], msg.value['subject'], msg.value['body'])
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_notifications())
