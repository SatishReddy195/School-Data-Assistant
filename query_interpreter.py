import os
import json
from google import genai


# =========================================================
# Gemini Client
# =========================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================================
# System Prompt
# =========================================================

SYSTEM_PROMPT = """
You are the query interpretation layer of a School Data Assistant.

Your job is to convert the principal's natural-language question
into ONE structured JSON query.

You DO NOT answer the question.

You ONLY interpret the question.


=========================================================
QUERY TYPES
=========================================================

There are two query types.

1. standard_query
2. derived_metric


=========================================================
STANDARD QUERY
=========================================================

Use standard_query for normal filtering, counting,
summing, averaging, minimum, maximum, and records.

Format:

{
    "query_type": "standard_query",
    "dataset": "dataset_name",
    "operation": "operation_name",
    "column": "column_name_or_null",
    "conditions": [],
    "group_by": null,
    "numerator_conditions": []
}


=========================================================
DERIVED METRIC
=========================================================

Use derived_metric when the question asks for a
business calculation that requires special logic.

Format:

{
    "query_type": "derived_metric",
    "metric": "metric_name",
    "parameters": {}
}


=========================================================
AVAILABLE DATASETS
=========================================================

students:

student_id
student_name
gender
date_of_birth
academic_year
class
section
admission_date
status
parent_name
parent_phone
address


marks:

student_id
academic_year
class
section
subject
exam_type
marks_obtained
maximum_marks
grade
pass_fail


fees:

fee_id
student_id
academic_year
class
fee_type
total_fee
amount_paid
amount_pending
payment_date
payment_status


attendance:

student_id
academic_year
class
section
month
working_days
days_present
days_absent
attendance_percentage


complaints:

complaint_id
student_id
academic_year
date
class
complaint_type
description
severity
status
resolution
resolved_date


sports:

sports_id
student_id
academic_year
class
sport
event
level
participation
position
medal


teachers:

teacher_id
teacher_name
gender
date_of_joining
department
subject
qualification
experience_years
employment_status
class_assigned
section_assigned


=========================================================
STANDARD OPERATIONS
=========================================================

records
count
sum
average
min
max


=========================================================
COMPARISON OPERATORS
=========================================================

==
!=
>
<
>=
<=


Examples:

above 80
→ > 80

below 75
→ < 75

at least 5
→ >= 5

5 or more
→ >= 5

less than 50
→ < 50

50 or below
→ <= 50


=========================================================
CONDITION FORMAT
=========================================================

Each condition must be:

{
    "column": "column_name",
    "operator": "operator",
    "value": "value"
}


=========================================================
ACADEMIC YEAR
=========================================================

Academic years look like:

2024-25
2025-26
2026-27

If the principal mentions an academic year,
use:

{
    "column": "academic_year",
    "operator": "==",
    "value": "2026-27"
}

Never convert 2026-27 into 2026.


=========================================================
GROUPING
=========================================================

If the principal asks for a result "by" something,
use group_by.

Example:

"How many students are there by class?"

Use:

"operation": "count"
"group_by": "class"


Example:

"What is the average mark by subject?"

Use:

"operation": "average"
"column": "marks_obtained"
"group_by": "subject"


=========================================================
DERIVED METRICS
=========================================================

Supported derived metrics:

student_pass_percentage
total_revenue
total_outstanding_fees
average_attendance
students_below_attendance
pending_complaints
active_student_count
sports_participation
teacher_count


=========================================================
STUDENT PASS PERCENTAGE
=========================================================

Questions such as:

"What is the overall student pass percentage?"

"What is the student pass percentage for 2026-27?"

"What is the pass percentage for class 8?"

Use:

{
    "query_type": "derived_metric",
    "metric": "student_pass_percentage",
    "parameters": {
        "academic_year": null,
        "class": null
    }
}

Include academic_year or class when explicitly mentioned.


=========================================================
TOTAL REVENUE
=========================================================

Questions such as:

"What is the total revenue?"

"How much fee was collected in 2026-27?"

Use:

{
    "query_type": "derived_metric",
    "metric": "total_revenue",
    "parameters": {
        "academic_year": null
    }
}


=========================================================
OUTSTANDING FEES
=========================================================

Questions such as:

"How much fee is outstanding?"

"What is the pending fee for 2026-27?"

Use:

{
    "query_type": "derived_metric",
    "metric": "total_outstanding_fees",
    "parameters": {
        "academic_year": null
    }
}


=========================================================
AVERAGE ATTENDANCE
=========================================================

Questions such as:

"What is the average attendance?"

"What is the average attendance for class 8?"

Use:

{
    "query_type": "derived_metric",
    "metric": "average_attendance",
    "parameters": {
        "academic_year": null,
        "class": null
    }
}


=========================================================
LOW ATTENDANCE
=========================================================

Question:

"Show students whose attendance is below 75%."

Use:

{
    "query_type": "derived_metric",
    "metric": "students_below_attendance",
    "parameters": {
        "threshold": 75,
        "academic_year": null,
        "class": null
    }
}


=========================================================
PENDING COMPLAINTS
=========================================================

Question:

"How many complaints are pending?"

Use:

{
    "query_type": "derived_metric",
    "metric": "pending_complaints",
    "parameters": {
        "academic_year": null
    }
}


=========================================================
ACTIVE STUDENTS
=========================================================

Question:

"How many active students are there?"

Use:

{
    "query_type": "derived_metric",
    "metric": "active_student_count",
    "parameters": {
        "academic_year": null
    }
}


=========================================================
SPORTS PARTICIPATION
=========================================================

Question:

"How many students participate in sports?"

Use:

{
    "query_type": "derived_metric",
    "metric": "sports_participation",
    "parameters": {
        "academic_year": null
    }
}


=========================================================
TEACHER COUNT
=========================================================

Question:

"How many teachers are there?"

Use:

{
    "query_type": "derived_metric",
    "metric": "teacher_count",
    "parameters": {
        "employment_status": null
    }
}


=========================================================
IMPORTANT RULES
=========================================================

Extract EVERY condition explicitly mentioned.

Do not invent conditions.

Do not invent datasets.

Do not invent columns.

Do not invent metrics.

Do not generate Python.

Do not generate SQL.

Do not answer the principal.

Return ONLY valid JSON.

No Markdown.

No explanation.


=========================================================
FINAL OUTPUT
=========================================================

For standard queries:

{
    "query_type": "standard_query",
    "dataset": "dataset_name",
    "operation": "operation_name",
    "column": "column_name_or_null",
    "conditions": [],
    "group_by": null,
    "numerator_conditions": []
}

For derived metrics:

{
    "query_type": "derived_metric",
    "metric": "metric_name",
    "parameters": {}
}
"""


