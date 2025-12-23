#!/usr/bin/env python3
"""
Script to POST test data to Taiwan Core FHIR server
Usage: python3 post-test-data.py
"""

import json
import sys
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

FHIR_SERVER = "https://thas.mohw.gov.tw/v/r4/fhir"
SCRIPT_DIR = Path(__file__).parent
TEST_DATA_DIR = SCRIPT_DIR / "test-data"

# Colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


def print_info(message: str):
    print(f"{Colors.YELLOW}{message}{Colors.NC}")


def print_header(message: str):
    print(f"{Colors.BLUE}{message}{Colors.NC}")


def post_resource(resource: Dict[str, Any], resource_type: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    POST a FHIR resource to the server
    
    Args:
        resource: The FHIR resource as a dictionary
        resource_type: The resource type (e.g., "Patient", "Observation")
    
    Returns:
        Tuple of (success: bool, response_resource: Dict or None)
    """
    url = f"{FHIR_SERVER}/{resource_type}"
    
    headers = {
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json"
    }
    
    try:
        print_info(f"POSTing {resource_type} (id: {resource.get('id', 'N/A')})...")
        
        response = requests.post(url, json=resource, headers=headers, timeout=30)
        
        if response.status_code >= 200 and response.status_code < 300:
            print_success(f"Success (HTTP {response.status_code})")
            try:
                result = response.json()
                print(json.dumps(result, indent=2, ensure_ascii=False))
                print()
                return True, result
            except:
                print(response.text)
                print()
                return True, None
        else:
            print_error(f"Failed (HTTP {response.status_code})")
            try:
                error = response.json()
                print(json.dumps(error, indent=2, ensure_ascii=False))
            except:
                print(response.text)
            print()
            return False, None
            
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {str(e)}")
        print()
        return False, None


def load_json_file(file_path: Path) -> Any:
    """Load JSON from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in {file_path}: {str(e)}")
        return None


def main():
    print_header("=" * 50)
    print_header("POSTing Test Data to FHIR Server")
    print_header(f"Server: {FHIR_SERVER}")
    print_header("=" * 50)
    print()
    
    # Step 1: POST Patient
    print_header("Step 1: POSTing Patient resource...")
    patient_file = TEST_DATA_DIR / "patient-simple.json"
    patient = load_json_file(patient_file)
    
    patient_id = None
    if patient:
        patient_success, patient_response = post_resource(patient, "Patient")
        if patient_success and patient_response:
            patient_id = patient_response.get("id")
            print_info(f"Patient created with ID: {patient_id}")
            print()
    else:
        print_error("Failed to load Patient resource")
        patient_success = False
    
    if not patient_id:
        print_error("Cannot proceed without Patient ID. Exiting.")
        return
    
    # Step 2: POST Observations
    print_header("Step 2: POSTing Observation resources...")
    observations_file = TEST_DATA_DIR / "observations-simple.json"
    observations_data = load_json_file(observations_file)
    
    if observations_data:
        # Handle both Bundle and array formats
        if isinstance(observations_data, dict) and observations_data.get("resourceType") == "Bundle":
            # Extract observations from Bundle.entry[].resource
            entries = observations_data.get("entry", [])
            observations = [entry.get("resource") for entry in entries if entry.get("resource")]
            print_info(f"Found Bundle with {len(observations)} observations to POST")
        elif isinstance(observations_data, list):
            # Handle array format (backward compatibility)
            observations = observations_data
            print_info(f"Found {len(observations)} observations to POST")
        else:
            print_error("Observations file should contain a Bundle or JSON array")
            observations = []
        
        if observations:
            print()
            success_count = 0
            for i, observation in enumerate(observations, 1):
                if not observation:
                    continue
                # Update the subject reference to use the actual Patient ID
                observation["subject"] = {"reference": f"Patient/{patient_id}"}
                
                print_info(f"Observation {i}/{len(observations)}:")
                obs_success, _ = post_resource(observation, "Observation")
                if obs_success:
                    success_count += 1
            
            print_header(f"Summary: {success_count}/{len(observations)} observations posted successfully")
        else:
            print_error("No observations found to POST")
    else:
        print_error("Failed to load Observations")
    
    print()
    print_header("=" * 50)
    print_header("Done!")
    print_header("=" * 50)
    print()
    print("You can now test your app with:")
    print("  Launch URI: https://tw-vital-signs-app.vercel.app/launch.html")
    if patient_id:
        print(f"  Patient ID: {patient_id}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

