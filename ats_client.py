# ats_client.py
import uuid
import json
import os

DB_FILE = "mock_db.json"

JOBS = [
    {
        "id": "job_1",
        "title": "Software Engineer",
        "location": "Remote",
        "status": "OPEN",
        "external_url": "https://example.com/jobs/1"
    },
    {
        "id": "job_2",
        "title": "Backend Developer",
        "location": "Bangalore",
        "status": "OPEN",
        "external_url": "https://example.com/jobs/2"
    }
]


def _load_db():
    if not os.path.exists(DB_FILE):
        return {"applications": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def _save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)


def get_jobs():
    return JOBS


def create_candidate(candidate_data):
    return {
        "id": str(uuid.uuid4()),
        "name": candidate_data["name"],
        "email": candidate_data["email"],
        "phone": candidate_data["phone"],
        "resume_url": candidate_data["resume_url"]
    }


def apply_candidate(job_id, candidate):
    db = _load_db()

    application = {
        "id": str(uuid.uuid4()),
        "job_id": job_id,
        "candidate_name": candidate["name"],
        "email": candidate["email"],
        "status": "APPLIED"
    }

    db["applications"].append(application)
    _save_db(db)

    return application


def get_applications(job_id):
    db = _load_db()
    return [a for a in db["applications"] if a["job_id"] == job_id]
