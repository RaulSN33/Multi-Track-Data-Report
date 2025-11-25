
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

def multiyear_report(
        data,
        available_years,
):
    print("We're still working on this option, please come back later!")

    total_number_students_dict = formula_loop_filler(
        data,
        available_years,
        terms,
        total_number_students
    )
    # total_number_students_dict = total_number_students_dict[YEAR]
    # number_students_report = pd.DataFrame(total_number_students_dict)

    subject_averages = formula_loop_filler(
        data,
        available_years,
        terms,
        subject_avg
    )
    # subject_averages = subject_averages[YEAR]
    # subject_averages = pd.DataFrame(subject_averages)

    average_scores_data = formula_loop_filler(
        data,
        available_years,
        terms,
        average_calculation
    )
    # average_scores_data = average_scores_data[YEAR]

    average_attendance = formula_loop_filler(
        data,
        available_years,
        terms,
        average_calculation,
        columns_to_compute_average=['Attendance (%)']
    )
    # average_attendance = average_attendance[YEAR]
    # average_attendance = pd.concat(average_attendance, axis=1)
    # average_attendance.columns = average_attendance.columns.droplevel(1)

    pass_rates_data = formula_loop_filler(
        data,
        available_years,
        terms,
        pass_vs_fail_analytics,
        normalize=True,
        by_exchange_students=False
    )
    # pass_rates_data = pass_rates_data[YEAR]
    # pass_rates_report = pd.DataFrame(pass_rates_data)

    normalized_pass_rates = formula_loop_filler(
        data,
        available_years,
        terms,
        pass_vs_fail_analytics,
        normalize=True,
        by_exchange_students=True
    )
    # normalized_pass_rates = normalized_pass_rates[YEAR]
    # normalized_pass_rates = pd.DataFrame(normalized_pass_rates).reset_index()
    # normalized_pass_rates['IncomeStudent'] = normalized_pass_rates['IncomeStudent'].replace(
    #     {0: 'Local', 1: 'Foreigner'})
    # normalized_pass_rates.set_index(['Track', 'IncomeStudent'], inplace=True)

    avg_project_Scores = formula_loop_filler(
        data,
        available_years,
        terms,
        average_calculation,
        columns_to_compute_average=['ProjectScore'],
    )
    a = 0
    # avg_project_Scores = avg_project_Scores[YEAR]
    # avg_project_Scores = pd.concat(avg_project_Scores, axis=1)
    # avg_project_Scores.columns = avg_project_Scores.columns.droplevel(1)
