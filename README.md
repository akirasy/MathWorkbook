# MathWorkbook

A Python-based utility to generate customizable math practice worksheets in PDF format. This tool supports addition, subtraction, and multiplication with automatic problem generation based on user-defined difficulty tiers.

## Features

- **Config-Driven**: Define your math problems (ranges, operations, and page counts) in a simple `config.yml` file.
- **Multiple Operations**: Supports Addition (`+`), Subtraction (`-`), and Multiplication (`x`).
- **Smart Logic**: Subtraction logic automatically ensures the top number is larger than the bottom number to prevent negative results.
- **Professional Layout**: Generates a clean 4-column grid with vertical math alignment and question numbering (1-24 per page).
- **Automated Answer Key**: Appends an answer key at the end of the PDF with coordinates mapping back to specific "Parts" and question numbers.

## Installation

* Clone the repository
   ```
   git clone --depth=1 https://github.com/akirasy/MathWorkbook.git
   ```

## Usage

* Edit the `config.yml` file to set your desired difficulty levels.
    ```
    workbook_name: "My_Math_Practice.pdf"
    tiers:
      - name: "Addition Mastery"
        min_top: 10
        max_top: 99
        min_bot: 2
        max_bot: 50
        operation: "+"
        pages: 1
    ```

* Run the generator:
    ```
    python main.py
    ```

