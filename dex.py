#!/usr/bin/env python3
"""
Simple CSV data exploration script with histograms.

Usage:
    python explore_csv.py [csv_file]

If csv_file is not provided, the user will be prompted to enter a CSV file path.
"""

import sys
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Explore CSV data and generate histograms.')
    parser.add_argument('csv_file', nargs='?', default=None,
                        help='Path to CSV file (if not provided, user will be prompted)')
    args = parser.parse_args()

    csv_path = args.csv_file
    if csv_path is None:
        csv_path = input("Enter the path to the CSV file: ").strip()

    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    print(f"Exploring CSV file: {csv_path}")
    print("=" * 50)
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print()

    print("Columns:")
    for col in df.columns:
        print(f"  - {col}")
    print()

    print("Data types:")
    print(df.dtypes)
    print()

    print("Missing values:")
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    for col in df.columns:
        print(f"  {col}: {missing[col]} ({missing_percent[col]:.2f}%)")
    print()

    print("Basic statistics for numeric columns:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())
    else:
        print("No numeric columns found.")
    print()

    print("Value counts for categorical columns (top 5):")
    # Determine categorical columns: object, category, and string (for pandas >=2.0)
    try:
        # For pandas >= 2.0, 'str' is a valid dtype
        categorical_cols = df.select_dtypes(include=['object', 'category', 'str']).columns
    except TypeError:
        # For pandas < 2.0, 'str' is not a recognized dtype
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        print(f"  {col}:")
        print(df[col].value_counts().head())
        print()

    # Create histograms
    print("Generating histograms...")
    # Create a directory for plots if it doesn't exist
    plot_dir = "plots"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    for col in df.columns:
        plt.figure(figsize=(8, 6))

        if df[col].dtype in [np.int64, np.float64, np.int32, np.float32]:
            # Numeric column: histogram
            plt.hist(df[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.title(f'Histogram of {col}')
        else:
            # Categorical column: bar chart of value counts
            value_counts = df[col].value_counts().head(20)  # Top 20
            if len(value_counts) > 0:
                plt.bar(range(len(value_counts)), value_counts.values)
                plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
                plt.xlabel(col)
                plt.ylabel('Count')
                plt.title(f'Top 20 values of {col}')
            else:
                plt.text(0.5, 0.5, 'No data to display', ha='center', va='center')
                plt.title(f'{col} (no data)')

        plt.tight_layout()
        plot_filename = os.path.join(plot_dir, f"{col}_histogram.png")
        plt.savefig(plot_filename, dpi=150)
        plt.close()
        print(f"  Saved histogram for '{col}' to {plot_filename}")

    print()
    print(f"All plots saved in the '{plot_dir}' directory.")
    print("Exploration complete.")

if __name__ == "__main__":
    main()