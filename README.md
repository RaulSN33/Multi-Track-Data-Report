# Multi-Track-Data-Report

This project automates the creation of custom Excel reports summarizing academic performance and attendance data for university students.
Given a year of student records, the system loads and processes the data, computes key metrics, generates visualizations, and produces a polished Excel report intended for administrative staff.

The tool is fully command-line–driven: the user selects the academic year, and the report is generated end-to-end.

### Features: 

Data Loading 
Automatically reads student datasets for a selected academic year.

Data Wrangling & Cleaning
Handles preprocessing, restructuring, aggregations, and validation.

Automatic Calculations
Computes metrics such as:

Attendance statistics

Subject-level summaries

Track-based comparisons

One-year consolidated indicators

Plot Generation
Creates visuals to support the report (bar charts, distributions, comparisons, etc.).

Excel Report Generation
Produces a structured Excel report with:


Summary pages

### Interactive CLI
The program runs in the terminal and prompts the user to choose which year to generate a report for.

### Project Structure
Multi-Track-Data-Report/
│
├── __main__.py               # CLI entry point
├── consolidated_data.csv     # Example consolidated dataset
├── Multi_Track_Data_Report_Project.pdf  # Project specification
├── LICENSE
├── README.md
│
└── src/
    ├── DataLoader.py         # Loading yearly datasets
    ├── DataWrangling.py      # Transformations, cleaning, reshaping
    ├── DataClass.py          # Defines student/year/track data structures
    ├── calculations.py       # Core calculations for metrics
    ├── helpers.py            # Utility functions shared across modules
    ├── ploting.py            # Plot creation (matplotlib)
    ├── one_year_report.py    # Logic for full-year report assembly
    ├── xlsx_report.py        # Excel writer / formatting
    ├── report_initiator.py   # Orchestrates data → analysis → report
    └── old_xlsxreport.py     # Legacy version (kept for reference)

### How to Use
1. Install Requirements

(If you have a requirements.txt, include it. If not, list your dependencies later.)

pip install -r requirements.txt

2. Run the Program

From the project root:

python __main__.py


The system will display a prompt in the terminal asking you to choose the academic year.
After selection, the program will:

Load the corresponding dataset

Process and analyze the data

Generate plots

Produce a final Excel report in the output folder

### Workflow Overview

User selects a year
via CLI.

DataLoader retrieves the correct year’s dataset.

DataWrangling and calculations clean the data and compute metrics.

ploting.py creates visuals (matplotlib).

xlsx_report.py composes the final Excel report:

Multiple sheets

Embedded plots

Summary tables

Report is delivered to the administrative staff for academic analysis and decision-making.

### Intended Audience

This tool is designed for university administrative staff who need clear, accurate reporting on student performance and attendance across multiple programs or tracks.

### Technologies Used

Python

pandas

numpy

matplotlib

openpyxl / xlsxwriter (depending on your implementation)

###  License

This project is licensed under the MIT License.
See the LICENSE file for details.

###  Contact

For questions or suggestions, please reach out through GitHub:
RaulSN33

