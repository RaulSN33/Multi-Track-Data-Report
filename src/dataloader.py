from os import listdir

from src.datawrangling import (
    load_file,
    custom_replace,
    data_concatenation,
    dtype_transformation,
    term_data_filler
)
from src.helpers import subjects, replace_values_mapping_dict


class DataLoader():
    def __init__(
            self,
            route: str,
            output_data_route: str
    ):
        self.route = route
        self.files = listdir(self.route)
        self.output_data_route = output_data_route

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
                df.to_csv(f'{self.output_data_route}/consolidated_data_{school_year}.csv')
                print(f'Saved consolidated data at: {self.output_data_route}/consolidated_data_{school_year}.csv')
                annual_data = term_data_filler(
                    df
                )
                data_dict[school_year] = annual_data

        self.data = data_dict
        self.available_years = self.data.keys()

