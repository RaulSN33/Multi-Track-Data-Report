# Multi-Track-Data-Report

This project automates the creation of custom Excel reports summarizing academic performance and attendance data for university students.
Given a year of student records, the system loads and processes the data, computes key metrics, generates visualizations, and produces a polished Excel report intended for administrative staff.

The tool is fully command-line–driven: the user selects the academic year, and the report is generated end-to-end.

### Features: 

Data Loading: Automatically reads student datasets for a selected academic year.

Data Wrangling & Cleaning :Handles preprocessing, restructuring, aggregations, and validation.

#### Automatic Calculations:

- Attendance statistics 
- Subject-level summaries
- Track-based comparisons
- One-year consolidated indicators

#### Plot Generation:

- Creates visuals to support the report (bar charts, distributions, comparisons, etc.).

#### Excel Report Generation
- Produces a structured Excel report with:


## Summary pages

### Interactive CLI
The program runs in the terminal and prompts the user to choose which year to generate a report for.

### Project Structure

``` bash
Multi-Track-Data-Report/
├── .gitignore
├── LICENSE
├── Multi_Track_Data_Report_Project.pdf
├── README.md
├── workflow_debbuger.py
├── __main__.py
├── Input/
│   ├── student_grades_2027-2028.xlsx
│   └── student_grades_2028-2029.xlsx #Generated file to use it for another year
├── Output/ # where output data and reports will be stored!
│   ├── ConsolidatedData/
│   │   ├── .gitkeep
│   └── SummaryReports/
│       ├── .gitkeep
└── src/
    ├── calculations.py
    ├── DataClass.py
    ├── DataLoader.py
    ├── DataWrangling.py
    ├── helpers.py
    ├── multiyear_report.py
    ├── one_year_report.py
    ├── ploting.py
    ├── report_initiator.py
    ├── xlsx_report.py
    └── __init__.py
```
### How to Use
1. Install Requirements

pip install -r requirements.txt

2. Run the Program

From the project root:

python __main__.py


The system will display a prompt in the terminal asking you to choose the academic year.
After selection, the program will:

- Load the corresponding dataset
- Process and analyze the data
- Generate plots
- Produce a final Excel report in the output folder

### Workflow Overview

1. User selects a year via CLI.

2. DataLoader retrieves the correct year’s dataset.
3. DataLoader Saves the cleaned and aggregated Dataset
4. DataWrangling and calculations clean the data and compute metrics.
5. ploting.py creates visuals (matplotlib).
6. xlsx_report.py composes the final Excel report:
   - Embedded plots
   - Summary tables 
   - Report is delivered to the administrative staff for academic analysis and decision-making.

### Intended Audience

This tool is designed for university administrative staff who need clear, accurate reporting on student performance and attendance across multiple programs or tracks.

### Technologies Used

- Python:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - xlwings

###  License

This project is licensed under the MIT License.
See the LICENSE file for details.

###  Contact

For questions or suggestions, please reach out through GitHub:
RaulSN33

