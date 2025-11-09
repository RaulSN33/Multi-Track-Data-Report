import os

import pandas as pd

from src.DataClass import ByTermStudentData
from src.helpers import subjects, terms_mapping_dict, tracks


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


def avg_by_track_income(data,year):
    first_term = data[year]['Fall'].df
    second_term = data[year]['Spring'].df

    summary_avg1 = first_term[subjects+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()
    summary_avg2 = second_term[subjects+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()

    return summary_avg1, summary_avg2


def pass_vs_fail_analytics(
        data,
        year,
        terms,
):
    dict_results = {}
    for term in terms:
        first_term = data[year][term].df

        summary_passfail = (
            first_term.groupby(['Track', 'IncomeStudent', 'Passed (Y/N)'])
            .size()
            .reset_index(name='Count')
        )

        # Step 2: For plotting convenience, pivot table
        pivot_data = summary_passfail.pivot_table(
            index=['Track', 'IncomeStudent'],
            columns='Passed (Y/N)',
            values='Count',
            fill_value=0
        ).reset_index()

        dict_results[term] = pivot_data

    return dict_results
