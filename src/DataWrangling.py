import os

import pandas as pd

from src.DataClass import ByTermStudentData
from src.helpers import (
    subjects,
    terms_mapping_dict,
    tracks,
    columns_to_compute_average
)

def load_file(
        route: str,
        file: str
) -> dict[str:pd.DataFrame]:

    return pd.read_excel(
                os.path.join(route, file),
                sheet_name=None,
                index_col=0,
                # na_values= # convrt to othr values in other funct
            )


def custom_replace(
        df: pd.DataFrame,
        cols_to_filter: str,
        values_to_replace: dict
) -> pd.DataFrame:

    df[cols_to_filter] = df[cols_to_filter].replace(values_to_replace)

    return df


def data_concatenation(
        file_dict: dict[str:pd.DataFrame]
) -> pd.DataFrame:

    df = pd.concat(file_dict, axis=0).reset_index()
    df = df.rename(columns={'level_0': 'Track'})

    return df


def dtype_transformation(
        df:pd.DataFrame,
        subjects: list
) -> pd.DataFrame:
    df[subjects] = df[subjects].astype(float)
    return df


def term_data_filler(
        df:pd.DataFrame
)-> dict[str: ByTermStudentData]:
    annual_data = {}
    df_to_loop = df.copy()
    for term_idx, term_str in terms_mapping_dict.items():
        annual_data[term_str] = df_to_loop[df_to_loop['Term'] == term_idx]
        annual_data[term_str] = ByTermStudentData(
                    annual_data[term_str],
                    subjects
                )
    return annual_data


def avg_by_track_income(
        data: ByTermStudentData,
        year: str
):
    first_term = data[year]['Fall'].df
    second_term = data[year]['Spring'].df

    summary_avg1 = first_term[subjects+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()
    summary_avg2 = second_term[subjects+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()

    return summary_avg1, summary_avg2


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
    pass_rates_pct.index = pass_rates_df.index

    return pass_rates_pct

def total_number_students(
        data: ByTermStudentData,
        year: str,
        term: str,
)-> pd.DataFrame:

    df = data[year][term].df
    grouped_by = df.groupby(['Track', 'IncomeStudent']).count()

    return grouped_by['StudentID']


def average_calculation(
        data: ByTermStudentData,
        year: str,
        term: str,
        columns_to_compute_average: list = columns_to_compute_average
)-> pd.DataFrame:

    df = data[year][term].df
    grouped_by = df[columns_to_compute_average+['Track']].groupby(['Track']).mean()

    return grouped_by


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

    return corr_df
