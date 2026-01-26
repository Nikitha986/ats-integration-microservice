# ATS Integration Microservice – README

---

## How to Create Free Trial / Sandbox in the ATS

This project uses **Zoho People** as the Applicant Tracking System (ATS).

Steps to create a free trial account:

1. Open the **Zoho People website**
2. Click on **Start Free Trial**
3. Sign up using an email address or Google account
4. Complete the initial company setup (dummy company details are sufficient)
5. After setup, you will be redirected to the Zoho People dashboard

The free trial account is sufficient for testing authentication and ATS integration.

---

## How to Generate API Key / Token

Zoho People uses **OAuth 2.0** authentication.

### Step 1: Create OAuth Client
1. Open the **Zoho API Console**
2. Log in using the same Zoho account
3. Click **Add Client**
4. Select **Server-based Application**
5. Provide the following details:
   - Client Name: ATS Integration Service
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
ZOHO_BASE_URL=zoho_people_api_domain
