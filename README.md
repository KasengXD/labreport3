# 🎓# Scholarship Advisory System

## 1. Project Description

This project is a Rule-Based Scholarship Advisory System developed using Python and Streamlit for the Artificial Intelligence Lab Report 3 assignment.

The system evaluates university scholarship applicants based on their academic performance, family income, co-curricular involvement and disciplinary records. It uses predefined IF–THEN rules to determine scholarship eligibility and provide a recommendation.

## 2. Objectives

- To develop a rule-based system for scholarship eligibility assessment.
- To apply IF–THEN rules for decision-making.
- To implement a rule engine using Python.
- To develop a simple interactive application using Streamlit.

## 3. Technologies Used

- Python
- Streamlit
- Pandas
- JSON

## 4. Applicant Information

The system collects the following information:

1. Cumulative GPA (CGPA)
2. Monthly family income
3. Co-curricular involvement score
4. Community service hours
5. Current semester
6. Number of disciplinary actions

## 5. Scholarship Decisions

The system uses five predefined rules to evaluate applicants.

| Decision | Description |
|---|---|
| AWARD_FULL | Full scholarship |
| AWARD_PARTIAL | Partial scholarship |
| REVIEW | Further assessment required |
| REJECT | Not eligible for scholarship |

When multiple rules are matched, the system selects the rule with the highest priority.

## 6. Application Features

- Enter applicant information.
- View applicant details.
- Edit scholarship rules using JSON.
- Evaluate scholarship eligibility.
- Display matched rules according to priority.
- Display the final decision and reason.
- Download the evaluation report in JSON format.

## 7. Project Structure

```text
Scholarship-Advisory-System/
│
├── app.py
├── requirements.txt
└── README.md
```

## 8. Installation and Execution

**Step 1: Install the required libraries.**

```bash
pip install streamlit pandas
```

**Step 2: Run the application.**

```bash
streamlit run app.py
```

**Step 3: Open the application in your browser.**

```text
http://localhost:8501
```

## 9. Author

- **Name:** [WONG KA SENG]
- **Student ID:** [SD24037]
- **Subject:** BSD2513 – Introduction to Artificial Intelligence
- **Lab:** Lab Report 3 – Knowledge Representation System
---

## 10. Link

https://labreport3-sd24037.streamlit.app/

*This project was developed for academic purposes as part of the Artificial Intelligence laboratory assignment.*
