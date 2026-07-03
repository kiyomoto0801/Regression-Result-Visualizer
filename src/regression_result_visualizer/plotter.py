"""Functions for creating regression table images and coefficient plots."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from regression_result_visualizer.formatter import (
    format_results_table,
    validate_results,
)


def prepare_output_path(output_path: str | Path) -> Path:
    """Create the output directory and return the output path.

    Parameters
    ----------
    output_path:
        Path where the image will be saved.

    Returns
    -------
    pathlib.Path
        Prepared output path.

    Raises
    ------
    ValueError
        If the file extension is not PNG or PDF.
    """
    path = Path(output_path)

    supported_extensions = {".png", ".pdf"}

    if path.suffix.lower() not in supported_extensions:
        raise ValueError("Output file must have a .png or .pdf extension.")

    path.parent.mkdir(parents=True, exist_ok=True)

    return path


def save_table_image(
    df: pd.DataFrame,
    output_path: str | Path,
    digits: int = 3,
    title: str = "Regression Results",
) -> Path:
    """Create and save a formatted regression results table.

    Parameters
    ----------
    df:
        Regression result data.
    output_path:
        PNG or PDF output path.
    digits:
        Number of decimal places.
    title:
        Title displayed above the table.

    Returns
    -------
    pathlib.Path
        Path of the saved image.
    """
    formatted = format_results_table(df, digits=digits)
    path = prepare_output_path(output_path)

    row_count = len(formatted)
    figure_height = max(3.5, 1.2 + row_count * 0.55)

    fig, ax = plt.subplots(
        figsize=(10, figure_height),
        facecolor="white",
    )

    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")

    ax.set_title(
        title,
        fontsize=16,
        pad=18,
        color="black",
    )

    table = ax.table(
        cellText=formatted.values,
        colLabels=formatted.columns,
        cellLoc="center",
        colLoc="center",
        loc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.5)

    for column_index in range(len(formatted.columns)):
        table.auto_set_column_width(column_index)

    # 表全体の背景と文字色を明示的に設定する
    for (row_index, column_index), cell in table.get_celld().items():
        cell.set_edgecolor("black")
        cell.set_linewidth(0.5)
        cell.get_text().set_color("black")

        if row_index == 0:
            cell.set_facecolor("#E6E6E6")
            cell.get_text().set_weight("bold")
        else:
            cell.set_facecolor("white")

    fig.tight_layout()

    fig.savefig(
        path,
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
        transparent=False,
    )

    plt.close(fig)

    return path


def save_coefficient_plot(
    df: pd.DataFrame,
    output_path: str | Path,
    title: str = "Regression Coefficient Plot",
    confidence_level: float = 0.95,
) -> Path:
    """Create and save a coefficient plot with confidence intervals.

    Parameters
    ----------
    df:
        Regression result data.
    output_path:
        PNG or PDF output path.
    title:
        Title displayed above the graph.
    confidence_level:
        Confidence level. Currently, only 0.95 is supported.

    Returns
    -------
    pathlib.Path
        Path of the saved image.
    """
    validate_results(df)

    if confidence_level != 0.95:
        raise ValueError("Currently, only a 95% confidence level is supported.")

    path = prepare_output_path(output_path)

    plot_df = df.copy()
    plot_df["ci_size"] = 1.96 * plot_df["std_error"]

    figure_height = max(4.5, 1.5 + len(plot_df) * 0.55)

    fig, ax = plt.subplots(
        figsize=(10, figure_height),
        facecolor="white",
    )

    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.errorbar(
        plot_df["coefficient"],
        plot_df["variable"],
        xerr=plot_df["ci_size"],
        fmt="o",
        capsize=4,
        linewidth=1.2,
    )

    ax.axvline(
        x=0,
        linestyle="--",
        linewidth=1,
    )

    ax.set_title(
        title,
        fontsize=16,
        pad=14,
        color="black",
    )

    ax.set_xlabel(
        "Coefficient",
        color="black",
    )

    ax.set_ylabel(
        "Variable",
        color="black",
    )

    ax.tick_params(
        axis="both",
        colors="black",
    )

    ax.grid(
        axis="x",
        linestyle=":",
        linewidth=0.7,
    )

    fig.tight_layout()

    fig.savefig(
        path,
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
        transparent=False,
    )

    plt.close(fig)

    return path