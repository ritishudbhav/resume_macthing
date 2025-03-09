import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET_NAME

# AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def fetch_resume_from_s3(s3_key):
    """Fetch resume text from S3 based on key."""
    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        return obj["Body"].read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching resume from S3: {e}")
        return None
