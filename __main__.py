import pandas as pd
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
    terms_mapping_dict, columns_to_compute_average
)
from src.ploting import (
    average_grades,
    by_subject_boxplot,
    pct_passed_pie
)
import xlwings as xw

# from src.xlsx_report import (
#     create_excel_report
# )

route = 'Input'
loader = DataLoader(route)


#%%

loader.get_data()

data = loader.data
available_years = loader.available_years

YEAR = '2027-2028'
# data['student_grades_2027-2028']
#
# described_fall = data['2027-2028']['Fall'].df.describe()
# described_spring = data['2027-2028']['Spring'].df.describe()


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
total_number_students_dict = total_number_students_dict[YEAR]
number_students_report = pd.DataFrame(total_number_students_dict)
average_scores_data = formula_loop_filler(
    data,
    available_years,
    terms,
    average_calculation
)
average_scores_data = average_scores_data[YEAR]
pass_rates_data = formula_loop_filler(
    data,
    available_years,
    terms,
    pass_vs_fail_analytics,
    normalize=True,
    by_exchange_students=False
)
pass_rates_data = pass_rates_data[YEAR]
pass_rates_report = pd.DataFrame(pass_rates_data)

avg_project_Scores = formula_loop_filler(
    data,
    available_years,
    terms,
    average_calculation,
    columns_to_compute_average = ['ProjectScore'],
)
avg_project_Scores = avg_project_Scores[YEAR]
avg_project_Scores = pd.concat(avg_project_Scores)

#%%

"""
3. Cross-Track Comparative Analysis 
Visualize distributions of History grades for each track using histograms or boxplots 
Compare average Mathematics scores between tracks 
Analyze correlations between attendance and project scores per track 
"""



pass_fail_dict_results = pass_vs_fail_analytics(
    data,
    year=YEAR,
    term='Fall'
)
pass_fail_dict_results['IncomeStudent']=pass_fail_dict_results['IncomeStudent'].replace({0:'Local',1:'Foreigner'})
pass_fail_dict_results.set_index(['Track', 'IncomeStudent'], inplace = True)

corr = formula_loop_filler(
    data,
    available_years,
    terms,
    correlation_calc,

)
corr=corr[YEAR]
pie_charts = {}
# pie_charts
for _, term in terms_mapping_dict.items():
    pie_charts[term] = pct_passed_pie(
        pass_fail_dict_results.reset_index(),
        data[YEAR][term].df,
        title = f'Average grades by track, {YEAR}; {term}'
    )


#%%

a = data[YEAR]['Spring'].df[
    [
        'Track',
        'Attendance (%)',
        'ProjectScore'
    ]
]
# fig_pairplot, ax = plt.subplots(figsize=(5,5))
fig_pairplot = sns.pairplot(
    a,
    hue='Track',
    markers=["o", "s", "D"],
)
# plt.title('ProjectScores against Attendance')
plt.show()


fig_pairplot = fig_pairplot.fig
#%%
#
# sns.pairplot(
#     a,
#     hue='Track',
#     markers=["o", "s", "D"],
#     x_vars=['ProjectScore'],
#     y_vars=['ProjectScore'],
# )
# plt.show()
#%%
# for subject in subjects:

subjects = ['Math', 'History']
math_plots={}
for subject in subjects:
    for term in terms:
        math_plots[term] = by_subject_boxplot(
            data[YEAR][term].df,
            subject,
            year = YEAR,
            term = term
        )

#%%

"""
4. Cohort-Level Analysis 
Calculate average grades and pass rates segmented by cohort 
Compare academic performance of income-supported students (IncomeStudent = True) 
against others
"""

# summary_avg1, summary_avg2 = avg_by_track_income(data, YEAR)
average_scores_by_income = formula_loop_filler(
    data,
    available_years,
    terms,
    avg_by_track_income,
)
average_scores_by_income=average_scores_by_income[YEAR]
#%%
# histograms(
#     data,
#     YEAR,
#     terms=terms
# )
average_scores_by_income_plots = {}
for term in terms:
    average_scores_by_income_plots[term] = average_grades(
        groupby_summaries=average_scores_by_income[term]['Math'].to_frame(),
        plot_title = f'Average grades by track, {YEAR}; {term}'

    )

# average_grades(
#     groupby_summaries=average_scores_by_income['Spring']['Math'].to_frame(),
#     plot_title = 'Spring Term; Average grades by track'
#
# )
#
# average_grades(
#     groupby_summaries=average_scores_by_income['Fall'],
#     plot_title = 'Fall Term; Average grades by track'
#
# )
#
# average_grades(
#     groupby_summaries=average_scores_by_income['Spring'],
#     plot_title = 'Spring Term; Average grades by track'
#
# )

#%%

"""
5. Final Report Generation 
Export a summary report as a CSV or Excel file encompassing all computed statistics 
Optionally generate charts and plots using matplotlib or seaborn libraries for visual 
interpretation 
"""

