# CSV Data Cleaner & Report Generator

A lightweight Python command-line tool for cleaning CSV datasets and generating data quality reports.

The project helps users remove empty and duplicate records, standardize whitespace, and identify missing values without modifying the original input file.

## Features

- Removes completely empty rows
- Detects and removes duplicate records
- Trims leading and trailing whitespace
- Detects missing values in each column
- Exports cleaned data to a separate CSV file
- Generates a text report with cleaning statistics
- Supports custom input and output filenames
- Handles missing files, invalid encodings, and CSV reading errors
- Validates command-line arguments

## Requirements

- Python 3.10 or newer
- No external dependencies required

## Installation

Clone the repository:

```bash
git clone https://github.com/wyalwme/csv-data-cleaner.git
cd csv-data-cleaner
```

## Usage

Run with the default sample file:

```bash
python main.py
```

Specify a custom input file:

```bash
python main.py customers.csv
```

Specify a custom output file:

```bash
python main.py customers.csv --output cleaned_customers.csv
```

The input and output arguments can also be provided in this order:

```bash
python main.py --output result.csv customers.csv
```

If no arguments are provided, the program uses:

- Input: `sample_data.csv`
- Output: `cleaned_data.csv`

## Example Results

Using the included sample dataset:

| Metric | Result |
|---|---:|
| Original rows | 7 |
| Empty rows removed | 1 |
| Duplicate rows removed | 1 |
| Clean rows remaining | 5 |

The program also detects missing values without automatically deleting affected records.

## Output Files

For an output file named `cleaned_data.csv`, the program generates:

- `cleaned_data.csv` — cleaned dataset
- `cleaned_data_report.txt` — data quality report

The report includes cleaning statistics and missing-value counts for each column.

## Running Tests

Run the automated test suite:

```bash
python -m unittest -v test_main.py
```

The project includes 12 automated tests covering:

- Empty row removal
- Duplicate detection
- Whitespace trimming
- Missing values
- Command-line argument validation
- Custom output filenames
- Missing input files
- Empty CSV files
- Invalid file encoding
- Absolute and relative file paths

## Test Coverage

Code coverage is measured using [Coverage.py](https://coverage.readthedocs.io/).

Install Coverage.py:

```bash
python -m pip install coverage
```

Run the tests with coverage:

```bash
python -m coverage erase
python -m coverage run -m unittest -v test_main.py
python -m coverage report -m
```

**Latest verified result: 100% statement and branch coverage for `main.py`.**

## Project Structure

```text
csv-data-cleaner/
├── main.py
├── test_main.py
├── sample_data.csv
├── README.md
├── .gitignore
└── .coveragerc
```

## Limitations

- Missing values are reported but not automatically filled or removed.
- Duplicate records are identified by comparing all column values after whitespace trimming.
- The tool is designed for standard CSV files and does not perform advanced data validation.

## Future Improvements

- JSON and Excel export support
- Configurable duplicate detection
- More advanced data validation
- Additional report formats
