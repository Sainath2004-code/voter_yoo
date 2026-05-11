from aiokafka import AIOKafkaProducer
import json
import asyncio
import os

class AuditProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_SERVERS", "localhost:9092")
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def log_event(self, event_type: str, actor_id: str, data: dict):
        if not self.producer:
            await self.start()
        
        event = {
            "event_type": event_type,
            "actor_id": actor_id,
            "data": data,
            "service": "auth-service"
        }
        await self.producer.send_and_wait("voter_audit_logs", event)

audit_producer = AuditProducer()
