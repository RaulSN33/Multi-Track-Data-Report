import os

import pandas as pd

from src.dataclass import ByTermStudentData
from src.helpers import (
    subjects,
    terms_mapping_dict
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


