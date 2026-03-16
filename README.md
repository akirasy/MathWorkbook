# MathWorkbook

A Python-based utility to generate customizable math practice worksheets in PDF format. This tool allows for highly tailored difficulty tiers and multiple visual layouts, making it perfect for students at different learning stages.

## Features

- **Config-Driven:** Define problem ranges, operations, page counts, and layouts in a single config.yml file.
- **Multiple Layout Styles:**
    - *Expanded*: Traditional vertical alignment (24 problems/page).
    - *List*: Horizontal equations with result lines (40 problems/page).
    - *Grid*: Problems contained within boxed cells (50 problems/page).
- **Smart Logic:**
    - Supports Addition (+) and Subtraction (-).
    - Automatic subtraction correction to ensure positive results.
    - Dynamic font sizing and alignment based on the selected layout.
- **Automated Answer Key:** Generates a comprehensive answer key at the end of the PDF, indexed by Tier and Page.

## Installation

Clone the repository:

```
git clone --depth=1 https://github.com/akirasy/MathWorkbook.git
```

> Python dependencies is included in this repository.
> There is no need to install any python module.

## Configuration

Edit the `config.yml` file to define your workbook structure:

    workbook_name: "Final_Math_Practice.pdf"
    
    tiers:
      - name: "Zufar"
        min_top: 599
        max_top: 999
        min_bot: 25
        max_bot: 555
        operation: "-"
        pages: 2
        layout: "expanded" # Options: expanded, list, grid
    
### Layout Comparison

| Layout | Problems per Page | Best For |
|:-:|:-:|---|
| Expanded | 24 | Long-form vertical calculation |
| List | 40 | Mental math and quick drills |
| Grid | 50 | High-density practice in a structured box |

## Usage

Run the generator from your terminal:

    python main.py

The PDF will be generated using the name specified in your configuration file.
