import os
import uuid
import requests
from zoho_auth import get_access_token

# ---------------------------------
# CONFIG
# ---------------------------------
ZOHO_BASE_URL = "https://recruit.zoho.in/recruit/v2"

# (MOCK_JOBS removed: all job operations use real Zoho Recruiter API)

# ---------------------------------
# COMMON HEADERS
# ---------------------------------
def _headers():
    return {
        "Authorization": f"Zoho-oauthtoken {get_access_token()}",
        "Content-Type": "application/json"
    }

# ---------------------------------
# GET JOBS (MOCKED)
# ---------------------------------
def get_jobs(page=1, limit=10):
    """
    Fetch job openings from Zoho Recruit API.
    """
    url = f"{ZOHO_BASE_URL}/JobOpenings"
    params = {
        "page": page,
        "per_page": limit
    }
    res = requests.get(url, headers=_headers(), params=params, timeout=10)
    res.raise_for_status()
    data = res.json().get("data", [])
    jobs = []
    for job in data:
        jobs.append({
            "id": job.get("id"),
            "title": job.get("Job_Title"),
            "location": job.get("City"),
            "status": job.get("Status"),
            "external_url": job.get("Job_Url")
        })
    has_more = len(data) == limit
    return {
        "results": jobs,
        "page": page,
        "limit": limit,
        "has_more": has_more
    }

# ---------------------------------
# CREATE CANDIDATE (REAL ZOHO)
# ---------------------------------
def create_candidate(candidate_data):
    url = f"{ZOHO_BASE_URL}/Candidates"

    name_parts = candidate_data["name"].split()
    first_name = name_parts[0]
    last_name = name_parts[-1] if len(name_parts) > 1 else "NA"

    payload = {
        "data": [
            {
                "First_Name": first_name,
                "Last_Name": last_name,
                "Email": candidate_data["email"],
                "Mobile": candidate_data["phone"]
            }
        ]
    }

    res = requests.post(url, headers=_headers(), json=payload, timeout=10)
    res.raise_for_status()

    data = res.json()["data"][0]

    # ✅ NORMALIZE ID (THIS IS CRITICAL)
    candidate_id = data.get("details", {}).get("id")
    if not candidate_id:
        raise RuntimeError("Zoho Recruit did not return candidate id")

    return {
        "id": candidate_id,
        "name": f"{first_name} {last_name}",
        "email": candidate_data["email"]
    }


# ---------------------------------
# APPLY CANDIDATE TO JOB (SIMULATED)
# ---------------------------------
def apply_candidate(job_id, candidate):
    """
    Zoho Recruit trial does not allow Applications API.
    We simulate application creation safely.
    """

    return {
        "id": str(uuid.uuid4()),
        "job_id": job_id,
        "candidate_name": candidate["name"],
        "email": candidate["email"],
        "status": "APPLIED"
    }


# ---------------------------------
# GET APPLICATIONS (SIMULATED)
# ---------------------------------
def get_applications(job_id):
    """
    Applications are simulated because Zoho Recruit trial blocks
    Applications API for Job Openings.
    """

    return [
        {
            "id": str(uuid.uuid4()),
            "candidate_name": "Sample Candidate",
            "email": "sample@example.com",
            "status": "APPLIED"
        }
    ]
