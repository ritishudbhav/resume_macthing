from kafka import KafkaProducer
import json
from config import KAFKA_BROKER, KAFKA_TOPIC

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_resume_update(student_id, resume_text):
    """Send resume update to Kafka for processing."""
    producer.send(KAFKA_TOPIC, {"student_id": student_id, "resume_text": resume_text})
    print(f"Sent resume update for student: {student_id}")

if __name__ == "__main__":
    # Test the producer
    send_resume_update("12345", "Sample resume text for AI matching.")
