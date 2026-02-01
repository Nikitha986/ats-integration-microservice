# ATS Integration Microservice – README

---

## How to Create Free Trial

This project uses **Zoho Recruiter** as the Applicant Tracking System (ATS).


Steps to create a free trial account:
1. Go to the **Zoho Recruiter** website: https://recruit.zoho.in/
2. Click on **Start Free Trial**
3. Sign up using your email address or Google account
4. Complete the initial company setup 
5. After setup, you will be redirected to the Zoho Recruiter dashboard

The free trial account is sufficient for testing authentication and ATS integration.

---

## How to Generate API Key / Token

Zoho Recruiter uses **OAuth 2.0** authentication.

### Step 1: Create OAuth Client
1. Open the **Zoho API Console**
2. Log in using the same Zoho account
3. Click **Add Client**
4. Select **Server-based Application**
5. Provide the following details:
   - Client Name:
   - Homepage URL: http://localhost
   - Redirect URI: http://localhost
6. Create the client

This generates:
- Client ID
- Client Secret

---

### Step 2: Generate Authorization Code
1. Use the OAuth authorization flow from Zoho Accounts
2. Grant permission when prompted
3. After authorization, an authorization code will be generated
4. Copy the authorization code

---

### Step 3: Generate Refresh Token
1. Exchange the authorization code for tokens using Zoho OAuth token generation
2. From the response, store the **refresh token**

---

### Step 4: Configure Environment Variables
Create a `.env` file in the project root and add:



```env
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
```
---
📡 API Endpoints
## API Endpoints

All endpoints are available under the `/dev` prefix when running locally with serverless-offline.

### GET /dev/jobs
Returns a list of jobs from Zoho Recruiter in a standardized format:

```
[
  {
    "id": "string",
    "title": "string",
    "location": "string",
    "status": "OPEN | CLOSED | DRAFT",
    "external_url": "string"
  }
]
```

### POST /dev/candidates
Creates a candidate in Zoho Recruiter and applies them to a job.

Request body:
```
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "resume_url": "string",
  "job_id": "string"
}
```
Response:
```
{
  "message": "Candidate created and applied successfully",
  "candidate_id": "string"
}
```

### GET /dev/applications?job_id=...
Returns applications for a given job (simulated due to Zoho Recruiter trial limitations):
```
[
  {
    "id": "string",
    "candidate_name": "string",
    "email": "string",
    "status": "APPLIED | SCREENING | REJECTED | HIRED"
  }
]
```

---

## How to Run Locally

1. Install dependencies:
   ```
   pip install -r requirements.txt
   npm install
   ```
2. Configure your `.env` file as described above.
3. Start the serverless offline server:
   ```
   serverless offline
   ```
4. Test endpoints using curl or Postman (see above for URLs).

---

## Example curl Calls

Get jobs:
```
curl http://localhost:3000/dev/jobs
```

Create candidate (replace job_id):
```
Invoke-WebRequest -Uri http://localhost:3000/dev/candidates -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"name":"John Doe","email":"john@example.com","phone":"1234567890","resume_url":"https://example.com/resume.pdf","job_id":"<REAL_JOB_ID>"}'
```

Get applications:
```
curl "http://localhost:3000/dev/applications?job_id=<REAL_JOB_ID>"
```

---

## Notes
- All job and candidate operations use the real Zoho Recruiter API.
- Application creation/listing is simulated due to Zoho Recruiter trial API limitations.
- Candidates created via the API will appear in your Zoho Recruiter dashboard under "Candidates".


