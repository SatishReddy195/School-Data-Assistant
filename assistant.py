import os

from google import genai
from google.genai import types

from query_engine import (
    query_school_data,
    get_school_metric,
)


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================================
# AGENT INSTRUCTIONS
# =========================================================

SYSTEM_INSTRUCTION = """
You are the School Data AI Agent.

You help a school principal answer questions about
school data.

You have access to two tools:

1. query_school_data
2. get_school_metric

=========================================================
YOUR RESPONSIBILITY
=========================================================

Understand the principal's question.

Decide whether you need a tool.

Choose the correct tool.

Provide the correct arguments.

Use the tool result to answer the principal.

=========================================================
TOOL 1: query_school_data
=========================================================

Use this for normal data queries such as:

- How many students are there?
- How many female students are there?
- Show students in class 8.
- What are the marks of student STU001?
- What is the average Mathematics mark?
- How many complaints are there?
- How many teachers are there by department?
- What is the total amount paid in fees?

Available datasets:

students
marks
fees
attendance
complaints
sports
teachers

Available operations:

records
count
sum
average
min
max

Available comparison operators:

==
!=
>
<
>=
<=

=========================================================
TOOL 2: get_school_metric
=========================================================

Use this for predefined school business calculations.

Available metrics:

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
IMPORTANT
=========================================================

Never invent data.

Never calculate school data yourself when a tool
can retrieve or calculate it.

Always use the appropriate tool for school-data questions.

The tool results are authoritative.

You may call more than one tool when a question
requires multiple steps.

For example:

"What class has the highest average marks and how
much fee is outstanding for that class?"

You may:

1. Query average marks grouped by class.
2. Identify the class with the highest result.
3. Query outstanding fees for that class.
4. Give the final answer.

Do not expose internal tool names or implementation
details to the principal.

Be concise and professional.

If no matching data exists, clearly say that no
matching records were found.
"""


# =========================================================
# GEMINI TOOL DECLARATIONS
# =========================================================

QUERY_SCHOOL_DATA_DECLARATION = {
    "name": "query_school_data",
    "description": """
Query school datasets using safe predefined operations.

Use this for normal filtering, counting, aggregation,
and record retrieval.

Available datasets:
students, marks, fees, attendance, complaints,
sports, teachers.

Available operations:
records, count, sum, average, min, max.
""",
    "parameters": {
        "type": "object",
        "properties": {

            "dataset": {
                "type": "string",
                "description": (
                    "Dataset to query: "
                    "students, marks, fees, attendance, "
                    "complaints, sports, or teachers."
                ),
                "enum": [
                    "students",
                    "marks",
                    "fees",
                    "attendance",
                    "complaints",
                    "sports",
                    "teachers",
                ],
            },

            "operation": {
                "type": "string",
                "description": (
                    "Operation to perform."
                ),
                "enum": [
                    "records",
                    "count",
                    "sum",
                    "average",
                    "min",
                    "max",
                ],
            },

            "column": {
                "type": "string",
                "description": (
                    "Column to aggregate. "
                    "Use an empty string when not needed."
                ),
            },

            "conditions": {
                "type": "array",
                "description": (
                    "Optional filtering conditions."
                ),
                "items": {
                    "type": "object",
                    "properties": {

                        "column": {
                            "type": "string",
                        },

                        "operator": {
                            "type": "string",
                            "enum": [
                                "==",
                                "!=",
                                ">",
                                "<",
                                ">=",
                                "<=",
                            ],
                        },

                        "value": {
                            "type": "string",
                        },
                    },
                    "required": [
                        "column",
                        "operator",
                        "value",
                    ],
                },
            },

            "group_by": {
                "type": "string",
                "description": (
                    "Optional column to group results by. "
                    "Use an empty string when not needed."
                ),
            },
        },
        "required": [
            "dataset",
            "operation",
            "column",
            "conditions",
            "group_by",
        ],
    },
}


