# 🎓 Scholarship Advisory System
### Artificial Intelligence Lab Report 3 – Knowledge Representation System

## 1. Project Overview

The Scholarship Advisory System is a web-based application developed using Python and Streamlit. It applies a Rule-Based System (RBS) to assist a university scholarship committee in evaluating applicants and determining their scholarship eligibility.

The system uses predefined IF–THEN rules to evaluate applicant information, including Cumulative Grade Point Average (CGPA), monthly family income, co-curricular involvement score and disciplinary records.

Based on the conditions satisfied by an applicant, the system generates one of four possible decisions:

- **AWARD_FULL** – Full scholarship awarded.
- **AWARD_PARTIAL** – Partial scholarship awarded.
- **REVIEW** – Further manual assessment required.
- **REJECT** – Scholarship application rejected.

The application also provides an editable JSON rule configuration, allowing the scholarship committee to review and modify decision rules when necessary.

## 2. Project Objectives

The main objectives of this project are:

- To develop a rule-based system for university scholarship eligibility assessment.
- To represent knowledge using predefined IF–THEN rules.
- To implement a rule engine that evaluates applicant information against multiple conditions.
- To apply priority-based decision-making when multiple rules are matched.
- To develop an interactive web application using Streamlit.
- To provide transparent and understandable scholarship recommendations.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application development |
| Pandas | Displaying applicant evaluation information |
| JSON | Knowledge representation and rule configuration |
| Operator | Evaluating logical comparison conditions |

## 4. Applicant Information

The system collects six types of information from scholarship applicants.

| Applicant Information | Description |
|---|---|
| CGPA | Applicant's cumulative grade point average (0.00–4.00) |
| Family Income | Monthly family income in MYR |
| Co-curricular Score | Applicant's co-curricular involvement score (0–100) |
| Community Service Hours | Total community service hours |
| Current Semester | Applicant's current semester of study |
| Disciplinary Actions | Number of disciplinary actions recorded |

All six fields are collected and displayed in the applicant profile. The scholarship decisions are evaluated using the conditions defined in the five prescribed rules.

## 5. Rule-Based Knowledge Representation

The application uses IF–THEN rules to represent scholarship eligibility knowledge.

Each rule consists of three main components:

- **Name:** Identifies the scholarship eligibility rule.
- **Priority:** Determines which matched rule takes precedence.
- **Conditions:** Specifies the requirements that an applicant must satisfy.
- **Action:** Defines the scholarship decision and its explanation.

The system implements five predefined scholarship rules:

| Rule Name | Priority | Decision |
|---|---:|---|
| Top merit candidate | 100 | AWARD_FULL |
| Good candidate - partial scholarship | 80 | AWARD_PARTIAL |
| Need-based review | 70 | REVIEW |
| Low CGPA – not eligible | 95 | REJECT |
| Serious disciplinary record | 90 | REJECT |

**Rule Evaluation Process**

1. The applicant enters their information.
2. The system retrieves the configured rules from the JSON editor.
3. Each rule is evaluated against the applicant's information.
4. All conditions within a rule must be satisfied for that rule to match (AND logic).
5. The system collects all matched rules.
6. Matched rules are sorted according to priority in descending order.
7. The highest-priority matched rule determines the final scholarship decision.
8. If no rule matches, the system returns REVIEW.

The five scholarship rules follow the original conditions and priorities provided in the laboratory assignment.

## 6. Application Features

### 6.1 Applicant Information Input
Users can enter applicant information through the Streamlit sidebar.

### 6.2 JSON Rule Editor
The application provides an editable JSON editor where users can view and modify the scholarship decision rules. Users can also restore the original default rules and download the JSON configuration.

### 6.3 Applicant Profile Dashboard
Displays the applicant's information using metric cards, including CGPA, monthly family income, co-curricular score, community service hours, current semester and disciplinary actions.

### 6.4 Scholarship Decision
Displays the final scholarship recommendation using status indicators:

- Green: Full or partial scholarship awarded.
- Yellow: Manual review required.
- Red: Application rejected.

### 6.5 Matched Rules
Displays all matched rules in descending priority order, including their names, priorities, decisions, reasons and evaluated conditions.

### 6.6 Evaluation Summary
Provides a structured summary of applicant information and the final evaluation result.

### 6.7 Download Evaluation Report
Allows users to download the evaluation results in JSON format for record-keeping and further review.

## 7. Project Structure

```text
Scholarship-Advisory-System/
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

## 8. Installation and Setup

### Prerequisites

- Python 3.9 or above
- Visual Studio Code or another Python IDE
- Internet connection for installing dependencies

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/Scholarship-Advisory-System.git
```

### Step 2: Navigate to the Project Folder

```bash
cd Scholarship-Advisory-System
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively, install the libraries directly:

```bash
pip install streamlit pandas
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

### Step 5: Access the Application

Open the following URL in your web browser:

```text
http://localhost:8501
```

## 9. Requirements

The project requires the following Python libraries:

```text
streamlit
pandas
```

## 10. Deployment

The application can be deployed using Streamlit Community Cloud.

Deployment steps:

1. Upload `app.py`, `requirements.txt` and `README.md` to a GitHub repository.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account.
4. Select the Scholarship Advisory System repository.
5. Choose `app.py` as the main application file.
6. Click Deploy.

After deployment, Streamlit Community Cloud will generate a public URL that can be shared with users.

## 11. Limitations

- Scholarship decisions depend on the predefined rules configured in the system.
- The system does not use machine learning or automatically learn from previous scholarship applications.
- Community service hours and current semester are collected but are not included in the five prescribed scholarship decision rules.
- Applicants who do not match any predefined rule are assigned a REVIEW decision.
- The generated results are recommendations and should be reviewed by the university scholarship committee before final approval.

## 12. Future Improvements

Possible improvements include:

- Adding applicant registration and authentication.
- Integrating a database to store applicant records.
- Generating downloadable PDF evaluation reports.
- Adding an administrator dashboard for managing scholarship applications.
- Supporting additional scholarship categories and configurable eligibility rules.

## 13. Author

**Name:** [WONG KA SENG]  
**Student ID:** [SD24037]  
**Subject:** BSD2513 – Introduction to Artificial Intelligence  
**Laboratory:** Lab Report 3 – Knowledge Representation System  
**Topic:** Rule-Based System

---

*This project was developed for academic purposes as part of the Artificial Intelligence laboratory assignment.*
