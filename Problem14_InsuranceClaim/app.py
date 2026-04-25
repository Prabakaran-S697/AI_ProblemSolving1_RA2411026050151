import streamlit as st
import pandas as pd
import datetime

# ──────────────────────────────────────────────
# UPGRADE 1 — Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="ClaimAI — Insurance Decision System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# UPGRADE 1 — Global Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Dark theme override */
.stApp {
    background-color: #0f1219;
    color: #f1f5f9;
}

/* Sidebar dark */
[data-testid="stSidebar"] {
    background-color: #1a1f2e !important;
    border-right: 1px solid #2d3548;
}

/* Sidebar labels & text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span,
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3,
[data-testid="stSidebar"] .stMarkdown h4,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #cbd5e1 !important;
}

/* All selectbox/input backgrounds */
[data-testid="stSelectbox"] > div,
[data-testid="stNumberInput"] > div > div {
    background-color: #242938 !important;
    border: 1px solid #2d3548 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}

/* Primary button */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    height: 52px !important;
    width: 100% !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.6) !important;
}

/* Secondary button */
[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #2d3548 !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    width: 100% !important;
}

/* Section headers in sidebar */
.section-header {
    background: #242938;
    border: 1px solid #2d3548;
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 12px;
    font-weight: 600;
    font-size: 14px;
    color: #f1f5f9;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #242938 !important;
    border: 1px solid #2d3548 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="stMetric"]:hover {
    border-color: #6366f1 !important;
    transition: border-color 0.2s ease;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}

/* Dataframe table */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #2d3548 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: #242938 !important;
    border: 1px solid #2d3548 !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #f1f5f9 !important;
    font-size: 15px !important;
}

