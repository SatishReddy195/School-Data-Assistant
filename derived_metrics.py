import pandas as pd

from data_loader import (
    students_df,
    marks_df,
    fees_df,
    attendance_df,
    complaints_df,
    sports_df,
    teachers_df,
)


# =========================================================
# Student Pass Percentage
# =========================================================

def student_pass_percentage(
    academic_year=None,
    class_value=None,
):
    """
    Calculate the percentage of students who passed.

    A student is considered to have passed when all of
    their available mark records have pass_fail = "Pass".
    """

    df = marks_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    # -----------------------------------------------------
    # Class filter
    # -----------------------------------------------------

    if class_value is not None:

        df = df[
            df["class"] == class_value
        ]

    # -----------------------------------------------------
    # No data
    # -----------------------------------------------------

    if df.empty:
        return None

    # -----------------------------------------------------
    # Determine whether each student passed
    # -----------------------------------------------------

    student_results = (
        df.groupby("student_id")["pass_fail"]
        .apply(
            lambda values:
            values.astype(str)
            .str.strip()
            .str.lower()
            .eq("pass")
            .all()
        )
    )

    total_students = len(student_results)

    passed_students = student_results.sum()

    # -----------------------------------------------------
    # Calculate percentage
    # -----------------------------------------------------

    if total_students == 0:
        return 0

    percentage = (
        passed_students / total_students
    ) * 100

    return round(percentage, 2)


# =========================================================
# Total Revenue
# =========================================================

def total_revenue(
    academic_year=None,
):
    """
    Calculate total fee amount collected.
    """

    df = fees_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    if df.empty:
        return None

    return round(
        df["amount_paid"].sum(),
        2
    )


# =========================================================
# Total Outstanding Fees
# =========================================================

def total_outstanding_fees(
    academic_year=None,
):
    """
    Calculate total pending fee amount.
    """

    df = fees_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    if df.empty:
        return None

    return round(
        df["amount_pending"].sum(),
        2
    )


# =========================================================
# Average Attendance
# =========================================================

def average_attendance(
    academic_year=None,
    class_value=None,
):
    """
    Calculate average attendance percentage.
    """

    df = attendance_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    # -----------------------------------------------------
    # Class filter
    # -----------------------------------------------------

    if class_value is not None:

        df = df[
            df["class"] == class_value
        ]

    if df.empty:
        return None

    return round(
        df["attendance_percentage"].mean(),
        2
    )


# =========================================================
# Students Below Attendance Threshold
# =========================================================

def students_below_attendance(
    threshold,
    academic_year=None,
    class_value=None,
):
    """
    Find students whose attendance percentage
    is below a specified threshold.
    """

    df = attendance_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    # -----------------------------------------------------
    # Class filter
    # -----------------------------------------------------

    if class_value is not None:

        df = df[
            df["class"] == class_value
        ]

    # -----------------------------------------------------
    # Attendance threshold
    # -----------------------------------------------------

    df = df[
        df["attendance_percentage"] < threshold
    ]

    if df.empty:
        return None

    # -----------------------------------------------------
    # Return unique students
    # -----------------------------------------------------

    result = (
        df[
            [
                "student_id",
                "academic_year",
                "class",
                "section",
                "attendance_percentage",
            ]
        ]
        .sort_values(
            "attendance_percentage"
        )
        .drop_duplicates(
            subset=["student_id"]
        )
        .reset_index(drop=True)
    )

    return result


# =========================================================
# Pending Complaints Count
# =========================================================

def pending_complaints_count(
    academic_year=None,
):
    """
    Count complaints whose status is Pending.
    """

    df = complaints_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    # -----------------------------------------------------
    # Pending complaints
    # -----------------------------------------------------

    df = df[
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "pending"
    ]

    return len(df)


# =========================================================
# Active Student Count
# =========================================================

def active_student_count(
    academic_year=None,
):
    """
    Count active students.
    """

    df = students_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    # -----------------------------------------------------
    # Active students
    # -----------------------------------------------------

    df = df[
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "active"
    ]

    return len(df)


# =========================================================
# Sports Participation Count
# =========================================================

def sports_participation_count(
    academic_year=None,
):
    """
    Count unique students who appear in the sports data.
    """

    df = sports_df.copy()

    # -----------------------------------------------------
    # Academic year filter
    # -----------------------------------------------------

    if academic_year is not None:

        df = df[
            df["academic_year"].astype(str).str.strip()
            == str(academic_year).strip()
        ]

    if df.empty:
        return 0

    return df["student_id"].nunique()


# =========================================================
# Teacher Count
# =========================================================

def teacher_count(
    employment_status=None,
):
    """
    Count teachers, optionally filtered by employment status.
    """

    df = teachers_df.copy()

    # -----------------------------------------------------
    # Employment status filter
    # -----------------------------------------------------

    if employment_status is not None:

        df = df[
            df["employment_status"]
            .astype(str)
            .str.strip()
            .str.lower()
            == str(employment_status).strip().lower()
        ]

    return len(df)