import pandas as pd
from numpy import nan
from src.DataClass import ByTermStudentData
import os

subjects = [
    'Math',
    'English',
    'Science',
    'History'
]

replace_values_mapping_dict = {
    'nans':{
        'columns':subjects,
        'values_to_replace':{
            'WAIVE':nan,
            'WAIVED':nan
        }
    },
    'passed': {
        'columns':'Passed (Y/N)',
        'values_to_replace':{
            'no':'N',
            'y':'Y'
        }
    }
}

terms_mapping_dict = {
    1:'Fall',
    2:'Spring'
}

class DataLoader():
    def __init__(
            self,
            route: str
    ):
        self.route = route
        self.files = os.listdir(self.route)
        # self.get_data()

    def get_data(
            self
    ):

        data_dict = {}
        for file in self.files:
            if file.endswith('.xlsx'):
                file_name = file.split('.')[0]
                school_year = file_name.split('_')[2]
                file_dict = load_file(
                    self.route,
                    file
                )
                df = data_concatenation(file_dict)

                for _, mapping_dict in replace_values_mapping_dict.items():

                    df = custom_replace(
                        df,
                        cols_to_filter=mapping_dict['columns'],
                        values_to_replace=mapping_dict['values_to_replace']
                    )

                df = dtype_transformation(df, subjects)

                annual_data = term_data_filler(
                    df
                )
                data_dict[school_year] = annual_data

        self.data = data_dict
        # return self.data

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
        df,
        subjects
):
    df[subjects] = df[subjects].astype(float)
    return df

def term_data_filler(df:pd.DataFrame):
    annual_data = {}
    df_to_loop = df.copy()
    for term_idx, term_str in terms_mapping_dict.items():
        annual_data[term_str] = df_to_loop[df_to_loop['Term'] == term_idx]
        annual_data[term_str] = ByTermStudentData(
                    annual_data[term_str],
                    subjects
                )
    return annual_data
