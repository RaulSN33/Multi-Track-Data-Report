import seaborn as sns
import matplotlib.pyplot as plt

from src.DataLoader import DataLoader
from src.calculations import (
    avg_by_track_income,
    pass_vs_fail_analytics,
    total_number_students,
    average_calculation,
    formula_loop_filler,
    correlation_calc
)

from src.helpers import (
    terms,
    subjects,
    terms_mapping_dict
)
from src.ploting import (
    average_grades,
    by_subject_boxplot,
    pct_passed_pie
)

route = 'Input'
loader = DataLoader(route)


#%%

loader.get_data()

data = loader.data
available_years = loader.available_years
# data['student_grades_2027-2028']

described_fall = data['2027-2028']['Fall'].df.describe()
described_spring = data['2027-2028']['Spring'].df.describe()



#%%

"""
2. Track-Level Summary Statistics 
Compute and present: 
- Total number of students per track 
- Average subject scores - Average attendance and project scores 
- Pass rates based on the designated "Passed (Y/N)" column
"""

total_number_students_dict = formula_loop_filler(
    data,
    available_years,
    terms,
    total_number_students
)
average_scores_data = formula_loop_filler(
    data,
    available_years,
    terms,
    average_calculation
)
pass_rates_data = formula_loop_filler(
    data,
    available_years,
    terms,
    pass_vs_fail_analytics,
    normalize=True,
    by_exchange_students=True
)
a = 0
# total_number_students(
#     data,
#     year='2027-2028',
#     term= 'Fall'
# )

#%%

"""
3. Cross-Track Comparative Analysis 
Visualize distributions of History grades for each track using histograms or boxplots 
Compare average Mathematics scores between tracks 
Analyze correlations between attendance and project scores per track 
"""


pass_fail_dict_results = pass_vs_fail_analytics(
    data,
    year='2027-2028',
    term='Fall'
)


for _, term in terms_mapping_dict.items():
    pct_passed_pie(
        pass_fail_dict_results[term],
        data['2027-2028'][term].df
    )

corr = formula_loop_filler(
    data,
    available_years,
    terms,
    correlation_calc,

)
#%%

a = data['2027-2028']['Spring'].df[
    [
        'Track',
        'Attendance (%)',
        'ProjectScore'
    ]
]

sns.pairplot(
    a,
    hue='Track',
    markers=["o", "s", "D"]
)
plt.show()
#%%

sns.pairplot(
    a,
    hue='Track',
    markers=["o", "s", "D"],
    x_vars=['ProjectScore'],
    y_vars=['ProjectScore'],
)
plt.show()
#%%

for term in terms:
    for subject in subjects:
        by_subject_boxplot(
            data['2027-2028'][term].df,
            subject,
            year = ['2027-2028'],
            term = term
        )

#%%

"""
4. Cohort-Level Analysis 
Calculate average grades and pass rates segmented by cohort 
Compare academic performance of income-supported students (IncomeStudent = True) 
against others
"""

summary_avg1, summary_avg2 = avg_by_track_income(data, '2027-2028')

# histograms(
#     data,
#     '2027-2028',
#     terms=terms
# )
average_grades(
    groupby_summaries=summary_avg1['Math'].to_frame(),
    plot_title = 'Fall Term; Average grades by track'

)

average_grades(
    groupby_summaries=summary_avg2['Math'].to_frame(),
    plot_title = 'Spring Term; Average grades by track'

)
#
average_grades(
    groupby_summaries=summary_avg1,
    plot_title = 'Fall Term; Average grades by track'

)

average_grades(
    groupby_summaries=summary_avg2,
    plot_title = 'Spring Term; Average grades by track'

)

#%%

"""
5. Final Report Generation 
Export a summary report as a CSV or Excel file encompassing all computed statistics 
Optionally generate charts and plots using matplotlib or seaborn libraries for visual 
interpretation 
"""
