import csv
import math
import sys

DATA_FILE = 'Employee_Survey_Data.csv'


def read_numeric_columns(path):
    """Read CSV and return order of numeric columns and column data lists (with
    Nones)."""
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        numeric_cols = [c for c in reader.fieldnames if c.startswith('Q') and c.endswith('Number')]
        data = {col: [] for col in numeric_cols}
        for row in reader:
            for col in numeric_cols:
                val = row.get(col, '').strip()
                if val == '' or val is None:
                    data[col].append(None)
                else:
                    try:
                        data[col].append(float(val))
                    except ValueError:
                        data[col].append(None)
    return numeric_cols, data


def read_numeric_columns_by_supervisor(path):
    """Return numeric data segmented by the Y/N Supervisor column."""
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        numeric_cols = [c for c in reader.fieldnames if c.startswith('Q') and c.endswith('Number')]
        groups = {
            'Y': {col: [] for col in numeric_cols},
            'N': {col: [] for col in numeric_cols},
        }
        for row in reader:
            group = row.get('Supervisor', '').strip().upper()
            if group not in groups:
                continue  # ignore blanks or unexpected values
            for col in numeric_cols:
                val = row.get(col, '').strip()
                if val == '' or val is None:
                    groups[group][col].append(None)
                else:
                    try:
                        groups[group][col].append(float(val))
                    except ValueError:
                        groups[group][col].append(None)
    return numeric_cols, groups


def covariance(list_x, list_y):
    paired = [(x, y) for x, y in zip(list_x, list_y) if x is not None and y is not None]
    n = len(paired)
    if n < 2:
        return float('nan')
    xs, ys = zip(*paired)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / (n - 1)


def main(path=DATA_FILE):
    numeric_cols, groups = read_numeric_columns_by_supervisor(path)
    for group, data in groups.items():
        print(f"\nSupervisor {group} responses:")
        for col in numeric_cols:
            print(f"Covariance of {col} with other Q-number columns:")
            for other in numeric_cols:
                if other == col:
                    continue
                cov = covariance(data[col], data[other])
                print(f"  {other}: {cov:.3f}")
            print()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
