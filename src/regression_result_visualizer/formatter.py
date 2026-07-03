"""Functions for validating and formatting regression results."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "variable",
    "coefficient",
    "std_error",
    "p_value",
}


def validate_results(df: pd.DataFrame) -> None:
    """Check whether the input data contains the required columns.

    Parameters
    ----------
    df:
        Regression result data.

    Raises
    ------
    ValueError:
        If required columns are missing or numerical columns contain
        non-numerical values.
    """
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing_text}")

    numerical_columns = ["coefficient", "std_error", "p_value"]

    for column in numerical_columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(f"Column '{column}' must contain numerical values.")

    if df["variable"].isna().any():
        raise ValueError("Column 'variable' must not contain missing values.")

    if df[numerical_columns].isna().any().any():
        raise ValueError("Numerical columns must not contain missing values.")

    if ((df["p_value"] < 0) | (df["p_value"] > 1)).any():
        raise ValueError("p_value must be between 0 and 1.")

    if (df["std_error"] < 0).any():
        raise ValueError("std_error must be zero or greater.")


def significance_stars(p_value: float) -> str:
    """Return statistical significance stars for a p-value.

    Parameters
    ----------
    p_value:
        Statistical p-value.

    Returns
    -------
    str
        "***" for p < 0.01,
        "**" for p < 0.05,
        "*" for p < 0.10,
        and an empty string otherwise.
    """
    if not 0 <= p_value <= 1:
        raise ValueError("p_value must be between 0 and 1.")

    if p_value < 0.01:
        return "***"

    if p_value < 0.05:
        return "**"

    if p_value < 0.10:
        return "*"

    return ""


def format_coefficient(
    coefficient: float,
    p_value: float,
    digits: int = 3,
) -> str:
    """Format a coefficient and add significance stars."""
    if digits < 0:
        raise ValueError("digits must be zero or greater.")

    stars = significance_stars(p_value)
    return f"{coefficient:.{digits}f}{stars}"


def format_standard_error(
    std_error: float,
    digits: int = 3,
) -> str:
    """Format a standard error inside parentheses."""
    if std_error < 0:
        raise ValueError("std_error must be zero or greater.")

    if digits < 0:
        raise ValueError("digits must be zero or greater.")

    return f"({std_error:.{digits}f})"


def format_results_table(
    df: pd.DataFrame,
    digits: int = 3,
) -> pd.DataFrame:
    """Create a presentation-ready regression results table.

    Parameters
    ----------
    df:
        DataFrame containing variable, coefficient, std_error and p_value.
    digits:
        Number of decimal places.

    Returns
    -------
    pandas.DataFrame
        Formatted regression result table.
    """
    validate_results(df)

    if digits < 0:
        raise ValueError("digits must be zero or greater.")

    formatted = pd.DataFrame(
        {
            "Variable": df["variable"].astype(str),
            "Coefficient": [
                format_coefficient(coefficient, p_value, digits)
                for coefficient, p_value in zip(
                    df["coefficient"],
                    df["p_value"],
                    strict=True,
                )
            ],
            "Std. Error": [
                format_standard_error(std_error, digits)
                for std_error in df["std_error"]
            ],
            "p-value": [
                f"{p_value:.{digits}f}"
                for p_value in df["p_value"]
            ],
        }
    )

    return formatted