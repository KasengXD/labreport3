
import json
from typing import List, Dict, Any, Tuple
import operator
import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------
# 1) Minimal rule engine
# ----------------------------

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
}

# EXACTLY the five rules provided in the assignment
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
    },
]


def evaluate_condition(facts: Dict[str, Any], cond: List[Any]) -> bool:
    """Evaluate a single condition: [field, operator, value]."""

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
    """All conditions must be true (AND)."""

    return all(
        evaluate_condition(facts, condition)
        for condition in rule.get("conditions", [])
    )


def run_rules(
    facts: Dict[str, Any],
    rules: List[Dict[str, Any]]
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Returns (best_action, fired_rules).

    The highest-priority matched rule determines the final decision.
    If priorities are equal, the first encountered rule wins.
    """

    fired = [
        rule for rule in rules
        if rule_matches(facts, rule)
    ]

    if not fired:
        return (
            {
                "decision": "REVIEW",
                "reason": "No rule matched. Further assessment is required."
            },
            []
        )

    fired_sorted = sorted(
        fired,
        key=lambda rule: rule.get("priority", 0),
        reverse=True
    )

    best = fired_sorted[0].get(
        "action",
        {
            "decision": "REVIEW",
            "reason": "No action specified."
        }
    )

    return best, fired_sorted


# ----------------------------
# 2) Rule validation
# ----------------------------

def validate_rules(rules: Any) -> None:
    """Check whether the JSON rules have a valid structure."""

    if not isinstance(rules, list):
        raise ValueError("Rules must be a JSON array.")

    for index, rule in enumerate(rules):

        if not isinstance(rule, dict):
            raise ValueError(f"Rule {index + 1} must be an object.")

        if not isinstance(rule.get("name"), str):
            raise ValueError(f"Rule {index + 1} needs a valid name.")

        if not isinstance(rule.get("priority"), (int, float)):
            raise ValueError(f"Rule {index + 1} needs a numeric priority.")

        if not isinstance(rule.get("conditions"), list):
            raise ValueError(f"Rule {index + 1} needs a conditions list.")

        if not rule["conditions"]:
            raise ValueError(f"Rule {index + 1} must have at least one condition.")

        for condition in rule["conditions"]:

            if not isinstance(condition, list) or len(condition) != 3:
                raise ValueError(
                    f"Rule {index + 1} contains an invalid condition."
                )

            field, op, value = condition

            allowed_fields = [
                "cgpa",
                "family_income",
                "co_curricular_score",
                "community_service_hours",
                "current_semester",
                "disciplinary_actions"
            ]

            if field not in allowed_fields:
                raise ValueError(
                    f"Rule {index + 1} contains an unknown field: {field}"
                )

            if op not in OPS:
                raise ValueError(
                    f"Rule {index + 1} contains an invalid operator: {op}"
                )

        action = rule.get("action")

        if not isinstance(action, dict):
            raise ValueError(f"Rule {index + 1} needs a valid action.")

        if not action.get("decision"):
            raise ValueError(f"Rule {index + 1} needs a decision.")

        if not action.get("reason"):
            raise ValueError(f"Rule {index + 1} needs a reason.")


# ----------------------------
# 3) Streamlit page settings
# ----------------------------

st.set_page_config(
    page_title="Scholarship Advisory System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 Scholarship Advisory System")

st.caption(
    "A Rule-Based Knowledge Representation System "
    "for University Scholarship Eligibility Assessment."
)

st.markdown("""
This application evaluates scholarship applicants using predefined
IF–THEN rules. The system considers academic performance, financial
background, co-curricular involvement and disciplinary records
to generate a scholarship recommendation.
""")

# ----------------------------
# 4) Sidebar: Applicant Facts
# ----------------------------

with st.sidebar:

    st.header("👤 Applicant Information")

    st.write("Enter the applicant's details below.")

    cgpa = st.number_input(
        "Cumulative GPA (CGPA)",
        min_value=0.0,
        max_value=4.0,
        step=0.01,
        value=3.50,
        format="%.2f"
    )

    family_income = st.number_input(
        "Monthly Family Income (MYR)",
        min_value=0.0,
        step=100.0,
        value=5000.0
    )

    co_curricular_score = st.number_input(
        "Co-curricular Involvement Score",
        min_value=0,
        max_value=100,
        step=1,
        value=75
    )

    community_service_hours = st.number_input(
        "Community Service Hours",
        min_value=0,
        step=1,
        value=30
    )

    current_semester = st.number_input(
        "Current Semester of Study",
        min_value=1,
        step=1,
        value=3
    )

    disciplinary_actions = st.number_input(
        "Number of Disciplinary Actions",
        min_value=0,
        step=1,
        value=0
    )

    st.divider()

    st.header("⚙️ Evaluation Settings")

    evaluate_button = st.button(
        "Evaluate Applicant",
        type="primary",
        use_container_width=True
    )

    reset_button = st.button(
        "Reset Applicant",
        use_container_width=True
    )

    if reset_button:
        st.rerun()


# ----------------------------
# 5) Collect Applicant Facts
# ----------------------------

facts = {
    "cgpa": float(cgpa),
    "family_income": float(family_income),
    "co_curricular_score": int(co_curricular_score),
    "community_service_hours": int(community_service_hours),
    "current_semester": int(current_semester),
    "disciplinary_actions": int(disciplinary_actions)
}


# ----------------------------
# 6) JSON Rule Editor
# ----------------------------

st.subheader("📋 Knowledge Base: Rule Configuration")

st.write(
    "The following JSON editor allows the scholarship committee "
    "to view and modify the decision rules."
)

if "rules_text" not in st.session_state:
    st.session_state.rules_text = json.dumps(
        DEFAULT_RULES,
        indent=4
    )

if "evaluation_result" not in st.session_state:
    st.session_state.evaluation_result = None

with st.expander("View and Edit Scholarship Rules (JSON)", expanded=False):

    rules_text = st.text_area(
        "Edit rules here",
        key="rules_text",
        height=450
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Restore Default Rules"):
            st.session_state.rules_text = json.dumps(
                DEFAULT_RULES,
                indent=4
            )
            st.rerun()

    with col2:
        st.download_button(
            "Download Rules (JSON)",
            data=st.session_state.rules_text,
            file_name="scholarship_rules.json",
            mime="application/json"
        )


# ----------------------------
# 7) Applicant Facts Display
# ----------------------------

st.divider()

st.subheader("📊 Applicant Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CGPA", f"{cgpa:.2f} / 4.00")

with col2:
    st.metric("Family Income", f"MYR {family_income:,.2f}")

with col3:
    st.metric("Co-curricular Score", f"{co_curricular_score} / 100")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Community Service", f"{community_service_hours} hours")

with col5:
    st.metric("Current Semester", current_semester)

with col6:
    st.metric("Disciplinary Actions", disciplinary_actions)


# ----------------------------
# 8) Parse and Validate Rules
# ----------------------------

try:

    rules = json.loads(st.session_state.rules_text)

    validate_rules(rules)

    rules_valid = True

except (json.JSONDecodeError, ValueError, TypeError) as e:

    st.error(f"Invalid rules configuration: {e}")

    st.warning(
        "Please correct the JSON rules before evaluating the applicant."
    )

    rules_valid = False
    rules = []


# ----------------------------
# 9) Evaluate Scholarship Applicant
# ----------------------------

if evaluate_button:

    if rules_valid:

        action, fired = run_rules(facts, rules)

        st.session_state.evaluation_result = {
            "facts": facts.copy(),
            "action": action,
            "fired": fired,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    else:

        st.session_state.evaluation_result = None


# ----------------------------
# 10) Display Evaluation Results
# ----------------------------

result = st.session_state.evaluation_result

if result is not None:

    st.divider()

    st.subheader("🎯 Scholarship Evaluation Result")

    action = result["action"]
    fired = result["fired"]

    decision = action.get("decision", "REVIEW")
    reason = action.get("reason", "-")

    # Decision display

    if decision == "AWARD_FULL":

        st.success("🏆 FULL SCHOLARSHIP AWARDED")

    elif decision == "AWARD_PARTIAL":

        st.success("🥈 PARTIAL SCHOLARSHIP AWARDED")

    elif decision == "REJECT":

        st.error("❌ SCHOLARSHIP APPLICATION REJECTED")

    else:

        st.warning("⚠️ MANUAL REVIEW REQUIRED")

    result_col1, result_col2 = st.columns([1, 1])

    with result_col1:

        st.markdown("### Final Decision")

        st.subheader(decision)

        st.write("**Reason for Decision:**")

        st.info(reason)

    with result_col2:

        st.markdown("### Decision Information")

        st.write(
            f"**Matched Rules:** {len(fired)}"
        )

        if fired:

            st.write(
                f"**Highest Priority:** {fired[0].get('priority', 0)}"
            )

            st.write(
                f"**Selected Rule:** {fired[0].get('name', '-')}"
            )

        else:

            st.write("**Selected Rule:** No matching rule")

        st.write(
            f"**Evaluation Time:** {result['timestamp']}"
        )

    # ----------------------------
    # 11) Matched Rules
    # ----------------------------

    st.divider()

    st.subheader("📌 Matched Rules (Sorted by Priority)")

    if not fired:

        st.info(
            "No predefined rules matched this applicant. "
            "The application requires further assessment."
        )

    else:

        for index, rule in enumerate(fired, start=1):

            with st.expander(
                f"{index}. {rule.get('name', 'Unnamed Rule')} "
                f"| Priority: {rule.get('priority', 0)}",
                expanded=(index == 1)
            ):

                st.write(
                    f"**Decision:** {rule.get('action', {}).get('decision', '-')}"
                )

                st.write(
                    f"**Reason:** {rule.get('action', {}).get('reason', '-')}"
                )

                st.write("**Conditions:**")

                for condition in rule.get("conditions", []):

                    field, op, value = condition

                    actual_value = facts[field]

                    matched = evaluate_condition(facts, condition)

                    if matched:
                        st.success(
                            f"{field}: {actual_value} {op} {value} ✓"
                        )
                    else:
                        st.error(
                            f"{field}: {actual_value} {op} {value} ✗"
                        )

    # ----------------------------
    # 12) Evaluation Summary
    # ----------------------------

    st.divider()

    st.subheader("📑 Evaluation Summary")

    summary_data = {
        "Applicant Information": [
            "CGPA",
            "Monthly Family Income (MYR)",
            "Co-curricular Score",
            "Community Service Hours",
            "Current Semester",
            "Disciplinary Actions"
        ],
        "Applicant Values": [
            facts["cgpa"],
            facts["family_income"],
            facts["co_curricular_score"],
            facts["community_service_hours"],
            facts["current_semester"],
            facts["disciplinary_actions"]
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    # ----------------------------
    # 13) Download Evaluation Report
    # ----------------------------

    report = {
        "evaluation_time": result["timestamp"],
        "applicant_facts": facts,
        "final_decision": decision,
        "reason": reason,
        "selected_rule": (
            fired[0]["name"] if fired else "No matching rule"
        ),
        "matched_rules": [
            {
                "name": rule.get("name"),
                "priority": rule.get("priority"),
                "action": rule.get("action")
            }
            for rule in fired
        ]
    }

    report_json = json.dumps(
        report,
        indent=4
    )

    st.download_button(
        label="📥 Download Evaluation Report (JSON)",
        data=report_json,
        file_name="scholarship_evaluation_report.json",
        mime="application/json",
        use_container_width=True
    )

else:

    st.divider()

    st.info(
        "Enter the applicant's information in the sidebar "
        "and click **Evaluate Applicant** to generate a scholarship decision."
    )


# ----------------------------
# 14) Footer
# ----------------------------

st.divider()

st.caption(
    "Scholarship Advisory System | "
    "Artificial Intelligence Lab Report 3 | "
    "Knowledge Representation System"
)

st.caption(
    "Note: This application provides decision support based on "
    "predefined rules. Final scholarship approval remains subject "
    "to the university scholarship committee."
)
