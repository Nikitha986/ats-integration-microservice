# handler.py
import json
from ats_client import (
    get_jobs,
    create_candidate,
    apply_candidate,
    get_applications
)


# -----------------------------
# Common JSON Response Helper
# -----------------------------
def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, indent=2)
    }


# -----------------------------
# GET /jobs
# -----------------------------

def jobs(event, context):
    print("DEBUG: jobs() function called")

    try:
        params = event.get("queryStringParameters") or {}
        print("DEBUG params:", params)

        page = int(params.get("page", 1))
        limit = int(params.get("limit", 10))

        print("DEBUG calling get_jobs with:", page, limit)

        ats_response = get_jobs(page=page, limit=limit)

        print("DEBUG ats_response:", ats_response)

        return response(200, ats_response)

    except Exception as e:
        print("DEBUG ERROR:", str(e))
        return response(500, {
            "error": "ATS_ERROR",
            "message": str(e)
        })




# -----------------------------
# POST /candidates
# -----------------------------
def candidates(event, context):
    try:
        if not event.get("body"):
            raise ValueError("Request body is required")

        body = json.loads(event["body"])

        # Basic validation
        required_fields = ["name", "email", "phone", "resume_url", "job_id"]
        for field in required_fields:
            if field not in body:
                raise ValueError(f"{field} is required")

        candidate = create_candidate(body)
        apply_candidate(body["job_id"], candidate)

        return response(201, {
            "message": "Candidate created and applied successfully",
            "candidate_id": candidate["id"]
        })

    except ValueError as ve:
        return response(400, {
            "error": "INVALID_REQUEST",
            "message": str(ve)
        })

    except Exception as e:
        return response(500, {
            "error": "ATS_ERROR",
            "message": str(e)
        })


# -----------------------------
# GET /applications
# -----------------------------
def applications(event, context):
    try:
        params = event.get("queryStringParameters")

        if not params or "job_id" not in params:
            raise ValueError("job_id query parameter is required")

        job_id = params["job_id"]

        apps = get_applications(job_id)

        return response(200, apps)

    except ValueError as ve:
        return response(400, {
            "error": "INVALID_REQUEST",
            "message": str(ve)
        })

    except Exception as e:
        return response(500, {
            "error": "ATS_ERROR",
            "message": str(e)
        })