def create_excel_report(
    number_students_report: dict[str:pd.DataFrame],
    YEAR,
    average_scores_data,
    pass_rates_report,
    avg_project_Scores,
    pass_fail_dict_results,
    pie_charts,
    corr,
    fig_pairplot,
    math_plots,
    average_scores_by_income_plots,
):
    # n_rows = average_scores_data.shape[0]
    # start_cell = 6
    # end_row = start_cell + n_rows

    wb = xw.Book()
    app = xw.apps.active
    app.api.ActiveWindow.DisplayGridlines = False
    # try:
    #     sheet1 = wb.sheets['Hoja1']
    # except:
    #     sheet1 = wb.sheets['Sheet1']
    sheet1 = wb.sheets[0]
    # sheet1 = wb.add_worksheet('Summary Stats')
    # sheet1.set_tab_color('#E7E6E6')

    """
    2. Track-Level Summary Statistics 
    Compute and present: 
    - Total number of students per track 
    - Average subject scores - Average attendance and project scores 
    - Pass rates based on the designated "Passed (Y/N)" column
    """

    sheet1.range('B1:K1').merge()
    sheet1.range("B1").value = f"{YEAR} EDHEC Summary Report"
    sheet1.range("B1").font.bold = True
    sheet1.range("B1").font.size = 20

    sheet1['B2'].value = '2.1 Total number of students'
    sheet1['B2'].api.Font.Bold = True
    sheet1['B3'].value = number_students_report

    sheet1['F2'].value = '2.2 Average subject scores; Fall Semester'
    sheet1['F2'].api.Font.Bold = True
    sheet1['F3'].value = average_scores_data['Fall']

    sheet1['L2'].value = '2.2 Average subject scores; Spring Semester'
    sheet1['L2'].api.Font.Bold = True
    sheet1['L3'].value = average_scores_data['Spring']

    sheet1['R2'].value = '2.3 Average PassRates'
    sheet1['R2'].api.Font.Bold = True
    sheet1['R3'].value = pass_rates_report

    sheet1['V2'].value = '2.4 Average PassRates'
    sheet1['V2'].api.Font.Bold = True
    sheet1['V3'].value = avg_project_Scores

    ##########
    sheet1['B11'].value = '3 Income PassRates'
    sheet1['B11'].api.Font.Bold = True
    sheet1['B12'].value = pass_fail_dict_results

    ##########
    sheet1['B31'].value = '3.3 Correlation between attendance and project scores'
    sheet1['B31'].api.Font.Bold = True
    sheet1['B32'].value = 'Fall'
    sheet1['B32'].api.Font.Bold = True
    sheet1['B33'].value = corr['Fall']['Attendance (%)']

    sheet1['F32'].value = 'Fall'
    sheet1['F32'].api.Font.Bold = True
    sheet1['F33'].value = corr['Spring']['Attendance (%)']


    pairplot = sheet1.pictures.add(
            fig_pairplot,
            name='Pairplot',
            update=True,
            left=sheet1.range(f'B41').left,
            top=sheet1.range(f'B41').top
        )
    pairplot.width = 250
    pairplot.height = 250

    math_scores_fall = sheet1.pictures.add(
            math_plots['Fall'],
            name='math_scores_fall',
            update=True,
            left=sheet1.range(f'L32').left,
            top=sheet1.range(f'L32').top
        )
    math_scores_fall.width = 350
    math_scores_fall.height = 250
    math_scores_spring = sheet1.pictures.add(
            math_plots['Spring'],
            name='math_scores_spring',
            update=True,
            left=sheet1.range(f'L50').left,
            top=sheet1.range(f'L50').top
        )
    math_scores_spring.width = 350
    math_scores_spring.height = 250
    ##########


    ##########

    ##########

    pie1 = sheet1.pictures.add(
        pie_charts['Fall'],
        name='Pie plot',
        update=True,
        left=sheet1.range(f'C69').left,
        top=sheet1.range(f'C69').top
    )
    pie1.width = 400
    pie1.height = 200

    pie2 = sheet1.pictures.add(
        pie_charts['Spring'],
        name='Pie plot 2',
        update=True,
        left=sheet1.range(f'C85').left,
        top=sheet1.range(f'C85').top
    )
    pie2.width = 400
    pie2.height = 200

    avg_scores_fall = sheet1.pictures.add(
            average_scores_by_income_plots['Fall'],
            name='avg_scores_fall',
            update=True,
            left=sheet1.range(f'P69').left,
            top=sheet1.range(f'P69').top
        )
    avg_scores_fall.width = 350
    avg_scores_fall.height = 250

    avg_scores_spring = sheet1.pictures.add(
            average_scores_by_income_plots['Spring'],
            name='avg_scores_spring',
            update=True,
            left=sheet1.range(f'P84').left,
            top=sheet1.range(f'P84').top
        )
    avg_scores_spring.width = 350
    avg_scores_spring.height = 250

    wb.save(f'Output/{YEAR}_summary_report.xlsx')



create_excel_report(
    number_students_report,
    YEAR,
    average_scores_data,
    pass_rates_report,
    avg_project_Scores,
    pass_fail_dict_results,
    pie_charts,
    corr,
    fig_pairplot,
    math_plots,
    average_scores_by_income_plots,
)
