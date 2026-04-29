# FHIR Resource Validator
# Author: Alwin
# Description: Validates FHIR R4 resources - Patient, Appointment, Observation
# FHIR (Fast Healthcare Interoperability Resources) is a standard for
# exchanging healthcare data between systems

# ------------------------------------------------------------
# STEP 1: Define allowed values from the FHIR R4 specification
# ------------------------------------------------------------

# These are the only gender values FHIR R4 allows
VALID_GENDER = ["male", "female", "other", "unknown"]

# These are the only status values allowed for an Appointment resource
VALID_APPOINTMENT_STATUS = [
    "proposed", "pending", "booked", "arrived",
    "fulfilled", "cancelled", "noshow", "entered-in-error",
    "checked-in", "waitlist"
]

# These are the only status values allowed for an Observation resource
VALID_OBSERVATION_STATUS = [
    "registered", "preliminary", "final", "amended",
    "corrected", "cancelled", "entered-in-error", "unknown"
]

# ------------------------------------------------------------
# STEP 2: Validation function for Patient resource
# ------------------------------------------------------------

def validate_patient(data):
    # Start with an empty list - we will add errors here if we find problems
    errors = []

    # Check 1: resourceType must say "Patient"
    if data.get("resourceType") != "Patient":
        errors.append("resourceType must be 'Patient'")

    # Check 2: id is required in every FHIR resource
    if not data.get("id"):
        errors.append("Missing required field: id")

    # Check 3: if gender is provided, it must be a valid FHIR gender code
    if "gender" in data:
        if data["gender"] not in VALID_GENDER:
            errors.append(f"Invalid gender '{data['gender']}'. Must be one of: {VALID_GENDER}")

    # Check 4: if birthDate is provided, it must follow YYYY-MM-DD format
    if "birthDate" in data:
        from datetime import datetime
        try:
            datetime.strptime(data["birthDate"], "%Y-%m-%d")
        except ValueError:
            errors.append("birthDate must be in YYYY-MM-DD format (example: 1999-05-15)")

    return errors

# ------------------------------------------------------------
# STEP 3: Validation function for Appointment resource
# ------------------------------------------------------------

def validate_appointment(data):
    errors = []

    # Check 1: resourceType must say "Appointment"
    if data.get("resourceType") != "Appointment":
        errors.append("resourceType must be 'Appointment'")

    # Check 2: id is required
    if not data.get("id"):
        errors.append("Missing required field: id")

    # Check 3: status is required and must be a valid FHIR status code
    if not data.get("status"):
        errors.append("Missing required field: status")
    elif data["status"] not in VALID_APPOINTMENT_STATUS:
        errors.append(f"Invalid status '{data['status']}'. Must be one of: {VALID_APPOINTMENT_STATUS}")

    # Check 4: participant is required in every Appointment resource
    if not data.get("participant"):
        errors.append("Missing required field: participant")

    return errors

# ------------------------------------------------------------
# STEP 4: Validation function for Observation resource
# ------------------------------------------------------------

def validate_observation(data):
    errors = []

    # Check 1: resourceType must say "Observation"
    if data.get("resourceType") != "Observation":
        errors.append("resourceType must be 'Observation'")

    # Check 2: id is required
    if not data.get("id"):
        errors.append("Missing required field: id")

    # Check 3: status is required and must be a valid FHIR status code
    if not data.get("status"):
        errors.append("Missing required field: status")
    elif data["status"] not in VALID_OBSERVATION_STATUS:
        errors.append(f"Invalid status '{data['status']}'. Must be one of: {VALID_OBSERVATION_STATUS}")

    # Check 4: code is required - it identifies what was observed (e.g. blood pressure)
    if not data.get("code"):
        errors.append("Missing required field: code")

    return errors

# ------------------------------------------------------------
# STEP 5: Main function that runs the right validator
# ------------------------------------------------------------

def validate_resource(resource_type, data):
    print(f"\n--- Validating {resource_type} ---")

    # Call the right validation function based on resource type
    if resource_type == "Patient":
        errors = validate_patient(data)
    elif resource_type == "Appointment":
        errors = validate_appointment(data)
    elif resource_type == "Observation":
        errors = validate_observation(data)
    else:
        print(f"Unknown resource type: {resource_type}")
        return

    # Print result
    if not errors:
        print(f"VALID: {resource_type} resource passed validation")
    else:
        print(f"INVALID: {resource_type} resource failed validation")
        for error in errors:
            print(f"  - {error}")

# ------------------------------------------------------------
# STEP 6: Test cases
# ------------------------------------------------------------

# Test 1: Valid Patient
validate_resource("Patient", {
    "resourceType": "Patient",
    "id": "patient-001",
    "name": [{"family": "Thomas", "given": ["Alwin"]}],
    "gender": "male",
    "birthDate": "1999-05-15"
})

# Test 2: Invalid Patient - wrong gender code, wrong date format
validate_resource("Patient", {
    "resourceType": "Patient",
    "id": "patient-002",
    "gender": "M",
    "birthDate": "15-05-1990"
})

# Test 3: Invalid Patient - missing resourceType
validate_resource("Patient", {
    "id": "patient-003",
    "gender": "female"
})

# Test 4: Valid Appointment
validate_resource("Appointment", {
    "resourceType": "Appointment",
    "id": "appt-001",
    "status": "booked",
    "participant": [{"status": "accepted"}]
})

# Test 5: Invalid Appointment - wrong status, missing participant
validate_resource("Appointment", {
    "resourceType": "Appointment",
    "id": "appt-002",
    "status": "confirmed"
})

# Test 6: Valid Observation - blood pressure reading
validate_resource("Observation", {
    "resourceType": "Observation",
    "id": "obs-001",
    "status": "final",
    "code": {
        "coding": [{
            "system": "http://loinc.org",
            "code": "55284-4",
            "display": "Blood Pressure"
        }]
    }
})

# Test 7: Invalid Observation - wrong status, missing code
validate_resource("Observation", {
    "resourceType": "Observation",
    "id": "obs-002",
    "status": "done"
})