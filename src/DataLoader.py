import pandas as pd
import os

class DataLoader():
    def __init__(
            self,
            route: str
    ):
        self.route = route
        self.files = os.listdir(self.route)
        self.get_data()

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
                )
                data_dict[file_name] = file_dict

        self.data = data_dict



