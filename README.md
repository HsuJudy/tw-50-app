# Taiwan Vital Signs FHIR App

A web application for displaying blood pressure trends and risk alerts using FHIR (Fast Healthcare Interoperability Resources) standards.

## Features

- FHIR OAuth2 authentication
- Blood pressure trend visualization using Chart.js
- Risk alerts based on Taiwan hypertension clinical guidelines
- Supports TW Core Vital Signs Profile

## Setup

1. The app uses FHIR OAuth2 for authentication
2. Launch the app via `launch.html` to initiate OAuth flow
3. The main app (`index.html`) displays patient blood pressure data

## Deployment

- **Vercel**: https://tw-vital-signs-app.vercel.app
- **GitHub Pages**: Configure in repository settings

## Configuration

Update `launch.html` with your FHIR server details:
- `client_id`: Your FHIR client ID
- `iss`: Your FHIR server endpoint (will be replaced by EHR at launch)
- `redirect_uri`: Your app's redirect URI

