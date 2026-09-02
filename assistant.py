from query_interpreter import interpret_query
from query_engine import execute_query

from derived_metrics import (
    student_pass_percentage,
    total_revenue,
    total_outstanding_fees,
    average_attendance,
    students_below_attendance,
    pending_complaints_count,
    active_student_count,
    sports_participation_count,
    teacher_count,
)

from response_generator import generate_response


# =========================================================
# Derived Metric Router
# =========================================================

def execute_derived_metric(metric, parameters):
    """
    Execute a supported business/derived metric.
    """

    # -----------------------------------------------------
    # Student pass percentage
    # -----------------------------------------------------

    if metric == "student_pass_percentage":

        return student_pass_percentage(
            academic_year=parameters.get(
                "academic_year"
            ),
            class_value=parameters.get(
                "class"
            ),
        )

    # -----------------------------------------------------
    # Total revenue
    # -----------------------------------------------------

    if metric == "total_revenue":

        return total_revenue(
            academic_year=parameters.get(
                "academic_year"
            )
        )

    # -----------------------------------------------------
    # Outstanding fees
    # -----------------------------------------------------

    if metric == "total_outstanding_fees":

        return total_outstanding_fees(
            academic_year=parameters.get(
                "academic_year"
            )
        )

    # -----------------------------------------------------
    # Average attendance
    # -----------------------------------------------------

    if metric == "average_attendance":

        return average_attendance(
            academic_year=parameters.get(
                "academic_year"
            ),
            class_value=parameters.get(
                "class"
            ),
        )

    # -----------------------------------------------------
    # Students below attendance threshold
    # -----------------------------------------------------

    if metric == "students_below_attendance":

        threshold = parameters.get(
            "threshold"
        )

        if threshold is None:

            raise ValueError(
                "Attendance threshold is required."
            )

        return students_below_attendance(
            threshold=threshold,
            academic_year=parameters.get(
                "academic_year"
            ),
            class_value=parameters.get(
                "class"
            ),
        )

    # -----------------------------------------------------
    # Pending complaints
    # -----------------------------------------------------

    if metric == "pending_complaints":

        return pending_complaints_count(
            academic_year=parameters.get(
                "academic_year"
            )
        )

    # -----------------------------------------------------
    # Active students
    # -----------------------------------------------------

    if metric == "active_student_count":

        return active_student_count(
            academic_year=parameters.get(
                "academic_year"
            )
        )

    # -----------------------------------------------------
    # Sports participation
    # -----------------------------------------------------

    if metric == "sports_participation":

        return sports_participation_count(
            academic_year=parameters.get(
                "academic_year"
            )
        )

    # -----------------------------------------------------
    # Teacher count
    # -----------------------------------------------------

    if metric == "teacher_count":

        return teacher_count(
            employment_status=parameters.get(
                "employment_status"
            )
        )

    # -----------------------------------------------------
    # Unknown metric
    # -----------------------------------------------------

    raise ValueError(
        f"Unsupported derived metric: {metric}"
    )


# =========================================================
# Main School Data Assistant
# =========================================================

def ask_school_data_assistant(question):
    """
    Process a principal's natural-language question
    and return a human-friendly answer.
    """

    try:

        # -------------------------------------------------
        # Step 1
        # Gemini interprets the question
        # -------------------------------------------------

        query = interpret_query(question)

        # -------------------------------------------------
        # Step 2
        # Decide query path
        # -------------------------------------------------

        query_type = query["query_type"]

        # =================================================
        # STANDARD QUERY
        # =================================================

        if query_type == "standard_query":

            result = execute_query(
                dataset=query["dataset"],
                operation=query["operation"],
                column=query.get("column"),
                conditions=query.get(
                    "conditions",
                    []
                ),
                group_by=query.get(
                    "group_by"
                ),
                numerator_conditions=query.get(
                    "numerator_conditions",
                    []
                ),
            )

        # =================================================
        # DERIVED METRIC
        # =================================================

        elif query_type == "derived_metric":

            result = execute_derived_metric(
                metric=query["metric"],
                parameters=query["parameters"],
            )

        # -------------------------------------------------
        # Unknown query type
        # -------------------------------------------------

        else:

            raise ValueError(
                f"Unsupported query type: {query_type}"
            )

        # -------------------------------------------------
        # Step 3
        # No result
        # -------------------------------------------------

        if result is None:

            return (
                "I could not find any matching "
                "records in the school data."
            )

        # -------------------------------------------------
        # Step 4
        # Generate final response
        # -------------------------------------------------

        answer = generate_response(
            question=question,
            result=result,
        )

        return answer

    except Exception as error:

        return (
            "I was unable to process the question "
            "because of an internal error."
        )