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


def jobs(event, context):
    try:
        return response(200, get_jobs())
    except Exception as e:
        return response(500, {"error": str(e)})


def candidates(event, context):
    try:
        body = json.loads(event["body"])

        candidate = create_candidate(body)
        apply_candidate(body["job_id"], candidate)

        return response(201, {
            "message": "Candidate created and applied successfully",
            "candidate_id": candidate["id"]
        })

    except Exception as e:
        return response(500, {"error": str(e)})


def applications(event, context):
    try:
        job_id = event["queryStringParameters"]["job_id"]
        apps = get_applications(job_id)
        return response(200, apps)

    except Exception as e:
        return response(500, {"error": str(e)})
