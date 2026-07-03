"""Tests for regression result formatting functions."""

import pandas as pd
import pytest

from regression_result_visualizer.formatter import (
    format_coefficient,
    format_results_table,
    format_standard_error,
    significance_stars,
    validate_results,
)


def create_sample_results() -> pd.DataFrame:
    """Create valid sample regression results."""
    return pd.DataFrame(
        {
            "variable": ["Health", "Income"],
            "coefficient": [0.4567, -0.2345],
            "std_error": [0.1234, 0.1000],
            "p_value": [0.008, 0.150],
        }
    )


def test_significance_stars() -> None:
    """Significance stars should correspond to p-value thresholds."""
    assert significance_stars(0.001) == "***"
    assert significance_stars(0.030) == "**"
    assert significance_stars(0.080) == "*"
    assert significance_stars(0.200) == ""


def test_significance_star_boundaries() -> None:
    """Exact threshold values should use the lower significance category."""
    assert significance_stars(0.010) == "**"
    assert significance_stars(0.050) == "*"
    assert significance_stars(0.100) == ""


def test_invalid_p_value() -> None:
    """Invalid p-values should raise ValueError."""
    with pytest.raises(ValueError):
        significance_stars(-0.1)

    with pytest.raises(ValueError):
        significance_stars(1.1)


def test_format_coefficient() -> None:
    """A coefficient should be rounded and include stars."""
    result = format_coefficient(
        coefficient=0.4567,
        p_value=0.008,
        digits=3,
    )

    assert result == "0.457***"


def test_format_standard_error() -> None:
    """A standard error should be displayed inside parentheses."""
    result = format_standard_error(
        std_error=0.1234,
        digits=3,
    )

    assert result == "(0.123)"


def test_validate_results() -> None:
    """Valid data should pass validation."""
    df = create_sample_results()

    validate_results(df)


def test_missing_required_column() -> None:
    """Missing required columns should raise ValueError."""
    df = create_sample_results().drop(columns=["p_value"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_results(df)


def test_negative_standard_error() -> None:
    """Negative standard errors should raise ValueError."""
    df = create_sample_results()
    df.loc[0, "std_error"] = -0.1

    with pytest.raises(ValueError, match="std_error"):
        validate_results(df)


def test_format_results_table() -> None:
    """Raw regression results should be converted into a formatted table."""
    df = create_sample_results()

    result = format_results_table(df, digits=3)

    assert list(result.columns) == [
        "Variable",
        "Coefficient",
        "Std. Error",
        "p-value",
    ]

    assert result.loc[0, "Variable"] == "Health"
    assert result.loc[0, "Coefficient"] == "0.457***"
    assert result.loc[0, "Std. Error"] == "(0.123)"
    assert result.loc[0, "p-value"] == "0.008"