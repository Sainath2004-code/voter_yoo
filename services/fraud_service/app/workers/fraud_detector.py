import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_registration(event_data):
    """
    Simulate AI-powered fraud detection logic.
    - Check for duplicate national IDs
    - Analyze biometric confidence scores
    - Geo-location anomaly detection
    """
    voter_id = event_data.get("voter_id")
    logger.info(f"Analyzing voter registration for fraud: {voter_id}")
    
    # Simulation: Risk scoring logic
    risk_score = 0.15 # Low risk default
    
    # Check for biometric duplicates (simulation)
    # if await face_service.find_duplicates(voter_id):
    #    risk_score += 0.8
    
    is_fraud = risk_score > 0.7
    
    return {
        "voter_id": voter_id,
        "is_fraud": is_fraud,
        "risk_score": risk_score,
        "flags": ["biometric_match_ok", "location_verified"] if not is_fraud else ["duplicate_identity_detected"]
    }

async def run_fraud_detector():
    consumer = AIOKafkaConsumer(
        "voter_registration_events",
        bootstrap_servers='localhost:9092',
        group_id="fraud_detection_group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    await consumer.start()
    await producer.start()
    
    logger.info("Fraud Detection Worker started...")
    
    try:
        async for msg in consumer:
            logger.info(f"Processing event: {msg.key}")
            result = await process_registration(msg.value)
            
            # Send results to alerts topic
            if result["is_fraud"]:
                await producer.send_and_wait("fraud_alerts", result)
                logger.warning(f"FRAUD DETECTED for voter {result['voter_id']}")
            else:
                await producer.send_and_wait("verification_results", result)
                logger.info(f"Voter {result['voter_id']} passed initial fraud check")
                
    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(run_fraud_detector())
