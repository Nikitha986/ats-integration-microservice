# ATS Integration Microservice (Python + Serverless)

## Project Overview
This project is a backend microservice built in Python using the Serverless Framework.  
It integrates with an Applicant Tracking System (ATS) to provide a unified REST API for jobs, candidates, and applications.

Zoho People is used as the target ATS.

---

## ATS Integration Approach
The service is designed to integrate with Zoho People as the underlying Applicant Tracking System (ATS).

For the purpose of this assignment and local demonstration:
- Job data is mocked to match the unified API contract
- Candidate creation and application workflows follow real ATS behavior
- OAuth 2.0 authentication is implemented using Zoho People
- Integration points are structured so the service can be connected to live Zoho People APIs in production

---

## APIs Exposed

### GET /jobs
Returns a list of open jobs.

```json
{
  "id": "string",
  "title": "string",
  "location": "string",
  "status": "OPEN | CLOSED | DRAFT",
  "external_url": "string"
}

###POST /candidates

Creates a candidate and attaches them to a job.

Request body:

{
  "name": "string",
  "email": "string",
  "phone": "string",
  "resume_url": "string",
  "job_id": "string"
}


Authentication (Zoho People OAuth 2.0)

Zoho People uses OAuth 2.0 authentication.

Steps to generate credentials:

Create a Zoho People free trial account

Open Zoho API Console

Create an OAuth client (Server-based application)

Generate an authorization code

Exchange the code for a refresh token

Store credentials securely using environment variables

The service uses the refresh token to generate short-lived access tokens dynamically.
