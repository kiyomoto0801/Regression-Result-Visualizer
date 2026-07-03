"""Tests for regression result image generation."""

from pathlib import Path

import pandas as pd
import pytest

from regression_result_visualizer.plotter import (
    prepare_output_path,
    save_coefficient_plot,
    save_table_image,
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


def test_prepare_output_path_creates_directory(tmp_path: Path) -> None:
    """The output directory should be created automatically."""
    output_path = tmp_path / "new_directory" / "table.png"

    result = prepare_output_path(output_path)

    assert result == output_path
    assert output_path.parent.exists()


def test_prepare_output_path_rejects_invalid_extension(
    tmp_path: Path,
) -> None:
    """Unsupported file extensions should raise ValueError."""
    output_path = tmp_path / "table.txt"

    with pytest.raises(ValueError, match="png or .pdf"):
        prepare_output_path(output_path)


def test_save_table_image_png(tmp_path: Path) -> None:
    """A PNG regression table should be created."""
    df = create_sample_results()
    output_path = tmp_path / "regression_table.png"

    result = save_table_image(
        df,
        output_path,
        title="Test Regression Results",
    )

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_save_table_image_pdf(tmp_path: Path) -> None:
    """A PDF regression table should be created."""
    df = create_sample_results()
    output_path = tmp_path / "regression_table.pdf"

    save_table_image(df, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_save_coefficient_plot_png(tmp_path: Path) -> None:
    """A PNG coefficient plot should be created."""
    df = create_sample_results()
    output_path = tmp_path / "coefficient_plot.png"

    result = save_coefficient_plot(
        df,
        output_path,
        title="Test Coefficient Plot",
    )

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_save_coefficient_plot_pdf(tmp_path: Path) -> None:
    """A PDF coefficient plot should be created."""
    df = create_sample_results()
    output_path = tmp_path / "coefficient_plot.pdf"

    save_coefficient_plot(df, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_unsupported_confidence_level(tmp_path: Path) -> None:
    """Unsupported confidence levels should raise ValueError."""
    df = create_sample_results()
    output_path = tmp_path / "coefficient_plot.png"

    with pytest.raises(ValueError, match="95%"):
        save_coefficient_plot(
            df,
            output_path,
            confidence_level=0.90,
        )