GET_SCHOOL_METRIC_DECLARATION = {
    "name": "get_school_metric",
    "description": """
Calculate predefined school business metrics.

Use this for school-level business calculations such as
student pass percentage, revenue, outstanding fees,
attendance, pending complaints, active students,
sports participation, and teacher count.
""",
    "parameters": {
        "type": "object",
        "properties": {

            "metric": {
                "type": "string",
                "description": "School metric to calculate.",
                "enum": [
                    "student_pass_percentage",
                    "total_revenue",
                    "total_outstanding_fees",
                    "average_attendance",
                    "students_below_attendance",
                    "pending_complaints",
                    "active_student_count",
                    "sports_participation",
                    "teacher_count",
                ],
            },

            "academic_year": {
                "type": "string",
                "description": (
                    "Academic year such as 2026-27. "
                    "Use an empty string if not specified."
                ),
            },

            "class_value": {
                "type": "integer",
                "description": (
                    "Class number when applicable. "
                    "Use 0 if not specified."
                ),
            },

            "threshold": {
                "type": "number",
                "description": (
                    "Attendance threshold when checking "
                    "students below a percentage."
                ),
            },

            "employment_status": {
                "type": "string",
                "description": (
                    "Teacher employment status when applicable. "
                    "Use an empty string if not specified."
                ),
            },
        },
        "required": [
            "metric",
            "academic_year",
            "class_value",
            "threshold",
            "employment_status",
        ],
    },
}


# =========================================================
# TOOL MAP
# =========================================================

AVAILABLE_FUNCTIONS = {
    "query_school_data": query_school_data,
    "get_school_metric": get_school_metric,
}


# =========================================================
# EXECUTE TOOL
# =========================================================

def execute_tool(
    function_name,
    function_args,
):
    """
    Execute only tools explicitly exposed to Gemini.
    """

    if function_name not in AVAILABLE_FUNCTIONS:
        raise ValueError(
            f"Unknown tool requested: {function_name}"
        )

    function = AVAILABLE_FUNCTIONS[
        function_name
    ]

    return function(
        **function_args
    )


# =========================================================
# MAIN AI AGENT
# =========================================================

def ask_school_data_assistant(question):
    """
    Run the School Data AI Agent.

    Gemini decides which school-data tool to call.
    Python executes the tool.
    Gemini receives the result and generates
    the final answer.
    """

    tools = types.Tool(
        function_declarations=[
            QUERY_SCHOOL_DATA_DECLARATION,
            GET_SCHOOL_METRIC_DECLARATION,
        ]
    )

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[tools],
        temperature=0.1,
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=question
                )
            ],
        )
    ]

    # =====================================================
    # AGENT LOOP
    # =====================================================

    for _ in range(10):

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=config,
        )

        model_content = (
            response.candidates[0].content
        )

        contents.append(
            model_content
        )

        function_calls = []

        for part in model_content.parts:

            if part.function_call:
                function_calls.append(
                    part.function_call
                )

        # -------------------------------------------------
        # NO TOOL CALL
        # -------------------------------------------------

        if not function_calls:

            if response.text:
                return response.text.strip()

            return (
                "I could not generate an answer "
                "for that question."
            )

        # -------------------------------------------------
        # EXECUTE TOOL CALLS
        # -------------------------------------------------

        tool_response_parts = []

        for function_call in function_calls:

            function_name = (
                function_call.name
            )

            function_args = dict(
                function_call.args
            )

            try:

                result = execute_tool(
                    function_name,
                    function_args,
                )

            except Exception as error:

                result = {
                    "status": "error",
                    "message": str(error),
                }

            tool_response_parts.append(
                types.Part.from_function_response(
                    name=function_name,
                    response=result,
                )
            )

        # -------------------------------------------------
        # SEND TOOL RESULTS BACK TO GEMINI
        # -------------------------------------------------

        contents.append(
            types.Content(
                role="user",
                parts=tool_response_parts,
            )
        )

    return (
        "I was unable to complete the request "
        "within the allowed number of tool steps."
    )