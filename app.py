
import json
from typing import List, Dict, Any, Tuple
import operator
import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. OPERATOR DEFINITIONS
# --------------------------------------------------

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b
}

# --------------------------------------------------
# 2. DEFAULT SCHOLARSHIP RULES
# --------------------------------------------------

DEFAULT_RULES: List[Dict[str, Any]] = [
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]

# --------------------------------------------------
# 3. RULE EVALUATION FUNCTIONS
# --------------------------------------------------

def evaluate_condition(facts: Dict[str, Any], cond: List[Any]) -> bool:
    if len(cond) != 3:
        return False

    field, op, value = cond

    if field not in facts or op not in OPS:
        return False

    try:
        return OPS[op](facts[field], value)
    except Exception:
        return False


def rule_matches(facts: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    return all(
        evaluate_condition(facts, condition)
        for condition in rule["conditions"]
    )


def run_rules(
    facts: Dict[str, Any],
    rules: List[Dict[str, Any]]
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:

    fired = [
        rule for rule in rules
        if rule_matches(facts, rule)
    ]

    if not fired:
        return {
            "decision": "REVIEW",
            "reason": "No rule matched"
        }, []

    fired_sorted = sorted(
        fired,
        key=lambda rule: rule["priority"],
        reverse=True
    )

    return fired_sorted[0]["action"], fired_sorted


# --------------------------------------------------
# 4. RULE VALIDATION
# --------------------------------------------------

def validate_rules(rules: Any) -> Tuple[bool, str]:

    if not isinstance(rules, list):
        return False, "Rules must be a JSON list."

    allowed_fields = [
        "cgpa",
        "family_income",
        "co_curricular_score",
        "community_service_hours",
        "current_semester",
        "disciplinary_actions"
    ]

    for rule in rules:

        if not isinstance(rule, dict):
            return False, "Each rule must be a JSON object."

        required_keys = [
            "name",
            "priority",
            "conditions",
            "action"
        ]

        if not all(key in rule for key in required_keys):
            return False, "A rule is missing required fields."

        if not isinstance(rule["conditions"], list):
            return False, "Rule conditions must be a list."

        for condition in rule["conditions"]:

            if not isinstance(condition, list) or len(condition) != 3:
                return False, "Each condition must contain field, operator and value."

            field, op, value = condition

            if field not in allowed_fields:
                return False, f"Invalid field: {field}"

            if op not in OPS:
                return False, f"Invalid operator: {op}"

        if not isinstance(rule["action"], dict):
            return False, "Rule action must be a JSON object."

        if "decision" not in rule["action"] or "reason" not in rule["action"]:
            return False, "Action must contain decision and reason."

    return True, "Rules are valid."


# --------------------------------------------------
# 5. STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Scholarship Advisory System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Scholarship Advisory System")
st.write("A Rule-Based System for University Scholarship Evaluation")

st.divider()

# --------------------------------------------------
# 6. SIDEBAR - APPLICANT INFORMATION
# --------------------------------------------------

st.sidebar.header("Applicant Information")

cgpa = st.sidebar.number_input(
    "CGPA",
    min_value=0.0,
    max_value=4.0,
    value=3.50,
    step=0.01
)

family_income = st.sidebar.number_input(
    "Monthly Family Income (RM)",
    min_value=0,
    value=5000,
    step=100
)

co_curricular_score = st.sidebar.slider(
    "Co-curricular Score",
    min_value=0,
    max_value=100,
    value=70
)

community_service_hours = st.sidebar.number_input(
    "Community Service Hours",
    min_value=0,
    value=20,
    step=1
)

current_semester = st.sidebar.number_input(
    "Current Semester",
    min_value=1,
    value=3,
    step=1
)

disciplinary_actions = st.sidebar.number_input(
    "Number of Disciplinary Actions",
    min_value=0,
    value=0,
    step=1
)

facts = {
    "cgpa": cgpa,
    "family_income": family_income,
    "co_curricular_score": co_curricular_score,
    "community_service_hours": community_service_hours,
    "current_semester": current_semester,
    "disciplinary_actions": disciplinary_actions
}

# --------------------------------------------------
# 7. JSON RULE EDITOR
# --------------------------------------------------

st.sidebar.divider()
st.sidebar.header("Scholarship Rules")

if "rules_json" not in st.session_state:
    st.session_state.rules_json = json.dumps(
        DEFAULT_RULES,
        indent=4,
        ensure_ascii=False
    )

rules_text = st.sidebar.text_area(
    "Edit Rules (JSON)",
    value=st.session_state.rules_json,
    height=400
)

# --------------------------------------------------
# 8. MAIN PAGE - APPLICANT PROFILE
# --------------------------------------------------

st.subheader("Applicant Profile")

col1, col2, col3 = st.columns(3)

col1.metric("CGPA", f"{cgpa:.2f} / 4.00")
col2.metric("Family Income", f"RM {family_income:,.2f}")
col3.metric("Co-curricular Score", f"{co_curricular_score} / 100")

col4, col5, col6 = st.columns(3)

col4.metric("Community Service", f"{community_service_hours} hours")
col5.metric("Current Semester", current_semester)
col6.metric("Disciplinary Actions", disciplinary_actions)

st.divider()

# --------------------------------------------------
# 9. EVALUATE SCHOLARSHIP APPLICATION
# --------------------------------------------------

st.subheader("Scholarship Evaluation")

if st.button("Evaluate Application", type="primary"):

    try:
        rules = json.loads(rules_text)

        valid, message = validate_rules(rules)

        if not valid:
            st.error(message)

        else:
            st.session_state.rules_json = json.dumps(
                rules,
                indent=4,
                ensure_ascii=False
            )

            result, fired_rules = run_rules(facts, rules)

            st.session_state.evaluation_result = result
            st.session_state.fired_rules = fired_rules
            st.session_state.evaluated_facts = facts

    except json.JSONDecodeError as error:
        st.error(f"Invalid JSON format: {error}")

# --------------------------------------------------
# 10. DISPLAY EVALUATION RESULT
# --------------------------------------------------

if "evaluation_result" in st.session_state:

    result = st.session_state.evaluation_result
    fired_rules = st.session_state.fired_rules

    st.subheader("Evaluation Result")

    decision = result["decision"]
    reason = result["reason"]

    if decision == "AWARD_FULL":
        st.success("Decision: FULL SCHOLARSHIP")

    elif decision == "AWARD_PARTIAL":
        st.success("Decision: PARTIAL SCHOLARSHIP")

    elif decision == "REJECT":
        st.error("Decision: REJECTED")

    else:
        st.warning("Decision: FURTHER REVIEW REQUIRED")

    st.write("**Decision Code:**", decision)
    st.write("**Reason:**", reason)

    st.divider()

    # Matched Rules
    st.subheader("Matched Rules")

    if fired_rules:

        for rule in fired_rules:

            with st.expander(
                f"{rule['name']} (Priority: {rule['priority']})"
            ):

                st.write("**Conditions:**")

                for condition in rule["conditions"]:

                    field, op, value = condition

                    matched = evaluate_condition(
                        st.session_state.evaluated_facts,
                        condition
                    )

                    status = "Matched" if matched else "Not Matched"

                    st.write(
                        f"{field} {op} {value} — {status}"
                    )

                st.write(
                    "**Decision:**",
                    rule["action"]["decision"]
                )

                st.write(
                    "**Reason:**",
                    rule["action"]["reason"]
                )

    else:
        st.info("No predefined rule matched the applicant.")

    # Evaluation Summary
    st.subheader("Evaluation Summary")

    summary_data = {
        "Applicant Information": [
            "CGPA",
            "Monthly Family Income",
            "Co-curricular Score",
            "Community Service Hours",
            "Current Semester",
            "Disciplinary Actions"
        ],
        "Value": [
            st.session_state.evaluated_facts["cgpa"],
            f"RM {st.session_state.evaluated_facts['family_income']:,.2f}",
            st.session_state.evaluated_facts["co_curricular_score"],
            st.session_state.evaluated_facts["community_service_hours"],
            st.session_state.evaluated_facts["current_semester"],
            st.session_state.evaluated_facts["disciplinary_actions"]
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    # Download Report
    report = {
        "applicant_information": st.session_state.evaluated_facts,
        "final_decision": result,
        "matched_rules": fired_rules
    }

    st.download_button(
        label="Download Evaluation Report (JSON)",
        data=json.dumps(report, indent=4, ensure_ascii=False),
        file_name="scholarship_evaluation_report.json",
        mime="application/json"
    )

# --------------------------------------------------
# 11. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Scholarship Advisory System | Artificial Intelligence Lab Report 3"
)

st.caption(
    "This system provides recommendations based on predefined rules. "
    "Final scholarship approval remains the responsibility of the scholarship committee."
)
