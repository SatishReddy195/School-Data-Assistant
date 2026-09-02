import os
import json
import pandas as pd

from google import genai


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================================
# RESULT FORMATTER
# =========================================================

def format_result(result):
    """
    Convert the verified Python/Pandas result into
    a clean representation that Gemini can understand.

    Gemini will NOT calculate the result.
    It will only explain the already-verified result.
    """

    # -----------------------------------------------------
    # Pandas DataFrame
    # -----------------------------------------------------

    if isinstance(result, pd.DataFrame):

        if result.empty:
            return "No matching records were found."

        return result.to_json(
            orient="records",
            date_format="iso"
        )

    # -----------------------------------------------------
    # Pandas Series
    # -----------------------------------------------------

    if isinstance(result, pd.Series):

        return result.to_json(
            orient="index"
        )

    # -----------------------------------------------------
    # Dictionary
    # -----------------------------------------------------

    if isinstance(result, dict):

        return json.dumps(
            result,
            default=str,
            indent=2
        )

    # -----------------------------------------------------
    # List
    # -----------------------------------------------------

    if isinstance(result, list):

        return json.dumps(
            result,
            default=str,
            indent=2
        )

    # -----------------------------------------------------
    # Numeric / String / Boolean
    # -----------------------------------------------------

    return str(result)


# =========================================================
# RESPONSE GENERATOR
# =========================================================

def generate_response(question, result):
    """
    Convert the verified school-data result into a
    clear response for the principal.
    """

    formatted_result = format_result(result)

    prompt = f"""
You are the response-generation layer of a School Data Assistant.

The principal asked:

{question}

The school-data system has already executed the query.

The VERIFIED RESULT is:

{formatted_result}

Your job is ONLY to explain this verified result
to the principal in clear and concise natural language.

=========================================================
IMPORTANT RULES
=========================================================

1. NEVER invent information.

2. NEVER change a number from the verified result.

3. NEVER perform your own calculations.

4. NEVER guess missing information.

5. Use ONLY the verified result provided above.

6. Do not mention:
   - Python
   - Pandas
   - Excel
   - APIs
   - query engine
   - Gemini
   - internal processing

7. If the result contains records, summarize them
   clearly and include the important fields.

8. If the result contains grouped data, explain the
   groups clearly.

9. If the result is a percentage, clearly include
   the percentage sign.

10. If the result is a financial amount, describe it
    clearly as a fee/revenue amount.

11. If the result is empty or says that no matching
    records were found, clearly tell the principal
    that no matching records were found.

12. Keep the answer concise and professional.

13. Answer the exact question asked.

=========================================================
EXAMPLES
=========================================================

Question:
How many students are there?

Verified result:
100

Good response:
There are 100 students.

---------------------------------------------------------

Question:
What is the overall student pass percentage?

Verified result:
82.5

Good response:
The overall student pass percentage is 82.5%.

---------------------------------------------------------

Question:
What is the total revenue?

Verified result:
1250000

Good response:
The total fee revenue is ₹1,250,000.

---------------------------------------------------------

Question:
How many complaints are pending?

Verified result:
7

Good response:
There are 7 pending complaints.

---------------------------------------------------------

Question:
Show students whose attendance is below 75%.

Verified result:
[
  {{"student_id": "STU001", "attendance_percentage": 68.5}},
  {{"student_id": "STU002", "attendance_percentage": 72.0}}
]

Good response:
2 students have attendance below 75%:
- STU001 — 68.5%
- STU002 — 72.0%

=========================================================

Return ONLY the final answer to the principal.
"""


    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text.strip()