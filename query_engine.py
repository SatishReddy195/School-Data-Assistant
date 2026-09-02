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
# Available School Datasets
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
# Supported Operations
# =========================================================

SUPPORTED_OPERATIONS = {
    "records",
    "count",
    "sum",
    "average",
    "min",
    "max",
    "percentage",
}


# =========================================================
# Supported Comparison Operators
# =========================================================

SUPPORTED_OPERATORS = {
    "==",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
}


# =========================================================
# Convert Values
# =========================================================

def convert_value(value):
    """
    Convert numeric-looking strings into numbers.
    Leave normal text unchanged.
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
# Apply One Condition
# =========================================================

def apply_condition(df, column, operator, value):
    """
    Apply one comparison condition to a DataFrame.
    """

    # -----------------------------------------------------
    # Validate column
    # -----------------------------------------------------

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    # -----------------------------------------------------
    # Convert value
    # -----------------------------------------------------

    value = convert_value(value)

    # -----------------------------------------------------
    # Text comparison
    # -----------------------------------------------------

    if isinstance(value, str):

        series = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        comparison_value = value.strip().lower()

        if operator == "==":
            return df[series == comparison_value]

        if operator == "!=":
            return df[series != comparison_value]

        raise ValueError(
            f"Operator '{operator}' cannot be used "
            f"with text values."
        )

    # -----------------------------------------------------
    # Numeric comparison
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


# =========================================================
# Apply All Conditions
# =========================================================

def apply_conditions(df, conditions):
    """
    Apply all query conditions to the DataFrame.
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
            value
        )

    return df


# =========================================================
# Execute Query
# =========================================================

def execute_query(
    dataset,
    operation,
    column=None,
    conditions=None,
    group_by=None,
    numerator_conditions=None,
):
    """
    Execute a structured query against school data.
    """

    # -----------------------------------------------------
    # Validate dataset
    # -----------------------------------------------------

    if dataset not in DATASETS:
        raise ValueError(
            f"Unknown dataset: {dataset}"
        )

    # -----------------------------------------------------
    # Validate operation
    # -----------------------------------------------------

    if operation not in SUPPORTED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    # -----------------------------------------------------
    # Get dataset
    # -----------------------------------------------------

    df = DATASETS[dataset].copy()

    # -----------------------------------------------------
    # Apply filters / conditions
    # -----------------------------------------------------

    df = apply_conditions(
        df,
        conditions
    )

    # -----------------------------------------------------
    # No matching records
    # -----------------------------------------------------

    if df.empty:
        return None

    # -----------------------------------------------------
    # Grouped query
    # -----------------------------------------------------

    if group_by:

        if group_by not in df.columns:
            raise ValueError(
                f"Group column '{group_by}' "
                f"does not exist."
            )

        # -------------------------------------------------
        # Group count
        # -------------------------------------------------

        if operation == "count":

            result = (
                df.groupby(group_by)
                .size()
                .reset_index(name="count")
            )

            return result

        # -------------------------------------------------
        # Group numerical calculations
        # -------------------------------------------------

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
                    f"does not exist."
                )

            grouped = df.groupby(group_by)[column]

            if operation == "sum":
                result = grouped.sum()

            elif operation == "average":
                result = grouped.mean()

            elif operation == "min":
                result = grouped.min()

            else:
                result = grouped.max()

            return result.reset_index(
                name=operation
            )

    # -----------------------------------------------------
    # Return records
    # -----------------------------------------------------

    if operation == "records":

        return df.head(100)

    # -----------------------------------------------------
    # Count
    # -----------------------------------------------------

    if operation == "count":

        return len(df)

    # -----------------------------------------------------
    # Numerical operations
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
                f"does not exist."
            )

        if operation == "sum":
            return df[column].sum()

        if operation == "average":
            return df[column].mean()

        if operation == "min":
            return df[column].min()

        if operation == "max":
            return df[column].max()

    # -----------------------------------------------------
    # Percentage
    # -----------------------------------------------------

    if operation == "percentage":

        if not numerator_conditions:
            raise ValueError(
                "Percentage query requires "
                "numerator_conditions."
            )

        numerator_df = apply_conditions(
            df.copy(),
            numerator_conditions
        )

        numerator = len(numerator_df)
        denominator = len(df)

        if denominator == 0:
            return 0

        percentage = (
            numerator / denominator
        ) * 100

        return round(percentage, 2)

    # -----------------------------------------------------
    # Safety fallback
    # -----------------------------------------------------

    raise ValueError(
        f"Unable to execute operation "
        f"'{operation}'."
    )