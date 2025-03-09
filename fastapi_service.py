from fastapi import FastAPI, HTTPException
from db import jobs_collection, students_collection
from s3_handler import fetch_resume_from_s3
from producer import send_resume_update

app = FastAPI()

@app.post("/upload_resume/{student_id}")
def upload_resume(student_id: str, s3_key: str):
    """Trigger resume matching when a student uploads a resume to S3."""
    resume_text = fetch_resume_from_s3(s3_key)
    if not resume_text:
        raise HTTPException(status_code=500, detail="Error fetching resume from S3.")

    # Update student record
    students_collection.update_one(
        {"student_id": student_id},
        {"$set": {"resume_text": resume_text, "s3_key": s3_key}},
        upsert=True
    )

    # Send Kafka event
    send_resume_update(student_id, resume_text)

    return {"message": "Resume uploaded and matching started."}

@app.get("/top_jobs/{student_id}")
def get_top_jobs(student_id: str):
    """Retrieve top 5 job matches for a student."""
    jobs = list(jobs_collection.find({f"matches.{student_id}": {"$exists": True}}))

    # Sort by match percentage
    sorted_jobs = sorted(jobs, key=lambda job: job["matches"].get(student_id, 0), reverse=True)

    # Get top 5 jobs
    top_jobs = [
        {"job_id": str(job["_id"]), "text": job["text"], "match_percentage": job["matches"][student_id]}
        for job in sorted_jobs[:5]
    ]

    return {"student_id": student_id, "top_jobs": top_jobs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
