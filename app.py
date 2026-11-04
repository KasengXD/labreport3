import json
import operator
from typing import List, Dict, Any, Tuple
import streamlit as st

# ----------------------------
# 1) Streamlit Page Configuration (MUST BE FIRST)
# ----------------------------
st.set_page_config(
    page_title="Scholarship Advisory Rule-Based System", 
    page_icon="🎓", 
    layout="wide"
)

# ----------------------------
# 2) Key Normalization & Engine Logic
# ----------------------------
OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

def normalize_key(k: str) -> str:
    """Normalize keys (lowercase, stripped, spaces to underscores) to fix JSON variations."""
    return str(k).lower().strip().replace(" ", "_")

# EXACT JSON Rules as specified in Lab Report Question 2
DEFAULT_RULES: List[Dict[str, Any]] = [
  {
    "name": "Top merit candidate",
    "priority": 100,
    "conditions": [
      ["cgpa", ">=", 3.7],
      ["co curricular score", ">=", 80],
      ["family income", "<=", 8000],
      ["disciplinary_actions", "==", 0]
    ],
    "action": {
      "decision": "AWARD FULL",
      "reason": "Excellent academic & co-curricular performance, with acceptable need"
    }
  },
  {
    "name": "Good candidate partial scholarship",
    "priority": 80,
    "conditions": [
      ["cgpa", ">=", 3.3],
      ["co_curricular score", ">=", 60],
      ["family_income", "<=", 12000],
      ["disciplinary_actions", "<=", 1]
    ],
    "action": {
      "decision": "AWARD PARTIAL",
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
    "name": "Low CGPA not eligible",
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
      ["disciplinary actions", ">=", 2]
    ],
    "action": {
      "decision": "REJECT",
      "reason": "Too many disciplinary records"
    }
  }
]

def evaluate_condition(facts: Dict[str, Any], cond: List[Any]) -> bool:
    """Evaluate a single condition [field, operator, target_value] with key normalization."""
    if len(cond) != 3:
        return False
    field, op, value = cond
    norm_field = normalize_key(field)
    norm_facts = {normalize_key(k): v for k, v in facts.items()}
    
    if norm_field not in norm_facts or op not in OPS:
        return False
    try:
        return OPS[op](norm_facts[norm_field], value)
    except Exception:
        return False

def rule_matches(facts: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    """Check if all conditions in a rule are met (AND logic)."""
    return all(evaluate_condition(facts, c) for c in rule.get("conditions", []))

def run_rules(facts: Dict[str, Any], rules: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Evaluates rules and returns (best_action, fired_rules) sorted by priority."""
    fired = [r for r in rules if rule_matches(facts, r)]
    if not fired:
        return ({"decision": "REVIEW", "reason": "No matching rule criteria met"}, [])

    fired_sorted = sorted(fired, key=lambda r: r.get("priority", 0), reverse=True)
    best = fired_sorted[0].get("action", {"decision": "REVIEW", "reason": "No action defined"})
    return best, fired_sorted

# ----------------------------
# 3) User Interface (Streamlit)
# ----------------------------
st.title("🎓 University Scholarship Advisory System")
st.caption("Transparent Decision Support Tool powered by Knowledge Representation System")

with st.sidebar:
    st.header("📋 Applicant Facts")
    cgpa = st.number_input("Cumulative GPA (CGPA)", min_value=0.0, max_value=4.0, step=0.01, value=3.75)
    family_income = st.number_input("Monthly Family Income (MYR)", min_value=0, step=100, value=5000)
    co_curricular_score = st.number_input("Co-curricular Score (0-100)", min_value=0, max_value=100, step=1, value=85)
    community_service_hours = st.number_input("Community Service Hours", min_value=0, step=1, value=20)
    current_semester = st.number_input("Current Semester of Study", min_value=1, max_value=12, step=1, value=3)
    disciplinary_actions = st.number_input("Disciplinary Actions on Record", min_value=0, step=1, value=0)

    st.divider()
    st.header("⚙️ Rule Configuration (JSON)")
    st.caption("Edit and fine-tune rules in JSON format below:")    
    default_json = json.dumps(DEFAULT_RULES, indent=2)
    rules_text = st.text_area("JSON Rule Base", value=default_json, height=320)

    run = st.button("Evaluate Application", type="primary")

facts = {
    "cgpa": float(cgpa),
    "family_income": float(family_income),
    "co_curricular_score": int(co_curricular_score),
    "community_service_hours": int(community_service_hours),
    "current_semester": int(current_semester),
    "disciplinary_actions": int(disciplinary_actions),
}

st.subheader("📌 Input Applicant Profile")
st.json(facts)

# Parse JSON Rules cleanly
try:
    rules = json.loads(rules_text)
    assert isinstance(rules, list), "Rules must be a JSON array"
except Exception as e:
    st.error(f"Invalid JSON structure in editor. Using default rules. Details: {e}")
    rules = DEFAULT_RULES

st.subheader("📜 Active Rules Engine")
with st.expander("View Active JSON Rules Configuration", expanded=False):
    st.code(json.dumps(rules, indent=2), language="json")

st.divider()

if run:
    action, fired = run_rules(facts, rules)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("🏆 Advisory Decision")
        badge = action.get("decision", "REVIEW")
        reason = action.get("reason", "-")
        
        if badge == "AWARD FULL":
            st.success(f"🟢 **AWARD FULL** — {reason}")
        elif badge == "AWARD PARTIAL":
            st.info(f"🔵 **AWARD PARTIAL** — {reason}")
        elif badge == "REJECT":
            st.error(f"🔴 **REJECT** — {reason}")
        else:
            st.warning(f"🟡 **REVIEW** — {reason}")

    with col2:
        st.subheader("🔥 Fired Rules (Ranked by Priority)")
        if not fired:
            st.info("No rule conditions matched this profile.")
        else:
            for i, r in enumerate(fired, start=1):
                st.write(f"**{i}. {r.get('name', '(unnamed)')}** | Priority: `{r.get('priority', 0)}`")
                st.caption(f"Action: {r.get('action', {})}")
                with st.expander("Evaluated Conditions"):
                    for cond in r.get("conditions", []):
                        st.code(str(cond))
else:
    st.info("Set applicant inputs on the sidebar and click **Evaluate Application**.")
