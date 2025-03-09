from kafka import KafkaConsumer
import json
from db import jobs_collection, students_collection
from ai_matcher import get_match_percentage
from config import KAFKA_BROKER, KAFKA_TOPIC

# Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    group_id="job-matching",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

def process_resume_updates():
    """Consume Kafka messages and perform job matching."""
    for message in consumer:
        data = message.value
        student_id = data["student_id"]
        resume_text = data["resume_text"]

        print(f"Processing resume for student: {student_id}")

        # Fetch all jobs
        jobs = list(jobs_collection.find())

        for job in jobs:
            job_id = job["_id"]
            job_text = job.get("text")

            if not job_text:
                continue

            # Check if match score already exists
            existing_match = jobs_collection.find_one(
                {"_id": job_id, f"matches.{student_id}": {"$exists": True}}
            )
            if existing_match:
                continue  # Skip if already matched

            # Get match percentage
            match_percentage = get_match_percentage(resume_text, job_text)

            # Store match percentage in jobs collection
            jobs_collection.update_one(
                {"_id": job_id},
                {"$set": {f"matches.{student_id}": match_percentage}}
            )

        print(f"Matching completed for student: {student_id}")

if __name__ == "__main__":
    process_resume_updates()
