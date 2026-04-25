# 🤖 Artificial Intelligence — Problem Solving Assignment

---

## 👥 Team Members

| Name | Register Number |
|------|-----------------|
| Kanishkar S  | RA2411026050169 |
| Prabakaran S | RA2411026050151 |

> **Subject:** Artificial Intelligence
> **Deadline:** 25th April 2026

---

## 📁 Repository Structure

AI_ProblemSolving1_RA2411026050169/
├── Problem5_MapColoring/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── Problem14_InsuranceClaim/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
└── README.md

---

## 📌 Problems Implemented

| Problem | Title | Algorithm | Topic |
|---------|-------|-----------|-------|
| Problem 5 | Map Coloring Problem | CSP Backtracking | Constraint Satisfaction |
| Problem 14 | Rule-Based Insurance Claim System | Propositional Logic | Rule-Based Inference |

---

# 🗺️ Problem 5 — Map Coloring Problem (CSP)

## 1. Problem Description

In a map coloring scenario, different regions on a map must be colored
such that no two adjacent regions share the same color. This system
allows the user to input any map with regions and adjacency
relationships through an interactive web interface. The AI then assigns
colors to each region while satisfying all constraints using minimum colors.

### Key Features
- Interactive web interface built with Streamlit
- CSP Backtracking solver implemented from scratch
- NetworkX graph visualization with actual colors
- Supports 3 or 4 color options
- Preloaded examples — Default and India States
- Dark professional UI with gradient cards

---

## 2. Algorithm Used — CSP Backtracking

| Component | Map Coloring Equivalent |
|-----------|------------------------|
| Variables | Regions on the map |
| Domain | Available colors (Red, Green, Blue, Yellow) |
| Constraint | No two adjacent regions share same color |

### Backtracking Steps

Step 1: Pick first uncolored region
Step 2: Try each available color
Step 3: Check if color conflicts with any colored neighbor
Step 4: If no conflict — assign color — move to next region
Step 5: If conflict — try next color
Step 6: If all colors fail — backtrack to previous region
Step 7: Repeat until all regions colored or no solution found

---

## 3. Execution Steps

### Install Dependencies

cd Problem5_MapColoring
pip install -r requirements.txt

### Run the App

streamlit run app.py

### Open in Browser

http://localhost:8501

### requirements.txt

streamlit
networkx
matplotlib
pandas

---

## 4. Sample Output

### Input

Regions   : A, B, C, D
Adjacency : A-B, A-C, B-C, B-D, C-D
Colors    : 3

### Output

VALID COLORING FOUND

A → Red
B → Green
C → Blue
D → Red

Colors Used    : 3
Backtracks     : 2
Nodes Explored : 8

Final: No two adjacent regions share the same color

---

# 🛡️ Problem 14 — Rule-Based Insurance Claim Decision System

## 1. Problem Description

An insurance company needs an automated system to evaluate whether a
claim should be approved or rejected based on predefined logical rules.
The system uses Propositional Logic Inference to evaluate conditions
such as policy validity, document verification, accident reporting,
fraud detection and claim amount validation and produces an instant
APPROVED or REJECTED decision with full reasoning.

### Key Features
- Interactive web interface built with Streamlit
- 7 logical rules evaluated in real-time
- Full inference chain with step-by-step reasoning
- Rules Evaluation Table with pass/fail status
- Downloadable claim report
- Dark professional UI with gradient cards

---

## 2. Algorithm Used — Propositional Logic Inference

| Rule No | Rule Name | Condition |
|---------|-----------|-----------|
| Rule 1 | Policy Validity | policy_active AND premium_paid |
| Rule 2 | Document Verification | documents_valid == True |
| Rule 3 | Incident Reporting | accident_reported == True |
| Rule 4 | Coverage Period Check | incident_within_coverage == True |
| Rule 5 | Fraud Detection | fraud_suspected == False |
| Rule 6 | Claim Amount Validation | claim_amount <= coverage_limit |
| Rule 7 | Medical Records | IF Health THEN medical_records == True |

### Decision Logic

IF fraud_suspected        → INSTANT REJECT
IF policy invalid         → REJECT
IF documents invalid      → REJECT
IF outside coverage       → REJECT
IF amount exceeds limit   → REJECT
IF health + no records    → REJECT
IF all 7 rules pass       → APPROVE CLAIM

---

## 3. Execution Steps

### Install Dependencies

cd Problem14_InsuranceClaim
pip install -r requirements.txt

### Run the App

streamlit run app.py

### Open in Browser

http://localhost:8501

### requirements.txt

streamlit
pandas

---

## 4. Sample Output

### Approved Case

Policy Active          : Yes
Policy Type            : Health
Premium Paid           : Yes
Accident Reported      : Yes
Within Coverage Period : Yes
Fraud Suspected        : No
Documents Valid        : Yes
Medical Records        : Yes
Claim Amount           : 50000
Coverage Limit         : 100000

CLAIM APPROVED
Approved Amount : 50,000
Rules Passed    : 7 / 7
Rules Failed    : 0 / 7

Step 1: policy_active AND premium_paid     → TRUE
Step 2: documents_valid                    → TRUE
Step 3: accident_reported                  → TRUE
Step 4: incident_within_coverage           → TRUE
Step 5: fraud_suspected == False           → TRUE
Step 6: claim_amount <= coverage_limit     → TRUE
Step 7: medical_records (Health policy)    → TRUE

Final Inference: All critical rules passed → APPROVE CLAIM

### Rejected Case

CLAIM REJECTED
Rules Passed : 2 / 7
Rules Failed : 5 / 7

Final Inference: Critical rules failed → REJECT CLAIM

---

## How to Run Both Projects

git clone https://github.com/KANISHKAR614/AI_ProblemSolving1_RA2411026050169.git

cd AI_ProblemSolving1_RA2411026050169/Problem5_MapColoring
pip install -r requirements.txt
streamlit run app.py

cd ../Problem14_InsuranceClaim
pip install -r requirements.txt
streamlit run app.py

---

## Links

| Item | Link |
|------|------|
| GitHub Repository | https://github.com/Prabakaran-S697/AI_ProblemSolving1_RA2411026050151 |
| Problem  Live Demo (Map Coloring) | https://chromora.streamlit.app/ |
| Problem  Live Demo (Rule Based Insurance) | https://claimora.streamlit.app/ |
