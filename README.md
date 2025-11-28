# Multi-Track-Data-Report

This project automates the creation of custom Excel reports summarizing academic performance and attendance data for university students.
Given a year of student records, the system loads and processes the data, computes key metrics, generates visualizations, and produces a polished Excel report intended for administrative staff.

The tool is fully command-line–driven: the user selects the academic year, and the report is generated end-to-end.


## _Assumptions_:

After exploring the data, we realized that the file contains data from the spring and fall terms. For us, it does not make 
sense to compute all the calculations mixing the scores of both semesters, just like in reality! Furthermore, each semester
contains different students, so it is not that on fall the students had History I and in spring they attended History II.
This is why the code is meant to handle Yearly data, to then be splitted in Fall and Spring semester, all the calculations are done based on this 
assumption, also the DataClass is programed to handle this differences. This handling will be clear in the excel report.

To use the code, the users should put all the student_grades_XXXX-xxxx.xlsx files in the ```Input/ ``` route.

The code will read all files from this route and will give the user the opportunity to select which year to use to make the report.

We coded the option to select the multi-year report, and the functions are well connected with the logic,
but due to time constraints, we could do a multiyear report, so if the user selects this option, the console will only 
print that we are working on that feature for future work, just like any other good python project :^)

The output is stored in 2 routes:
- ```Output/ConsolidatedData``` : will contain the consolidated and cleaned dataset in .csv, where the first entries of the
table are from the fall semester, the others from the spring semester.
- ```Output/SummaryReports```: is where the formated ecel report will be stored, with the academicyear_summary_report.xlsx filename.

The ```src/helpers.py``` contain all parameters used in the code, like subject names, possible values which 
could be mistakes in the data, names of the tracks, etc. This makes the code more future-proof, as if any of these labels
where to change in the input excel files, the user should change them here in order for the code to work again.

Finaly, we created another year of data for the grader to check that the code is working with multiple years of data!

### Features: 

Data Loading: Automatically reads student datasets for a selected academic year.

Data Wrangling & Cleaning: Handles preprocessing, restructuring, aggregations, and validation.

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
    ├── calculations.py #To calculate all pertinent metrics
    ├── dataClass.py #DataClass to store by-term data
    ├── dataLoader.py #DataLoader object to read and fill the dataclass object
    ├── datawrangling.py #All datacleaning logics
    ├── helpers.py #All hardcoded variables
    ├── multiyear_report.py #.py for multiyear analysis
    ├── one_year_report.py # orchestrating all calculations and plots
    ├── ploting.py #Plot Functions
    ├── report_initiator.py # CLI menu interfase
    ├── xlsx_report.py #xlwings report creator
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
5. ploting.py creates visuals (matplotlib and Seaborne).
6. xlsx_report.py composes the final Excel report:
   - Embedded plots
   - Summary tables 
   - Report is delivered to the administrative staff for academic analysis and decision-making.

### Intended Audience

This tool is designed for university administrative staff who need clear, accurate reporting on student performance and attendance across multiple programs or tracks.

### Libraries Used

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

