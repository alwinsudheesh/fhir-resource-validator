# FHIR R4 Resource Validator

A Python-based validator for FHIR R4 (Fast Healthcare Interoperability Resources) 
resources, built to understand and apply health data interoperability standards.

## What is FHIR?
FHIR (Fast Healthcare Interoperability Resources) is the international standard 
for exchanging healthcare data between systems such as Hospital Information Systems 
(HIS), Electronic Health Records (EHR), and health information exchanges (HIE).

## What this project does
This validator checks whether FHIR R4 resources are correctly structured according 
to the official specification. It validates three core resource types used in 
hospital workflows:

- **Patient** — validates gender codes, date format, required fields
- **Appointment** — validates status codes, participant requirement
- **Observation** — validates status codes, code requirement

## Validation checks
| Resource | Field | Rule |
|----------|-------|------|
| Patient | gender | Must be: male, female, other, unknown |
| Patient | birthDate | Must follow YYYY-MM-DD format |
| Appointment | status | Must be a valid FHIR appointment status code |
| Appointment | participant | Required field |
| Observation | status | Must be a valid FHIR observation status code |
| Observation | code | Required field |

## Sample output

--- Validating Patient ---
VALID: Patient resource passed validation
--- Validating Patient ---
INVALID: Patient resource failed validation

Invalid gender 'M'. Must be one of: ['male', 'female', 'other', 'unknown']
birthDate must be in YYYY-MM-DD format (example: 1999-05-15)


## How to run
1. Install the required library:
pip install fhir.resources
2. Run the validator:
python "FHIR Validator.py"

## Standards reference
- FHIR R4 specification: https://hl7.org/fhir/R4/
- Patient resource: https://hl7.org/fhir/R4/patient.html
- Appointment resource: https://hl7.org/fhir/R4/appointment.html
- Observation resource: https://hl7.org/fhir/R4/observation.html

## Background
Built as part of a digital health learning roadmap covering OpenHIE, 
FHIR standards, and health information exchange concepts.
Paste that in, commit it, and the repo is complete.
