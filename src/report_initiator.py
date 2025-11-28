from src.dataloader import DataLoader
from src.one_year_report import one_year_report
from src.multiyear_report import multiyear_report

def report_initiator(
        input_route,
        output_data_route,
        output_report_route,
):
    loader = DataLoader(
        input_route,
        output_data_route
    )
    loader.get_data()

    data = loader.data
    available_years = list(loader.available_years)

    print('Read the input directory successfully.\n')
    print(f'Available years to create report: {available_years}\n')

    print(
        "Type of report to create:\n"
        "  1) single_year\n"
        "  2) multi_year\n"
    )

    choice = input("Enter 'single_year' or 'multi_year'").strip().lower()

    if choice in {"single_year"}:
        print(f"\nPlease enter a year from: {available_years}")
        year = input("Year: ").strip()

        if isinstance(available_years[0], int):
            try:
                year_val = int(year)
            except ValueError:
                print("That doesn't look like a valid number for a year.")
                return
            if year_val not in available_years:
                print("Year not found in available years. Please try again.")
                return
            year_to_use = year_val
        else:
            if year not in available_years:
                print("Year not found in available years. Please try again.")
                return
            year_to_use = year

        one_year_report(
            data=data,
            available_years=available_years,
            YEAR=year_to_use,
            output_report_route=output_report_route
        )
        print(f"Single-year report saved in {output_data_route}/{year_to_use}_summary_report.xlsx")

    elif choice in {"multi_year"}:
        multiyear_report(
        data = data,
        available_years = available_years,
    )
    else:
        print("No valid option selected, please try again.")