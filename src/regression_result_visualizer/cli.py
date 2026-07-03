"""Command-line interface for Regression Result Visualizer."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from regression_result_visualizer.plotter import (
    save_coefficient_plot,
    save_table_image,
)


def load_results(input_path: str | Path) -> pd.DataFrame:
    """Load regression results from a CSV or Excel file.

    Parameters
    ----------
    input_path:
        Path to a CSV or XLSX file.

    Returns
    -------
    pandas.DataFrame
        Loaded regression results.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    ValueError
        If the file format is unsupported.
    """
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file was not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)

    if suffix == ".xlsx":
        return pd.read_excel(path)

    raise ValueError("Input file must have a .csv or .xlsx extension.")


def create_parser() -> argparse.ArgumentParser:
    """Create and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Create a regression table image and a coefficient plot "
            "from CSV or Excel results."
        )
    )

    parser.add_argument(
        "input",
        help="Path to the input CSV or XLSX file.",
    )

    parser.add_argument(
        "--outdir",
        default="outputs",
        help="Directory where output files are saved. Default: outputs",
    )

    parser.add_argument(
        "--digits",
        type=int,
        default=3,
        help="Number of decimal places. Default: 3",
    )

    parser.add_argument(
        "--format",
        choices=["png", "pdf", "both"],
        default="both",
        help="Output format: png, pdf, or both. Default: both",
    )

    parser.add_argument(
        "--table-title",
        default="Regression Results",
        help="Title of the regression table.",
    )

    parser.add_argument(
        "--plot-title",
        default="Regression Coefficient Plot",
        help="Title of the coefficient plot.",
    )

    return parser


def main() -> None:
    """Run the command-line application."""
    parser = create_parser()
    args = parser.parse_args()

    if args.digits < 0:
        parser.error("--digits must be zero or greater.")

    try:
        results = load_results(args.input)
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))

    output_directory = Path(args.outdir)
    output_directory.mkdir(parents=True, exist_ok=True)

    formats = ["png", "pdf"] if args.format == "both" else [args.format]

    saved_files: list[Path] = []

    for file_format in formats:
        table_path = output_directory / f"regression_table.{file_format}"
        plot_path = output_directory / f"coefficient_plot.{file_format}"

        save_table_image(
            results,
            table_path,
            digits=args.digits,
            title=args.table_title,
        )

        save_coefficient_plot(
            results,
            plot_path,
            title=args.plot_title,
        )

        saved_files.extend([table_path, plot_path])

    print("Output files were created successfully:")

    for saved_file in saved_files:
        print(f"- {saved_file}")


if __name__ == "__main__":
    main()