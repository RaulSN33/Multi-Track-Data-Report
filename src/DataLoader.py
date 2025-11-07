import pandas as pd
from src.DataClass import AnnualStudentData
import os

subjects = [
    'Math',
    'English',
    'Science',
    'History'
]
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
                file_dict = pd.read_excel(
                    os.path.join(self.route, file),
                    sheet_name=None,
                    index_col=0,
                    na_values=['WAIVE','WAIVED'] # convrt to othr values in other funct
                )
                df = pd.concat(file_dict, axis = 0).reset_index()
                df = df.rename(columns={'level_0':'Track'})
                df = dtype_transformation(df, subjects)
                data_dict[file_name] = AnnualStudentData(
                    df,
                    subjects
                )
                # data_dict[file_name] = AnnualStudentData(df)

        self.data = data_dict
        return self.data

def dtype_transformation(df, subjects):
    df[subjects].astype(float)
    return df