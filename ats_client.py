# ats_client.py
import uuid
import json
import os

DB_FILE = "mock_db.json"

# ---------------------------------
# Mock ATS Job Data
# ---------------------------------
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
    },
    {
        "id": "job_3",
        "title": "Data Analyst",
        "location": "Hyderabad",
        "status": "DRAFT",
        "external_url": "https://example.com/jobs/3"
    }
]

# ---------------------------------
# Internal DB Helpers
# ---------------------------------
def _load_db():
    if not os.path.exists(DB_FILE):
        return {"applications": []}

    with open(DB_FILE, "r") as f:
        return json.load(f)


def _save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------
# GET JOBS (ATS + PAGINATION)
# ---------------------------------
def get_jobs(page=1, limit=10):
    """
    Fetch jobs from ATS with basic pagination support.
    """

    try:
        page = int(page)
        limit = int(limit)

        if page < 1 or limit < 1:
            raise ValueError("page and limit must be positive integers")

        start = (page - 1) * limit
        end = start + limit

        paginated_jobs = JOBS[start:end]

        return {
            "results": paginated_jobs,
            "page": page,
            "limit": limit,
            "has_more": end < len(JOBS)
        }

    except Exception as e:
        raise Exception(f"ATS job fetch failed: {str(e)}")


# ---------------------------------
# CREATE CANDIDATE (ATS)
# ---------------------------------
def create_candidate(candidate_data):
    try:
        return {
            "id": str(uuid.uuid4()),
            "name": candidate_data["name"],
            "email": candidate_data["email"],
            "phone": candidate_data["phone"],
            "resume_url": candidate_data["resume_url"]
        }

    except KeyError as e:
        raise Exception(f"Missing candidate field: {str(e)}")


# ---------------------------------
# APPLY CANDIDATE TO JOB
# ---------------------------------
def apply_candidate(job_id, candidate):
    try:
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

    except Exception as e:
        raise Exception(f"Failed to apply candidate: {str(e)}")


# ---------------------------------
# GET APPLICATIONS BY JOB
# ---------------------------------
def get_applications(job_id):
    try:
        db = _load_db()
        return [a for a in db["applications"] if a["job_id"] == job_id]

    except Exception as e:
        raise Exception(f"Failed to fetch applications: {str(e)}")
