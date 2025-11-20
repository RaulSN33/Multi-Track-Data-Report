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
    correlation_calc,
    subject_avg
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

subject_averages = formula_loop_filler(
    data,
    available_years,
    terms,
    subject_avg
)
subject_averages = subject_averages[YEAR]
subject_averages = pd.DataFrame(subject_averages)

average_scores_data = formula_loop_filler(
    data,
    available_years,
    terms,
    average_calculation
)
average_scores_data = average_scores_data[YEAR]

average_attendance = formula_loop_filler(
    data,
    available_years,
    terms,
    average_calculation,
    columns_to_compute_average = ['Attendance (%)']
)
average_attendance = average_attendance[YEAR]
average_attendance = pd.concat(average_attendance, axis=1)
average_attendance.columns=average_attendance.columns.droplevel(1)


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


normalized_pass_rates = formula_loop_filler(
    data,
    available_years,
    terms,
    pass_vs_fail_analytics,
    normalize=True,
    by_exchange_students=True
)
normalized_pass_rates = normalized_pass_rates[YEAR]
normalized_pass_rates = pd.DataFrame(normalized_pass_rates).reset_index()
normalized_pass_rates['IncomeStudent']=normalized_pass_rates['IncomeStudent'].replace({0:'Local',1:'Foreigner'})
normalized_pass_rates.set_index(['Track', 'IncomeStudent'], inplace = True)

avg_project_Scores = formula_loop_filler(
    data,
    available_years,
    terms,
    average_calculation,
    columns_to_compute_average = ['ProjectScore'],
)
avg_project_Scores = avg_project_Scores[YEAR]
avg_project_Scores = pd.concat(avg_project_Scores, axis = 1)
avg_project_Scores.columns=avg_project_Scores.columns.droplevel(1)


#%%

"""
3. Cross-Track Comparative Analysis 
Visualize distributions of History grades for each track using histograms or boxplots 
Compare average Mathematics scores between tracks 
Analyze correlations between attendance and project scores per track 
"""
#
# def pct_passed_pie2(pass_fail_info, title):
#     """
#     Create side-by-side pie charts per Track showing the proportion of Local vs Foreigner
#     among those who passed and those who failed.
#     """
#     tracks = pass_fail_info.index.get_level_values('Track').unique()
#     fig, axes = plt.subplots(len(tracks), 2, figsize=(10, 4 * len(tracks)))
#     fig.suptitle(title, fontsize=16, fontweight='bold')
#
#     for i, track in enumerate(tracks):
#         track_data = pass_fail_info.loc[track]
#
#         # Extract counts
#         passed = track_data['Y']
#         failed = track_data['N']
#
#         # Pie for passed (locals vs foreigners)
#         axes[i, 0].pie(
#             passed,
#             labels=passed.index,
#             autopct='%1.1f%%',
#             startangle=90,
#             colors=['#4CAF50', '#81C784']
#         )
#         axes[i, 0].set_title(f"{track} – Passed")
#
#         # Pie for failed (locals vs foreigners)
#         axes[i, 1].pie(
#             failed,
#             labels=failed.index,
#             autopct='%1.1f%%',
#             startangle=90,
#             colors=['#F44336', '#E57373']
#         )
#         axes[i, 1].set_title(f"{track} – Failed")
#
#     sns.despine()
#     plt.tight_layout(rect=[0, 0, 1, 0.96])
#     plt.show()
#     return fig

