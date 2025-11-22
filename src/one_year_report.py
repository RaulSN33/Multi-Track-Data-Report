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
    terms_mapping_dict
)
from src.ploting import (
    average_grades,
    by_subject_boxplot,
    pct_passed_pie
)

from src.xlsx_report import (
    one_year_excel_report
)

def one_year_report(
        data: DataLoader,
        available_years,
        YEAR
):
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
        columns_to_compute_average=['Attendance (%)']
    )
    average_attendance = average_attendance[YEAR]
    average_attendance = pd.concat(average_attendance, axis=1)
    average_attendance.columns = average_attendance.columns.droplevel(1)

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
    normalized_pass_rates['IncomeStudent'] = normalized_pass_rates['IncomeStudent'].replace(
        {0: 'Local', 1: 'Foreigner'})
    normalized_pass_rates.set_index(['Track', 'IncomeStudent'], inplace=True)

    avg_project_Scores = formula_loop_filler(
        data,
        available_years,
        terms,
        average_calculation,
        columns_to_compute_average=['ProjectScore'],
    )
    avg_project_Scores = avg_project_Scores[YEAR]
    avg_project_Scores = pd.concat(avg_project_Scores, axis=1)
    avg_project_Scores.columns = avg_project_Scores.columns.droplevel(1)


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
    pass_fail_dict_results['IncomeStudent'] = pass_fail_dict_results['IncomeStudent'].replace(
        {0: 'Local', 1: 'Foreigner'})
    pass_fail_dict_results.set_index(['Track', 'IncomeStudent'], inplace=True)

    corr = formula_loop_filler(
        data,
        available_years,
        terms,
        correlation_calc,

    )
    corr = corr[YEAR]
    pie_charts = {}
    # pie_charts
    for _, term in terms_mapping_dict.items():
        pie_charts[term] = pct_passed_pie(
            pass_fail_dict_results.reset_index(),
            data[YEAR][term].df,
            title=f'Pass Rates by track, {YEAR}; {term}'
        )


    a = data[YEAR]['Spring'].df[
        [
            'Track',
            'Attendance (%)',
            'ProjectScore'
        ]
    ]
    fig_pairplot = sns.pairplot(
        a,
        hue='Track',
        markers=["o", "s", "D"],
    )
    plt.show()

    fig_pairplot = fig_pairplot.fig

    subjects = ['Math', 'History']
    math_plots = {}
    for subject in subjects:
        math_plots[subject] = {}
        for term in terms:
            math_plots[subject][term] = by_subject_boxplot(
                data[YEAR][term].df,
                subject,
                year=YEAR,
                term=term
            )


    """
    4. Cohort-Level Analysis 
    Calculate average grades and pass rates segmented by cohort 
    Compare academic performance of income-supported students (IncomeStudent = True) 
    against others
    """

    average_scores_by_income = formula_loop_filler(
        data,
        available_years,
        terms,
        avg_by_track_income,
    )
    average_scores_by_income = average_scores_by_income[YEAR]

    average_scores_by_income_plots = {}
    for term in terms:
        average_scores_by_income_plots[term] = average_grades(
            groupby_summaries=average_scores_by_income[term],
            plot_title=f'Average grades by track, {YEAR}; {term}'

        )


    """
    5. Final Report Generation 
    Export a summary report as a CSV or Excel file encompassing all computed statistics 
    Optionally generate charts and plots using matplotlib or seaborn libraries for visual 
    interpretation 
    """

    one_year_excel_report(
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
        average_scores_by_income
    )