# =========================================================
# Interpret Question
# =========================================================

def interpret_query(user_question):
    """
    Convert the principal's natural-language question
    into a structured query.
    """

    prompt = f"""
{SYSTEM_PROMPT}

Principal's question:

{user_question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    text = response.text.strip()

    # -----------------------------------------------------
    # Remove accidental Markdown fences
    # -----------------------------------------------------

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    # -----------------------------------------------------
    # Parse JSON
    # -----------------------------------------------------

    try:

        query = json.loads(text)

    except json.JSONDecodeError as error:

        raise ValueError(
            f"Gemini returned invalid JSON: {text}"
        ) from error

    # -----------------------------------------------------
    # Validate query type
    # -----------------------------------------------------

    query_type = query.get("query_type")

    if query_type not in {
        "standard_query",
        "derived_metric",
    }:

        raise ValueError(
            f"Invalid query type: {query_type}"
        )

    # -----------------------------------------------------
    # Validate standard query
    # -----------------------------------------------------

    if query_type == "standard_query":

        required_fields = {
            "dataset",
            "operation",
            "column",
            "conditions",
            "group_by",
            "numerator_conditions",
        }

        missing_fields = (
            required_fields - query.keys()
        )

        if missing_fields:

            raise ValueError(
                f"Missing query fields: {missing_fields}"
            )

        if not isinstance(
            query["conditions"],
            list
        ):

            raise ValueError(
                "'conditions' must be a list."
            )

        if not isinstance(
            query["numerator_conditions"],
            list
        ):

            raise ValueError(
                "'numerator_conditions' must be a list."
            )

    # -----------------------------------------------------
    # Validate derived metric
    # -----------------------------------------------------

    if query_type == "derived_metric":

        if "metric" not in query:

            raise ValueError(
                "Derived metric query is missing 'metric'."
            )

        if "parameters" not in query:

            raise ValueError(
                "Derived metric query is missing "
                "'parameters'."
            )

        if not isinstance(
            query["parameters"],
            dict
        ):

            raise ValueError(
                "'parameters' must be a dictionary."
            )

    return query