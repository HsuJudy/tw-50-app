# Test Data for Taiwan Core FHIR

This directory contains test data for demonstrating the blood pressure trend application.

## Files

- `patient-example.json` - A Patient resource following TW Core Patient Profile
- `observations-bp.json` - An array of Observation resources for blood pressure measurements

## Blood Pressure Data

The observations include 5 blood pressure readings over time to demonstrate trends:

1. **2024-01-15**: 120/80 mmHg (Normal)
2. **2024-02-20**: 125/82 mmHg (Elevated)
3. **2024-03-10**: 130/85 mmHg (Stage 1 Hypertension)
4. **2024-04-05**: 135/88 mmHg (Stage 1 Hypertension)
5. **2024-05-12**: 142/92 mmHg (Stage 2 Hypertension - triggers alert)

The last reading (142/92) is above the 140 mmHg threshold, which will trigger the risk alert in the application.

## POSTing Data to FHIR Server

### Using Python Script (Recommended)

```bash
cd /Users/creator/smart/tw-vital-signs-app
python3 post-test-data.py
```

### Using Bash Script

```bash
cd /Users/creator/smart/tw-vital-signs-app
./post-test-data.sh
```

### Using curl Manually

#### POST Patient:

```bash
curl -X POST \
  -H "Content-Type: application/fhir+json" \
  -H "Accept: application/fhir+json" \
  -d @test-data/patient-example.json \
  https://thas.mohw.gov.tw/v/r4/fhir/Patient
```

#### POST Observations:

You'll need to extract each observation from the array and POST individually, or use the scripts provided.

## FHIR Server

- **Base URL**: https://thas.mohw.gov.tw/v/r4/fhir
- **Patient Endpoint**: `POST /Patient`
- **Observation Endpoint**: `POST /Observation`

## Resource Profiles

All resources follow Taiwan Core (TW Core) Implementation Guide profiles:

- Patient: `https://twcore.mohw.gov.tw/ig/twcore/StructureDefinition/Patient-twcore`
- Observation: `https://twcore.mohw.gov.tw/ig/twcore/StructureDefinition/Observation-bloodPressure-twcore`

## LOINC Codes Used

- **85354-9**: Blood pressure panel with all children optional
- **8480-6**: Systolic blood pressure
- **8462-4**: Diastolic blood pressure

## Testing the Application

After posting the data:

1. Launch the app: https://tw-vital-signs-app.vercel.app/launch.html
2. The app should display:
   - Patient name: 陳加玲
   - Blood pressure trend chart showing the 5 readings
   - Risk alert for the latest reading (142/92 mmHg)

## Notes

- The Patient resource ID is `pat-example`
- All Observation resources reference `Patient/pat-example`
- Make sure to POST the Patient first before POSTing Observations
- The server may require authentication - check the sandbox documentation

