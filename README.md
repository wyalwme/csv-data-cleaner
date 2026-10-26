
# CSV Data Cleaner & Report Generator

A Python tool that cleans CSV files and generates a summary report.

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

## How to Use

1. Place your input file in the project folder.
2. Name the input file `sample_data.csv`.
3. Run the program:

   ```bash
   python main.py
   ```

4. Check the generated files:
   - `cleaned_data.csv` — cleaned dataset
   - `report.txt` — cleaning summary and missing-value statistics

## Example

For the included sample dataset, the program removes one empty row and one duplicate record.

It also identifies missing email and age values without deleting those records.

## Project Structure

```text
prjct/
├── main.py
├── sample_data.csv
├── cleaned_data.csv
├── report.txt
└── README.md
```

## Limitations

The current version uses a fixed input filename and removes duplicate rows only when all column values match after whitespace trimming.
