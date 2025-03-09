import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://your_username:your_password@cluster.mongodb.net/")
DATABASE_NAME = "job_matching"

# AWS S3
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Kafka
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = "resume_updates"

# AI Model API Key (Gemini)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
