import pandas as pd

from src.DataClass import ByTermStudentData
from src.helpers import (
    subjects,
    columns_to_compute_average
)


def pass_vs_fail_analytics(
        data: ByTermStudentData,
        year: str,
        term: str,
        normalize: bool = False,
        by_exchange_students: bool = True
)-> pd.DataFrame:
    if by_exchange_students:
        cols_group_by = ['Track', 'IncomeStudent', 'Passed (Y/N)']
        cols_to_reindex = ['Track', 'IncomeStudent']

    else:
        cols_group_by =  ['Track', 'Passed (Y/N)']
        cols_to_reindex = 'Track'


    first_term = data[year][term].df

    summary_passfail = (
        first_term.groupby(cols_group_by)
        .size()
        .reset_index(name='Count')
    )

    # Step 2: For plotting convenience, pivot table
    pivot_data = summary_passfail.pivot_table(
        index=cols_to_reindex,
        columns='Passed (Y/N)',
        values='Count',
        fill_value=0
    ).reset_index()

    if normalize:
        pivot_data = pass_rates_normalizer(
            pivot_data,
            cols_to_reindex
        )

    return pivot_data


def pass_rates_normalizer(
        pass_rates_df: pd.DataFrame,
        cols_set_index: list[str]
)-> pd.DataFrame:
    pass_rates_df.set_index(cols_set_index, inplace=True)
    pass_rates_pct = pass_rates_df['Y'] / (pass_rates_df['Y'] + pass_rates_df['N'])
    # pass_rates_pct.index = pass_rates_df.index

    return pass_rates_pct


def total_number_students(
        data: ByTermStudentData,
        year: str,
        term: str,
)-> pd.DataFrame:

    df = data[year][term].df
    grouped_by = df.groupby(
        [
            'Track',
            # 'IncomeStudent'
        ]
    ).count()

    return grouped_by['StudentID']


def average_calculation(
        data: ByTermStudentData,
        year: str,
        term: str,
        columns_to_compute_average: list = subjects
)-> pd.DataFrame:

    df = data[year][term].df
    grouped_by = df[columns_to_compute_average+['Track']].groupby(['Track']).mean()


    return grouped_by

def subject_avg(
        data: ByTermStudentData,
        year: str,
        term: str,
)-> pd.DataFrame:

    df = data[year][term].df
    grouped_by = df[subjects].mean()


    return grouped_by

def avg_by_track_income(
        data: ByTermStudentData,
        year: str,
        term: str,
):
    first_term = data[year][term].df
    summary_avg1 = first_term[subjects+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()

    return summary_avg1

def formula_loop_filler(
        data: ByTermStudentData,
        available_years: list[str],
        terms: list[str],
        func_to_calc,
        **kwargs
):
    ts_data = {}
    for year in available_years:
        ts_data[year] = {}
        for term in terms:
            ts_data[year][term] = func_to_calc(
                data,
                year,
                term,
                **kwargs
            )
    return ts_data



def correlation_calc(
        data: ByTermStudentData,
        year: str,
        term: str,
        columns_to_compute_corr: list = ['Attendance (%)', 'ProjectScore']
)-> pd.DataFrame:
    # cols_list =
    df = data[year][term].df
    corr_df = df[columns_to_compute_corr+['Track']].groupby(['Track']).corr()
    # corr_df = corr_df[]


    return corr_df
