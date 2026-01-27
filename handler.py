# handler.py
import json
from ats_client import (
    get_jobs,
    create_candidate,
    apply_candidate,
    get_applications
)

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
    try:
        params = event.get("queryStringParameters") or {}
        page = int(params.get("page", 1))
        limit = int(params.get("limit", 10))

        ats_response = get_jobs(page=page, limit=limit)

        # return only standardized job list
        return response(200, ats_response["results"])

    except Exception as e:
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

        required_fields = ["name", "email", "phone", "resume_url", "job_id"]
        for field in required_fields:
            if field not in body:
                raise ValueError(f"{field} is required")

        # 1. Create candidate in ATS
        candidate = create_candidate(body)
        apply_candidate(body["job_id"], candidate)

       

        return response(201, {
            "message": "Candidate created and applied successfully",
            "candidate_id": candidate["id"],
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

        # standardize output schema
        formatted_apps = [
            {
                "id": app["id"],
                "candidate_name": app["candidate_name"],
                "email": app["email"],
                "status": app["status"]
            }
            for app in apps
        ]

        return response(200, formatted_apps)

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
