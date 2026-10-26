
import csv
from pathlib import Path


def load_csv(file_path):
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        headers = reader.fieldnames

    return headers, rows


def clean_data(headers, rows):
    cleaned_rows = []
    seen_rows = set()

    removed_empty = 0
    removed_duplicates = 0

    for row in rows:
        # Remove completely empty rows
        if all(not (value or "").strip() for value in row.values()):
            removed_empty += 1
            continue

        # Remove duplicate rows
        row_key = tuple((row.get(header) or "").strip() for header in headers)

        if row_key in seen_rows:
            removed_duplicates += 1
            continue

        seen_rows.add(row_key)

        # Normalize whitespace
        cleaned_row = {
            header: (row.get(header) or "").strip()
            for header in headers
        }

        cleaned_rows.append(cleaned_row)

    return cleaned_rows, removed_empty, removed_duplicates


def save_csv(file_path, headers, rows):
    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def save_report(file_path, original_count, cleaned_count,
                empty_count, duplicate_count, headers, rows):
    report_lines = [
        "CSV DATA CLEANING REPORT",
        "=" * 30,
        f"Original rows: {original_count}",
        f"Empty rows removed: {empty_count}",
        f"Duplicate rows removed: {duplicate_count}",
        f"Clean rows remaining: {cleaned_count}",
        "",
        "MISSING VALUES",
        "-" * 30,
    ]

    for header in headers:
        missing = sum(
            1 for row in rows
            if not row.get(header, "").strip()
        )
        report_lines.append(f"{header}: {missing}")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(report_lines) + "\n")

def main():
    folder = Path(__file__).parent
    input_file = folder / "sample_data.csv"

    if not input_file.exists():
        print(f"Error: File not found: {input_file.name}")
        return

    
    try:
        headers, rows = load_csv(input_file)
    except (OSError, csv.Error, UnicodeError) as error:
        print(f"Error: Could not read CSV file: {error}")
        return

    if not headers:
        print("Error: CSV headers are missing.")
        return


    cleaned_rows, empty_count, duplicate_count = clean_data(headers, rows)
    output_file = folder / "cleaned_data.csv"
    save_csv(output_file, headers, cleaned_rows)
    report_file = folder / "report.txt"

    save_report(
    report_file,
    len(rows),
    len(cleaned_rows),
    empty_count,
    duplicate_count,
    headers,
    cleaned_rows,
)

    print("CSV Data Cleaner & Report Generator")
    print("-" * 35)
    print(f"Original rows: {len(rows)}")
    print(f"Empty rows removed: {empty_count}")
    print(f"Duplicate rows removed: {duplicate_count}")
    print(f"Clean rows remaining: {len(cleaned_rows)}")

    print("\nMissing values:")
    for header in headers:
        missing = sum(
            1 for row in cleaned_rows
            if not row.get(header, "").strip()
        )
        print(f"- {header}: {missing}")
    print(f"\nCleaned file saved: {output_file.name}")
    print(f"Report saved: {report_file.name}")

if __name__ == "__main__":
    main()
