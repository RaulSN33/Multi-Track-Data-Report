from src.dataloader import DataLoader
from src.one_year_report import one_year_report
from src.multiyear_report import multiyear_report

route = 'Input'
loader = DataLoader(route)
loader.get_data()

data = loader.data
available_years = list(loader.available_years)

# one_year_report(
#             data=data,
#             available_years=available_years,
#             YEAR=year_to_use
#         )

multiyear_report(
    data=data,
    available_years=available_years,
)