/* Divider */
hr {
    border-color: #2d3548 !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None


# ──────────────────────────────────────────────
# Helper: Convert selectbox value to boolean
# ──────────────────────────────────────────────
def to_bool(val):
    """Convert selectbox string to boolean or None."""
    if val == "Yes":
        return True
    elif val == "No":
        return False
    return None  # "N/A"


# ──────────────────────────────────────────────
# RULE ENGINE — Pure Python functions
# ──────────────────────────────────────────────
def rule_policy_validity(policy_active, premium_paid):
    """Rule 1 — Policy Validity Check"""
    condition = (policy_active is True) and (premium_paid is True)
    name = "Policy Validity"
    if condition:
        explanation = "Policy is active and premium is paid on time."
    else:
        explanation = "Policy is inactive or premium not paid — claim invalid."
    return name, condition, explanation


def rule_document_completeness(documents_valid):
    """Rule 2 — Document Completeness"""
    condition = documents_valid is True
    name = "Document Verification"
    if condition:
        explanation = "All required documents submitted and verified."
    else:
        explanation = "Documents missing or invalid — cannot process claim."
    return name, condition, explanation


def rule_incident_reporting(accident_reported):
    """Rule 3 — Incident Reporting"""
    condition = accident_reported is True
    name = "Incident Reporting"
    if condition:
        explanation = "Incident was reported to authorities."
    else:
        explanation = "Incident not reported — claim may be rejected."
    return name, condition, explanation


def rule_coverage_period(incident_within_coverage):
    """Rule 4 — Coverage Period"""
    condition = incident_within_coverage is True
    name = "Coverage Period Check"
    if condition:
        explanation = "Incident occurred within the active coverage period."
    else:
        explanation = "Incident outside coverage period — not eligible."
    return name, condition, explanation


def rule_fraud_detection(fraud_suspected):
    """Rule 5 — Fraud Detection"""
    condition = fraud_suspected is False
    name = "Fraud Detection"
    if condition:
        explanation = "No fraud indicators detected."
    else:
        explanation = "⚠️ Fraud suspected — claim automatically rejected."
    return name, condition, explanation


def rule_claim_amount_validation(claim_amount, coverage_limit):
    """Rule 6 — Claim Amount vs Coverage"""
    condition = (claim_amount <= coverage_limit) and (claim_amount > 0)
    name = "Claim Amount Validation"
    if condition:
        explanation = "Claim amount is within coverage limit."
    else:
        explanation = "Claim amount exceeds coverage limit or is zero."
    return name, condition, explanation


def rule_medical_records(policy_type, medical_records):
    """Rule 7 — Health Policy Medical Records"""
    if policy_type == "Health":
        condition = medical_records is True
    else:
        condition = True
    name = "Medical Records (Health Claims)"
    if condition:
        explanation = "Medical records verified (or not required for this policy type)."
    else:
        explanation = "Medical records missing for health insurance claim."
    return name, condition, explanation


def evaluate_claim(facts):
    """
    Run all rules and produce the final decision.
    Returns a dict with decision, rules, approved_amount, etc.
    """
    # Convert string inputs to booleans
    policy_active = to_bool(facts["policy_active"])
    premium_paid = to_bool(facts["premium_paid"])
    accident_reported = to_bool(facts["accident_reported"])
    incident_within_coverage = to_bool(facts["incident_within_coverage"])
    fraud_suspected = to_bool(facts["fraud_suspected"])
    documents_valid = to_bool(facts["documents_valid"])
    medical_records = to_bool(facts["medical_records"])
    policy_type = facts["policy_type"]
    claim_amount = facts["claim_amount"]
    coverage_limit = facts["coverage_limit"]

    # Evaluate each rule
    rules = []
    rules.append(rule_policy_validity(policy_active, premium_paid))
    rules.append(rule_document_completeness(documents_valid))
    rules.append(rule_incident_reporting(accident_reported))
    rules.append(rule_coverage_period(incident_within_coverage))
    rules.append(rule_fraud_detection(fraud_suspected))
    rules.append(rule_claim_amount_validation(claim_amount, coverage_limit))
    rules.append(rule_medical_records(policy_type, medical_records))

    rules_passed = sum(1 for _, cond, _ in rules if cond)
    rules_failed = sum(1 for _, cond, _ in rules if not cond)

    # ── FINAL DECISION LOGIC ──
    decision = "APPROVED"

    if fraud_suspected is True:
        decision = "REJECTED"
    elif policy_active is not True or premium_paid is not True:
        decision = "REJECTED"
    elif documents_valid is not True:
        decision = "REJECTED"
    elif incident_within_coverage is not True:
        decision = "REJECTED"
    elif claim_amount > coverage_limit or claim_amount == 0:
        decision = "REJECTED"
    elif policy_type == "Health" and medical_records is not True:
        decision = "REJECTED"

    approved_amount = min(claim_amount, coverage_limit) if decision == "APPROVED" else 0

    # Build inference chain steps
    inference_chain = []
    inference_chain.append(
        f"Step 1: Check policy_active ({policy_active}) AND premium_paid ({premium_paid}) → {'TRUE' if rules[0][1] else 'FALSE'}"
    )
    inference_chain.append(
        f"Step 2: Check documents_valid ({documents_valid}) → {'TRUE' if rules[1][1] else 'FALSE'}"
    )
    inference_chain.append(
        f"Step 3: Check accident_reported ({accident_reported}) → {'TRUE' if rules[2][1] else 'FALSE'}"
    )
    inference_chain.append(
        f"Step 4: Check incident_within_coverage ({incident_within_coverage}) → {'TRUE' if rules[3][1] else 'FALSE'}"
    )
    inference_chain.append(
        f"Step 5: Check fraud_suspected ({fraud_suspected}) == False → {'TRUE' if rules[4][1] else 'FALSE'}"
    )
    inference_chain.append(
        f"Step 6: Check claim_amount (₹{claim_amount:,}) ≤ coverage_limit (₹{coverage_limit:,}) AND claim_amount > 0 → {'TRUE' if rules[5][1] else 'FALSE'}"
    )
    inference_chain.append(
        f"Step 7: Check medical_records for policy_type='{policy_type}' → {'TRUE' if rules[6][1] else 'FALSE'}"
    )

    if decision == "APPROVED":
        inference_chain.append("Final Inference: All critical rules passed → APPROVE CLAIM")
    else:
        failed_names = [name for name, cond, _ in rules if not cond]
        inference_chain.append(
            f"Final Inference: Failed rule(s): {', '.join(failed_names)} → REJECT CLAIM"
        )

    return {
        "decision": decision,
        "rules": rules,
        "rules_passed": rules_passed,
        "rules_failed": rules_failed,
        "approved_amount": approved_amount,
        "inference_chain": inference_chain,
        "facts": facts,
    }


# ──────────────────────────────────────────────
# UPGRADE 3 — SIDEBAR HEADER
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 20px;">
        <div style="font-size:36px; margin-bottom:8px;">🛡️</div>
        <div style="font-size:17px; font-weight:700; color:#f1f5f9;">
            Claim Input Form
        </div>
        <div style="font-size:12px; color:#94a3b8; margin-top:4px;">
            Fill all sections to evaluate
        </div>
        <div style="height:2px; background:linear-gradient(90deg,#6366f1,#a5b4fc);
            border-radius:2px; margin-top:16px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── UPGRADE 4 — Section: Policy Information ──
    st.markdown("""
    <div style="background:#1e2330; border-left:3px solid #6366f1;
        border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
        <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
            📋 Policy Information
        </span>
    </div>
    """, unsafe_allow_html=True)
    policy_active = st.selectbox(
        "Is Policy Active?", ["Yes", "No"], index=0, key="inp_policy_active"
    )
    policy_type = st.selectbox(
        "Policy Type",
        ["Health", "Vehicle", "Property", "Life"],
        index=0,
        key="inp_policy_type",
    )
    premium_paid = st.selectbox(
        "Premium Paid on Time?", ["Yes", "No"], index=0, key="inp_premium_paid"
    )

    # ── UPGRADE 4 — Section: Accident / Incident Details ──
    st.markdown("""
    <div style="background:#1e2330; border-left:3px solid #ef4444;
        border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
        <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
            🚨 Accident / Incident Details
        </span>
    </div>
    """, unsafe_allow_html=True)
    accident_reported = st.selectbox(
        "Was Accident Reported to Authorities?",
        ["Yes", "No"],
        index=0,
        key="inp_accident_reported",
    )
    incident_within_coverage = st.selectbox(
        "Incident Within Coverage Period?",
        ["Yes", "No"],
        index=0,
        key="inp_incident_within_coverage",
    )
    fraud_suspected = st.selectbox(
        "Fraud Suspected?", ["Yes", "No"], index=1, key="inp_fraud_suspected"
    )

    # ── UPGRADE 4 — Section: Document Verification ──
    st.markdown("""
    <div style="background:#1e2330; border-left:3px solid #f59e0b;
        border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
        <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
            📄 Document Verification
        </span>
    </div>
    """, unsafe_allow_html=True)
    documents_valid = st.selectbox(
        "All Documents Submitted & Valid?",
        ["Yes", "No"],
        index=0,
        key="inp_documents_valid",
    )
    medical_records = st.selectbox(
        "Medical Records Available? (Health only)",
        ["Yes", "No", "N/A"],
        index=0,
        key="inp_medical_records",
    )

    # ── UPGRADE 4 — Section: Claim Details ──
    st.markdown("""
    <div style="background:#1e2330; border-left:3px solid #10b981;
        border-radius:8px; padding:10px 14px; margin:16px 0 12px;">
        <span style="font-size:14px; font-weight:700; color:#f1f5f9;">
            💰 Claim Details
        </span>
    </div>
    """, unsafe_allow_html=True)
    claim_amount = st.number_input(
        "Claim Amount (₹)",
        min_value=0,
        max_value=10000000,
        value=50000,
        step=1000,
        key="inp_claim_amount",
    )
    coverage_limit = st.number_input(
        "Coverage Limit (₹)",
        min_value=0,
        max_value=10000000,
        value=100000,
        step=1000,
        key="inp_coverage_limit",
    )

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    # ── Buttons ──
    col_eval, col_reset = st.columns(2)
    with col_eval:
        evaluate_clicked = st.button("🔍 Evaluate Claim", type="primary", use_container_width=True)
    with col_reset:
        reset_clicked = st.button("🔄 Reset", use_container_width=True)

# ──────────────────────────────────────────────
# Handle button actions
# ──────────────────────────────────────────────
if reset_clicked:
    st.session_state.result = None
    st.rerun()

if evaluate_clicked:
    facts = {
        "policy_active": policy_active,
        "policy_type": policy_type,
        "premium_paid": premium_paid,
        "accident_reported": accident_reported,
        "incident_within_coverage": incident_within_coverage,
        "fraud_suspected": fraud_suspected,
        "documents_valid": documents_valid,
        "medical_records": medical_records,
        "claim_amount": claim_amount,
        "coverage_limit": coverage_limit,
    }
    st.session_state.result = evaluate_claim(facts)

# ──────────────────────────────────────────────
# UPGRADE 2 — TOP NAVBAR
# ──────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1a1f2e, #242938);
    border: 1px solid #2d3548;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
">
    <div>
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:8px;">
            <span style="font-size:40px;">🛡️</span>
            <div>
                <h1 style="margin:0; font-size:26px; font-weight:800;
                    background: linear-gradient(135deg, #6366f1, #a5b4fc);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;">
                    Insurance Claim Decision System
                </h1>
                <p style="margin:4px 0 0; color:#94a3b8; font-size:13px;">
                    Rule-Based Propositional Logic Inference Engine
                </p>
            </div>
        </div>
    </div>
    <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <span style="background:#064e3b; color:#10b981; padding:6px 14px;
            border-radius:50px; font-size:12px; font-weight:600;">
            🟢 Engine Active
        </span>
        <span style="background:#1e1b4b; color:#a5b4fc; padding:6px 14px;
            border-radius:50px; font-size:12px; font-weight:600;">
            📋 7 Rules Loaded
        </span>
        <span style="background:#2d1b4e; color:#c084fc; padding:6px 14px;
            border-radius:50px; font-size:12px; font-weight:600;">
            ⚡ Propositional Logic
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# MAIN PANEL — Results
# ──────────────────────────────────────────────
if st.session_state.result is None:
    st.info(
        "👈 Fill in the claim details in the sidebar and click **Evaluate Claim** to begin inference."
    )
else:
    result = st.session_state.result
    decision = result["decision"]
    rules = result["rules"]
    rules_passed = result["rules_passed"]
    rules_failed = result["rules_failed"]
    approved_amount = result["approved_amount"]
    inference_chain = result["inference_chain"]
    facts = result["facts"]
    claim_amount = facts["claim_amount"]
    coverage_limit = facts["coverage_limit"]

    # ── UPGRADE 5 — Decision Banner ──
    if decision == "APPROVED":
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #064e3b, #065f46);
            border: 1px solid #10b981;
            border-left: 6px solid #10b981;
            border-radius: 16px;
            padding: 32px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 28px;
            box-shadow: 0 8px 32px rgba(16,185,129,0.2);
            flex-wrap: wrap;
            gap: 16px;
        ">
            <div style="display:flex; align-items:center; gap:20px;">
                <div style="font-size:52px;">✅</div>
                <div>
                    <div style="font-size:30px; font-weight:800; color:#ffffff;
                        letter-spacing:1px;">
                        CLAIM APPROVED
                    </div>
                    <div style="font-size:16px; color:#6ee7b7; margin-top:6px;">
                        Approved Amount: ₹{approved_amount:,}
                    </div>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px; color:#6ee7b7; margin-bottom:4px;">
                    CONFIDENCE
                </div>
                <div style="font-size:28px; font-weight:800; color:#10b981;">
                    100%
                </div>
                <div style="font-size:12px; color:#6ee7b7;">
                    All 7 rules passed
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #7f1d1d, #991b1b);
            border: 1px solid #ef4444;
            border-left: 6px solid #ef4444;
            border-radius: 16px;
            padding: 32px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 28px;
            box-shadow: 0 8px 32px rgba(239,68,68,0.2);
            flex-wrap: wrap;
            gap: 16px;
        ">
            <div style="display:flex; align-items:center; gap:20px;">
                <div style="font-size:52px;">❌</div>
                <div>
                    <div style="font-size:30px; font-weight:800; color:#ffffff;
                        letter-spacing:1px;">
                        CLAIM REJECTED
                    </div>
                    <div style="font-size:16px; color:#fca5a5; margin-top:6px;">
                        {rules_failed} rule(s) failed — See details below
                    </div>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px; color:#fca5a5; margin-bottom:4px;">
                    FAILED RULES
                </div>
                <div style="font-size:28px; font-weight:800; color:#ef4444;">
                    {rules_failed}/7
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── UPGRADE 6 — Metrics Row (4 cards) ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="✅ Rules Passed", value=f"{rules_passed} / 7")
    with col2:
        st.metric(label="❌ Rules Failed", value=f"{rules_failed} / 7")
    with col3:
        st.metric(label="🏷️ Decision", value=decision)
    with col4:
        st.metric(
            label="💰 Approved Amount",
            value=f"₹{approved_amount:,}" if decision == "APPROVED" else "₹0",
        )

    # ── UPGRADE 6 — Claim vs Coverage Bar ──
    coverage_pct = int((claim_amount / coverage_limit) * 100) if coverage_limit > 0 else 0
    if coverage_pct <= 80:
        bar_color = "#10b981"
    elif coverage_pct <= 100:
        bar_color = "#f59e0b"
    else:
        bar_color = "#ef4444"

    st.markdown(f"""
    <div style="background:#242938; border:1px solid #2d3548; border-radius:12px;
        padding:20px 24px; margin:20px 0;">
        <div style="display:flex; justify-content:space-between;
            margin-bottom:10px;">
            <span style="color:#94a3b8; font-size:13px; font-weight:600;">
                CLAIM VS COVERAGE
            </span>
            <span style="color:#f1f5f9; font-size:13px; font-weight:700;">
                ₹{claim_amount:,} of ₹{coverage_limit:,} ({coverage_pct}%)
            </span>
        </div>
        <div style="background:#1a1f2e; border-radius:50px; height:10px;
            overflow:hidden;">
            <div style="background:{bar_color}; width:{min(coverage_pct, 100)}%;
                height:100%; border-radius:50px;
                transition: width 0.5s ease;">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── UPGRADE 7 — Rules Table Header ──
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:space-between;
        margin:28px 0 14px;">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:20px;">📊</span>
            <span style="font-size:18px; font-weight:700; color:#f1f5f9;">
                Rules Evaluation Table
            </span>
        </div>
        <span style="background:#1e1b4b; color:#a5b4fc; padding:4px 14px;
            border-radius:50px; font-size:12px; font-weight:600;">
            7 Rules
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Rules Evaluation Table (logic preserved) ──
    df_data = []
    for name, cond, explanation in rules:
        status = "✅ Passed" if cond else "❌ Failed"
        df_data.append({"Rule Name": name, "Status": status, "Explanation": explanation})

    df = pd.DataFrame(df_data)

    def color_status(val):
        if "Passed" in val:
            return "background-color: #064e3b; color: #6ee7b7;"
        elif "Failed" in val:
            return "background-color: #450a0a; color: #fca5a5;"
        return ""

    # Use .map() for pandas ≥ 2.1.0; fall back to .applymap() for older versions
    try:
        styled_df = df.style.map(color_status, subset=["Status"])
    except AttributeError:
        styled_df = df.style.applymap(color_status, subset=["Status"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Facts Summary (preserved) ──
    with st.expander("📝 View Submitted Facts", expanded=False):
        fact_col1, fact_col2 = st.columns(2)
        with fact_col1:
            st.markdown(f"**Policy Active:** {facts['policy_active']}")
            st.markdown(f"**Policy Type:** {facts['policy_type']}")
            st.markdown(f"**Premium Paid:** {facts['premium_paid']}")
            st.markdown(f"**Accident Reported:** {facts['accident_reported']}")
            st.markdown(f"**Incident Within Coverage:** {facts['incident_within_coverage']}")
        with fact_col2:
            st.markdown(f"**Fraud Suspected:** {facts['fraud_suspected']}")
            st.markdown(f"**Documents Valid:** {facts['documents_valid']}")
            st.markdown(f"**Medical Records:** {facts['medical_records']}")
            st.markdown(f"**Claim Amount:** ₹{facts['claim_amount']:,}")
            st.markdown(f"**Coverage Limit:** ₹{facts['coverage_limit']:,}")

    # ── UPGRADE 8 — Inference Chain Steps ──
    with st.expander("🔗 View Logic Inference Chain", expanded=False):
        for step in inference_chain:
            if step.startswith("Final"):
                # Final inference step
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#1e1b4b,#2d1b69);
                    border:2px solid #6366f1; border-radius:12px; padding:18px 24px;
                    margin-top:8px; display:flex; align-items:center; gap:16px;">
                    <span style="font-size:24px;">⚖️</span>
                    <span style="color:#e0e7ff; font-size:15px; font-weight:700;">
                        {step}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Extract step number and determine pass/fail
                step_number = step.split(":")[0].replace("Step ", "").strip()
                is_pass = "TRUE" in step
                if is_pass:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#064e3b,#065f46);
                        border:1px solid #10b981; border-radius:10px; padding:14px 20px;
                        margin-bottom:10px; display:flex; align-items:center; gap:16px;">
                        <div style="background:#10b981; color:#fff; border-radius:50%;
                            width:28px; height:28px; display:flex; align-items:center;
                            justify-content:center; font-weight:700; font-size:13px;
                            flex-shrink:0;">
                            {step_number}
                        </div>
                        <div style="flex:1; color:#ecfdf5; font-size:14px; font-weight:500;">
                            {step}
                        </div>
                        <div style="color:#10b981; font-weight:700; font-size:14px;">TRUE</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);
                        border:1px solid #ef4444; border-radius:10px; padding:14px 20px;
                        margin-bottom:10px; display:flex; align-items:center; gap:16px;">
                        <div style="background:#ef4444; color:#fff; border-radius:50%;
                            width:28px; height:28px; display:flex; align-items:center;
                            justify-content:center; font-weight:700; font-size:13px;
                            flex-shrink:0;">
                            {step_number}
                        </div>
                        <div style="flex:1; color:#fecaca; font-size:14px; font-weight:500;">
                            {step}
                        </div>
                        <div style="color:#ef4444; font-weight:700; font-size:14px;">FALSE</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── UPGRADE 9 — Download Report ──
    st.markdown("<hr>", unsafe_allow_html=True)

    rules_report_lines = []
    for i, (rname, rcond, rexpl) in enumerate(rules):
        status_str = "PASSED ✓" if rcond else "FAILED ✗"
        rules_report_lines.append(f"  Rule {i+1} - {rname}: {status_str}")

    report_text = f"""
╔══════════════════════════════════════════════════════╗
║       INSURANCE CLAIM DECISION REPORT               ║
╚══════════════════════════════════════════════════════╝

Date & Time : {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}
Decision    : {decision}
Approved    : ₹{approved_amount:,}

──────────────────────────────────────
SUBMITTED FACTS
──────────────────────────────────────
  Policy Active            : {facts['policy_active']}
  Policy Type              : {facts['policy_type']}
  Premium Paid             : {facts['premium_paid']}
  Accident Reported        : {facts['accident_reported']}
  Within Coverage Period   : {facts['incident_within_coverage']}
  Fraud Suspected          : {facts['fraud_suspected']}
  Documents Valid          : {facts['documents_valid']}
  Medical Records          : {facts['medical_records']}
  Claim Amount             : ₹{facts['claim_amount']:,}
  Coverage Limit           : ₹{facts['coverage_limit']:,}

──────────────────────────────────────
RULES EVALUATION ({rules_passed}/7 Passed)
──────────────────────────────────────
{chr(10).join(rules_report_lines)}

──────────────────────────────────────
INFERENCE CHAIN
──────────────────────────────────────
{chr(10).join(['  ' + s for s in inference_chain])}

──────────────────────────────────────
FINAL DECISION: {decision}
──────────────────────────────────────
"""

    st.download_button(
        label="📥 Download Claim Report",
        data=report_text,
        file_name=f"claim_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center; color:#64748b; font-size:0.8rem; padding:1rem 0;">
        🛡️ ClaimAI — Insurance Decision System &nbsp;|&nbsp; Built with Streamlit &nbsp;|&nbsp; Rule-Based Propositional Logic Inference
    </div>
    """,
    unsafe_allow_html=True,
)
