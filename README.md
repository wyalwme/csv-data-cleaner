# CSV Data Cleaner & Report Generator

A lightweight Python tool that cleans CSV datasets and generates a data quality report.

## Features

- Removes completely empty rows
- Removes duplicate records
- Trims unnecessary whitespace
- Detects missing values in each column
- Exports cleaned data to a new CSV file
- Generates a text report with cleaning statistics
- Handles missing input files and common file-reading errors

## Requirements

- Python 3.10 or newer
- No external libraries required

## How to Run

1. Clone or download this repository.
2. Make sure `sample_data.csv` is in the project folder.
3. Open a terminal in the project directory.
4. Run:

```bash
python main.py
```

## Example Results

Using the included sample dataset:

| Metric | Result |
|---|---:|
| Original rows | 7 |
| Empty rows removed | 1 |
| Duplicate rows removed | 1 |
| Clean rows remaining | 5 |

The tool also detects missing email and age values without deleting those records.

## Output Files

- `cleaned_data.csv` — the cleaned dataset
- `report.txt` — summary statistics and missing-value counts

## Project Structure

```text
prjct/
├── main.py
├── sample_data.csv
├── cleaned_data.csv
├── report.txt
├── README.md
└── .gitignore
```

## Limitations

- The input filename is currently fixed as `sample_data.csv`.
- Duplicate records are identified when all column values match after whitespace trimming.
- Missing values are reported but not automatically filled or removed.

## Future Improvements

- Allow users to specify an input CSV filename
- Add command-line arguments
- Support exporting reports in JSON format