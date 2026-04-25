# 🛡️ Rule-Based Insurance Claim Decision System

## 1. Problem Description

An insurance company needs an automated system to evaluate whether a claim should be approved or rejected based on predefined logical rules. The system uses Propositional Logic Inference to evaluate conditions such as policy validity, document verification, accident reporting, fraud detection, and claim amount validation and produces an instant APPROVED or REJECTED decision with full reasoning.

### Key Features
- Interactive web interface built with Streamlit
- 7 logical rules evaluated in real-time
- Full inference chain showing step-by-step reasoning
- Rules Evaluation Table with pass/fail status
- Downloadable claim report
- Dark professional UI

---

## 2. Algorithms Used

### Propositional Logic — Rule-Based Inference Engine

A rule-based expert system where each rule is an IF-THEN logical statement evaluated against user-provided facts.

| Rule No | Rule Name | Condition |
|---------|-----------|-----------|
| Rule 1 | Policy Validity | policy_active AND premium_paid |
| Rule 2 | Document Verification | documents_valid == True |
| Rule 3 | Incident Reporting | accident_reported == True |
| Rule 4 | Coverage Period Check | incident_within_coverage == True |
| Rule 5 | Fraud Detection | fraud_suspected == False |
| Rule 6 | Claim Amount Validation | claim_amount <= coverage_limit AND claim_amount > 0 |
| Rule 7 | Medical Records | IF Health policy THEN medical_records == True |

### Decision Logic

- IF fraud_suspected is True → INSTANT REJECT
- IF policy is inactive OR premium not paid → REJECT
- IF documents are invalid → REJECT
- IF incident is outside coverage period → REJECT
- IF claim amount exceeds coverage limit → REJECT
- IF health policy AND medical records missing → REJECT
- IF all 7 rules pass → APPROVE CLAIM

---

## 3. Execution Steps

### Requirements
- Python 3.8 or above
- pip

### Step 1 — Clone the Repository

git clone https://github.com/YourUsername/AI_ProblemSolving_YourRegNo.git
cd AI_ProblemSolving_YourRegNo/Problem14_InsuranceClaim

### Step 2 — Install Dependencies

pip install -r requirements.txt

### Step 3 — Run the Application

streamlit run app.py

### Step 4 — Open in Browser

claimora.streamlit.app
### requirements.txt

streamlit
pandas

---

## 4. Sample Outputs

### Sample Input 1 — Approved Case

| Field | Value |
|-------|-------|
| Policy Active | Yes |
| Policy Type | Health |
| Premium Paid | Yes |
| Accident Reported | Yes |
| Within Coverage Period | Yes |
| Fraud Suspected | No |
| Documents Valid | Yes |
| Medical Records | Yes |
| Claim Amount | 50000 |
| Coverage Limit | 100000 |

### Output 1

Decision        : CLAIM APPROVED
Approved Amount : 50,000
Rules Passed    : 7 / 7
Rules Failed    : 0 / 7

Inference Chain:
Step 1 - Check policy_active AND premium_paid → TRUE
Step 2 - Check documents_valid → TRUE
Step 3 - Check accident_reported → TRUE
Step 4 - Check incident_within_coverage → TRUE
Step 5 - Check fraud_suspected == False → TRUE
Step 6 - Check claim_amount <= coverage_limit → TRUE
Step 7 - Check medical_records for Health policy → TRUE

Final Inference: All critical rules passed → APPROVE CLAIM

---

### Sample Input 2 — Rejected Case

| Field | Value |
|-------|-------|
| Policy Active | No |
| Premium Paid | No |
| Fraud Suspected | Yes |
| Documents Valid | No |
| Claim Amount | 200000 |
| Coverage Limit | 100000 |

### Output 2

Decision        : CLAIM REJECTED
Approved Amount : 0
Rules Passed    : 2 / 7
Rules Failed    : 5 / 7

Final Inference: Critical rules failed → REJECT CLAIM

---

## Team Members

| Name | Register Number |
|------|-----------------|
| Member 1 | RA2411026050169 |
| Member 1 | RA2411026050151 |

---

## Subject Details

- Subject  : Artificial Intelligence
- Topic    : Problem 14 — Rule-Based Insurance Claim Decision System
- Deadline : 25th April 2026
