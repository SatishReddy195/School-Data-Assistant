from data_loader import (
    students_df,
    marks_df,
    fees_df,
    attendance_df,
    complaints_df,
    sports_df,
    teachers_df,
)

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


# =========================================================
# DATASETS
# =========================================================

DATASETS = {
    "students": students_df,
    "marks": marks_df,
    "fees": fees_df,
    "attendance": attendance_df,
    "complaints": complaints_df,
    "sports": sports_df,
    "teachers": teachers_df,
}


# =========================================================
# ALLOWED OPERATIONS
# =========================================================

SUPPORTED_OPERATIONS = {
    "records",
    "count",
    "sum",
    "average",
    "min",
    "max",
}


SUPPORTED_OPERATORS = {
    "==",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
}


# =========================================================
# VALUE CONVERSION
# =========================================================

def convert_value(value):
    """
    Convert string values to int or float when possible.
    """

    if not isinstance(value, str):
        return value

    try:
        return int(value)

    except ValueError:

        try:
            return float(value)

        except ValueError:
            return value


# =========================================================
# CONDITION HANDLING
# =========================================================

def apply_condition(
    df,
    column,
    operator,
    value,
):
    """
    Apply one filtering condition to a DataFrame.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    value = convert_value(value)

    # -----------------------------------------------------
    # TEXT VALUES
    # -----------------------------------------------------

    if isinstance(value, str):

        series = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        comparison_value = (
            value
            .strip()
            .lower()
        )

        if operator == "==":
            return df[
                series == comparison_value
            ]

        if operator == "!=":
            return df[
                series != comparison_value
            ]

        raise ValueError(
            f"Operator '{operator}' cannot be "
            "used with text values."
        )

    # -----------------------------------------------------
    # NUMERIC VALUES
    # -----------------------------------------------------

    series = df[column]

    if operator == "==":
        return df[series == value]

    if operator == "!=":
        return df[series != value]

    if operator == ">":
        return df[series > value]

    if operator == "<":
        return df[series < value]

    if operator == ">=":
        return df[series >= value]

    if operator == "<=":
        return df[series <= value]

    raise ValueError(
        f"Unsupported operator: {operator}"
    )


def apply_conditions(
    df,
    conditions,
):
    """
    Apply all supplied conditions.
    """

    if not conditions:
        return df

    for condition in conditions:

        column = condition.get("column")
        operator = condition.get("operator")
        value = condition.get("value")

        if column is None:
            raise ValueError(
                "Condition is missing column."
            )

        if operator not in SUPPORTED_OPERATORS:
            raise ValueError(
                f"Unsupported operator: {operator}"
            )

        df = apply_condition(
            df,
            column,
            operator,
            value,
        )

    return df


# =========================================================
# TOOL 1
# STANDARD SCHOOL DATA QUERY
# =========================================================

def query_school_data(
    dataset: str,
    operation: str,
    column: str = None,
    conditions: list = None,
    group_by: str = None,
):
    """
    Query school datasets using safe, predefined operations.

    This tool can retrieve records, count records,
    calculate sums, averages, minimums, maximums,
    and grouped results.

    Available datasets:
    students, marks, fees, attendance,
    complaints, sports, teachers

    Available operations:
    records, count, sum, average, min, max

    Conditions use:
    ==, !=, >, <, >=, <=

    The model chooses the dataset, operation,
    columns, filters, and grouping.
    """

    if dataset not in DATASETS:
        raise ValueError(
            f"Unknown dataset: {dataset}"
        )

    if operation not in SUPPORTED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    df = DATASETS[dataset].copy()

    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    df = apply_conditions(
        df,
        conditions or [],
    )

    if df.empty:
        return {
            "status": "no_data",
            "message": "No matching records were found.",
        }

    # -----------------------------------------------------
    # GROUPED QUERY
    # -----------------------------------------------------

    if group_by:

        if group_by not in df.columns:
            raise ValueError(
                f"Group column '{group_by}' "
                "does not exist."
            )

        # COUNT BY GROUP

        if operation == "count":

            result = (
                df.groupby(group_by)
                .size()
                .reset_index(name="count")
            )

            return {
                "status": "success",
                "result": result.to_dict(
                    orient="records"
                ),
            }

        # NUMERIC AGGREGATIONS BY GROUP

        if operation in {
            "sum",
            "average",
            "min",
            "max",
        }:

            if column is None:
                raise ValueError(
                    f"Column is required for "
                    f"'{operation}'."
                )

            if column not in df.columns:
                raise ValueError(
                    f"Column '{column}' "
                    "does not exist."
                )

            grouped = df.groupby(
                group_by
            )[column]

            if operation == "sum":
                result = grouped.sum()

            elif operation == "average":
                result = grouped.mean()

            elif operation == "min":
                result = grouped.min()

            else:
                result = grouped.max()

            result = (
                result
                .reset_index(
                    name=operation
                )
            )

            return {
                "status": "success",
                "result": result.to_dict(
                    orient="records"
                ),
            }

    # -----------------------------------------------------
    # RECORDS
    # -----------------------------------------------------

    if operation == "records":

        result = df.head(100)

        return {
            "status": "success",
            "result": result.to_dict(
                orient="records"
            ),
        }

    # -----------------------------------------------------
    # COUNT
    # -----------------------------------------------------

    if operation == "count":

        return {
            "status": "success",
            "result": len(df),
        }

    # -----------------------------------------------------
    # AGGREGATIONS
    # -----------------------------------------------------

    if operation in {
        "sum",
        "average",
        "min",
        "max",
    }:

        if column is None:
            raise ValueError(
                f"Column is required for "
                f"'{operation}'."
            )

        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' "
                "does not exist."
            )

        if operation == "sum":
            value = df[column].sum()

        elif operation == "average":
            value = df[column].mean()

        elif operation == "min":
            value = df[column].min()

        else:
            value = df[column].max()

        return {
            "status": "success",
            "result": value,
        }

    raise ValueError(
        f"Unable to execute operation: {operation}"
    )


# =========================================================
# TOOL 2
# SCHOOL BUSINESS METRICS
# =========================================================

def get_school_metric(
    metric: str,
    academic_year: str = None,
    class_value: int = None,
    threshold: float = None,
    employment_status: str = None,
):
    """
    Calculate predefined school business metrics.

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

    This tool is used for business calculations that
    require predefined school-specific logic.
    """

    # -----------------------------------------------------
    # PASS PERCENTAGE
    # -----------------------------------------------------

    if metric == "student_pass_percentage":

        result = student_pass_percentage(
            academic_year=academic_year,
            class_value=class_value,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    # -----------------------------------------------------
    # TOTAL REVENUE
    # -----------------------------------------------------

    if metric == "total_revenue":

        result = total_revenue(
            academic_year=academic_year,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    # -----------------------------------------------------
    # OUTSTANDING FEES
    # -----------------------------------------------------

    if metric == "total_outstanding_fees":

        result = total_outstanding_fees(
            academic_year=academic_year,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    # -----------------------------------------------------
    # AVERAGE ATTENDANCE
    # -----------------------------------------------------

    if metric == "average_attendance":

        result = average_attendance(
            academic_year=academic_year,
            class_value=class_value,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    # -----------------------------------------------------
    # LOW ATTENDANCE
    # -----------------------------------------------------

    if metric == "students_below_attendance":

        if threshold is None:
            raise ValueError(
                "Attendance threshold is required."
            )

        result = students_below_attendance(
            threshold=threshold,
            academic_year=academic_year,
            class_value=class_value,
        )

        if result is None:
            return {
                "status": "no_data",
                "metric": metric,
                "result": [],
            }

        return {
            "status": "success",
            "metric": metric,
            "result": result.to_dict(
                orient="records"
            ),
        }

    # -----------------------------------------------------
    # PENDING COMPLAINTS
    # -----------------------------------------------------

    if metric == "pending_complaints":

        result = pending_complaints_count(
            academic_year=academic_year,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    # -----------------------------------------------------
    # ACTIVE STUDENTS
    # -----------------------------------------------------

    if metric == "active_student_count":

        result = active_student_count(
            academic_year=academic_year,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    # -----------------------------------------------------
    # SPORTS PARTICIPATION
    # -----------------------------------------------------

    if metric == "sports_participation":

        result = sports_participation_count(
            academic_year=academic_year,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    # -----------------------------------------------------
    # TEACHER COUNT
    # -----------------------------------------------------

    if metric == "teacher_count":

        result = teacher_count(
            employment_status=employment_status,
        )

        return {
            "status": "success",
            "metric": metric,
            "result": result,
        }

    raise ValueError(
        f"Unsupported school metric: {metric}"
    )