# def nested_pass_fail_local_foreigner(df_pivot, title="Pass/Fail → Local vs Foreigner"):
#     """
#
#     df_pivot: pivoted DataFrame like:
#         index: MultiIndex ['Track','IncomeStudent']  (IncomeStudent in {'Local','Foreigner'})
#         columns: ['N','Y']  (counts; N = failed, Y = passed)
#
#     Example structure:
#                      N     Y
#     Track   IncomeStudent
#     BM      Local        6.0  51.0
#             Foreigner    5.0  49.0
#
#     """
#
#     # Ensure expected structure
#     required_cols = {'N','Y'}
#     if not required_cols.issubset(set(map(str, df_pivot.columns))):
#         raise ValueError("df_pivot must have columns ['N','Y'] with counts.")
#
#     # Prepare plotting by track
#     tracks = df_pivot.index.get_level_values('Track').unique()
#     n = len(tracks)
#     fig, axes = plt.subplots(1, n, figsize=(6*n, 6), squeeze=False)
#     axes = axes[0]
#     fig.suptitle(title, fontsize=12, fontweight='bold')
#
#     for ax, track in zip(axes, tracks):
#         # Slice rows for this track
#         sub = df_pivot.loc[track]
#
#         # Make sure we have both Local and Foreigner rows (fill 0s if one is missing)
#         sub = sub.reindex(['Local','Foreigner']).fillna(0)
#
#         # Inner ring (Passed vs Failed) totals for this track
#         y_total = float(sub['Y'].sum())
#         n_total = float(sub['N'].sum())
#         inner_sizes = [y_total, n_total]  # [Passed, Failed]
#
#         # Outer ring: within Passed -> [Local, Foreigner], within Failed -> [Local, Foreigner]
#         y_local, y_foreign = float(sub.loc['Local','Y']), float(sub.loc['Foreigner','Y'])
#         n_local, n_foreign = float(sub.loc['Local','N']), float(sub.loc['Foreigner','N'])
#         outer_sizes = [y_local, y_foreign, n_local, n_foreign]
#
#         # Colors
#         inner_colors = ['#4CAF50', '#F44336']  # Passed, Failed
#         outer_colors = ['#9BE5A2', '#58C96B',  # Passed: Local, Foreigner (greens)
#                         '#F9A3A3', '#E45C5C']  # Failed: Local, Foreigner (reds)
#
#         # Draw outer ring first (so inner sits on top visually clean) — outer radius 1.0, width 0.35
#         startangle = 90
#         ax.pie(
#             outer_sizes,
#             radius=1.0,
#             startangle=startangle,
#             labels=['Local','Foreigner','Local','Foreigner'],
#             labeldistance=1.08,
#             colors=outer_colors,
#             wedgeprops=dict(width=0.35, edgecolor='white'),
#             # omit autopct here; we'll show proportions in a legend-like note
#         )
#
#         # Draw inner ring — radius 0.65, width 0.35
#         ax.pie(
#             inner_sizes,
#             radius=0.65,
#             startangle=startangle,
#             labels=['Passed','Failed'],
#             labeldistance=0.5,
#             colors=inner_colors,
#             autopct=lambda p: f'{p:.1f}%',
#             pctdistance=0.78,
#             wedgeprops=dict(width=0.35, edgecolor='white')
#         )
#
#         ax.set(aspect="equal")
#         ax.set_title(str(track), pad=10, fontsize=12, fontweight='bold')
#
#         # Add a small text box with the Local/Foreigner split *within* each inner slice
#         # (percentages are relative to Passed and to Failed respectively)
#         def pct(a, b):
#             total = a + b
#             return (0.0 if total == 0 else 100.0 * a / total,
#                     0.0 if total == 0 else 100.0 * b / total)
#
#         y_loc_pct, y_for_pct = pct(y_local, y_foreign)
#         n_loc_pct, n_for_pct = pct(n_local, n_foreign)
#
#         note = (
#             f"Passed: Local {y_loc_pct:.1f}% • Foreigner {y_for_pct:.1f}%\n"
#             f"Failed: Local {n_loc_pct:.1f}% • Foreigner {n_for_pct:.1f}%"
#         )
#         ax.text(0, -1.25, note, ha='center', va='top', fontsize=9)
#
#     # plt.tight_layout()
#     plt.show()
#     return fig
#

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
        title = f'Pass Rates by track, {YEAR}; {term}'
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
    math_plots[subject] = {}
    for term in terms:
        math_plots[subject][term] = by_subject_boxplot(
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
        groupby_summaries=average_scores_by_income[term],
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
    subject_averages,
    pass_rates_report,
    average_attendance,
    avg_project_Scores,
    pass_fail_dict_results,
    pie_charts,
    normalized_pass_rates,
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

    sheet1['F2'].value = '2.2 Average grades'
    sheet1['F2'].api.Font.Bold = True
    sheet1['F3'].value = number_students_report

    sheet1['L2'].value = '2.3 Average subject scores; Fall Semester'
    sheet1['L2'].api.Font.Bold = True
    sheet1['L3'].value = average_scores_data['Fall']

    sheet1['R2'].value = '2.4 Average subject scores; Spring Semester'
    sheet1['R2'].api.Font.Bold = True
    sheet1['R3'].value = average_scores_data['Spring']

    sheet1['W2'].value = '2.5 Average Attendance'
    sheet1['W2'].api.Font.Bold = True
    sheet1['W3'].value = average_attendance

    sheet1['AA2'].value = '2.6 Average Project Scores by term'
    sheet1['AA2'].api.Font.Bold = True
    sheet1['AA3'].value = avg_project_Scores

    sheet1['AE2'].value = '2.7 Average Pass Rates'
    sheet1['AE2'].api.Font.Bold = True
    sheet1['AE3'].value = pass_rates_report

    ##########
    # pass_fail_dict_results

    ##########
    sheet1['B11'].value = '3.3 Correlation between attendance and project scores'
    sheet1['B11'].api.Font.Bold = True
    sheet1['B12'].value = 'Fall'
    sheet1['B12'].api.Font.Bold = True
    sheet1['B12'].value = corr['Fall']['Attendance (%)']

    sheet1['F12'].value = 'Fall'
    sheet1['F12'].api.Font.Bold = True
    sheet1['F13'].value = corr['Spring']['Attendance (%)']


    pairplot = sheet1.pictures.add(
            fig_pairplot,
            name='Pairplot',
            update=True,
            left=sheet1.range(f'B21').left,
            top=sheet1.range(f'B21').top
        )
    pairplot.width = 250
    pairplot.height = 250


    sheet1['L11'].value = '3.2 Average scores; History'
    sheet1['L11'].api.Font.Bold = True
    history_scores_fall = sheet1.pictures.add(
            math_plots['History']['Fall'],
            name='history_scores_fall',
            update=True,
            left=sheet1.range(f'L12').left,
            top=sheet1.range(f'L12').top
        )
    history_scores_fall.width = 350
    history_scores_fall.height = 250
    history_scores_spring = sheet1.pictures.add(
            math_plots['History']['Spring'],
            name='history_scores_spring',
            update=True,
            left=sheet1.range(f'L29').left,
            top=sheet1.range(f'L29').top
        )
    history_scores_spring.width = 350
    history_scores_spring.height = 250

    sheet1['V11'].value = '3.3 Average scores; Math'
    sheet1['V11'].api.Font.Bold = True
    math_scores_fall = sheet1.pictures.add(
            math_plots['Math']['Fall'],
            name='math_scores_fall',
            update=True,
            left=sheet1.range(f'V12').left,
            top=sheet1.range(f'V12').top
        )
    math_scores_fall.width = 350
    math_scores_fall.height = 250
    math_scores_spring = sheet1.pictures.add(
            math_plots['Math']['Spring'],
            name='math_scores_spring',
            update=True,
            left=sheet1.range(f'V29').left,
            top=sheet1.range(f'V29').top
        )
    math_scores_spring.width = 350
    math_scores_spring.height = 250
    ##########

    ##########

    ##########
    sheet1['B46'].value = '4.1 Passing Rates by track'
    sheet1['B46'].api.Font.Bold = True
    sheet1['B47'].values = normalized_pass_rates
    # sheet1['B4'].values = "asdacsdasdcad"

    pie1 = sheet1.pictures.add(
        pie_charts['Fall'],
        name='Pie plot',
        update=True,
        left=sheet1.range(f'B59').left,
        top=sheet1.range(f'B59').top
    )
    pie1.width = 400
    pie1.height = 200


    pie2 = sheet1.pictures.add(
        pie_charts['Spring'],
        name='Pie plot 2',
        update=True,
        left=sheet1.range(f'B72').left,
        top=sheet1.range(f'B72').top
    )
    pie2.width = 400
    pie2.height = 200

    sheet1['O46'].value = '3.2 Average Grades by track'
    sheet1['O46'].api.Font.Bold = True
    avg_scores_fall = sheet1.pictures.add(
            average_scores_by_income_plots['Fall'],
            name='avg_scores_fall',
            update=True,
            left=sheet1.range(f'O47').left,
            top=sheet1.range(f'O47').top
        )
    avg_scores_fall.width = 350
    avg_scores_fall.height = 250

    avg_scores_spring = sheet1.pictures.add(
            average_scores_by_income_plots['Spring'],
            name='avg_scores_spring',
            update=True,
            left=sheet1.range(f'O65').left,
            top=sheet1.range(f'O65').top
        )
    avg_scores_spring.width = 350
    avg_scores_spring.height = 250

    wb.save(f'Output/{YEAR}_summary_report.xlsx')



create_excel_report(
    number_students_report,
    YEAR,
    average_scores_data,
    subject_averages,
    pass_rates_report,
    average_attendance,
    avg_project_Scores,
    pass_fail_dict_results,
    pie_charts,
    normalized_pass_rates,
    corr,
    fig_pairplot,
    math_plots,
    average_scores_by_income_plots,
)
